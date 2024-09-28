import json
import boto3
import logging
from decimal import Decimal, InvalidOperation
from dateutil.parser import parse
import uuid
from datetime import datetime
from json.decoder import JSONDecodeError

# Inicializando os clientes do DynamoDB e S3
dynamodb = boto3.resource('dynamodb')
s3 = boto3.client('s3')

table = dynamodb.Table('PedidosTable')  # Substituir pelo nome da tabela DynamoDB
table_incorretos = dynamodb.Table('PedidosIncorretosTable')  # Tabela de pedidos incorretos

# Setup do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def gerar_order_id():
    return str(uuid.uuid4())

# Função para converter floats em Decimal
def converter_floats_para_decimal(item):
    if isinstance(item, list):
        return [converter_floats_para_decimal(i) for i in item]
    elif isinstance(item, dict):
        return {k: converter_floats_para_decimal(v) for k, v in item.items()}
    elif isinstance(item, float):
        return Decimal(str(item))
    else:
        return item

def validar_pedido(pedido):
    # Lista de campos obrigatórios
    campos_obrigatorios = ['customerName', 'customerEmail', 'totalAmount', 'orderDate']
    
    # Verificando campos ausentes ou inválidos
    for campo in campos_obrigatorios:
        if campo not in pedido or not pedido[campo]:
            return False, f"Campo ausente ou inválido: {campo}"

    # Validação de totalAmount (deve ser numérico)
    try:
        Decimal(str(pedido['totalAmount']))
    except (ValueError, InvalidOperation):
        return False, "Valor inválido no campo totalAmount"

    # Validação de orderDate (deve ser uma data válida)
    try:
        parse(pedido['orderDate'])
    except ValueError:
        return False, "Data inválida no campo orderDate"

    return True, None

def lambda_handler(event, context):
    logger.info(f"Evento recebido: {json.dumps(event)}")  # Logando o evento completo para depuração
    
    try:
        # Extraindo informações do evento S3
        s3_event = event['Records'][0]['s3']
        bucket_name = s3_event['bucket']['name']
        object_key = s3_event['object']['key']
        
        # Fazendo download do arquivo JSON do S3
        response = s3.get_object(Bucket=bucket_name, Key=object_key)
        file_content = response['Body'].read().decode('utf-8')
        
        # Tratando erro de JSON mal formatado
        try:
            pedidos = json.loads(file_content)
        except JSONDecodeError as e:
            logger.error(f"Erro ao decodificar o JSON do arquivo {object_key}: {e}")
            return {
                'statusCode': 400,
                'body': json.dumps(f"Erro: Arquivo JSON mal formatado: {e}")
            }

        # Verificando se é um único pedido ou uma lista de pedidos
        if isinstance(pedidos, list):
            for pedido in pedidos:
                processar_pedido(pedido, bucket_name, object_key)
        else:
            processar_pedido(pedidos, bucket_name, object_key)

        return {
            'statusCode': 200,
            'body': json.dumps(f"Arquivo {object_key} processado com sucesso!")
        }
    
    except s3.exceptions.NoSuchKey as e:
        logger.error(f"Arquivo {object_key} não encontrado no bucket {bucket_name}: {e}")
        return {
            'statusCode': 404,
            'body': json.dumps(f"Erro: Arquivo {object_key} não encontrado no bucket {bucket_name}.")
        }

    except Exception as e:
        logger.error(f"Erro ao processar o arquivo do S3: {e}")
        raise e

def processar_pedido(pedido, bucket_name, object_key):
    # Verificando se o orderId está ausente e tratando como erro
    if 'orderId' not in pedido or not pedido['orderId']:
        erro = "Campo ausente ou inválido: orderId"
        armazenar_pedido_incorreto(pedido, erro, bucket_name, object_key)
        return

    # Validando o pedido
    valido, erro = validar_pedido(pedido)
    if not valido:
        armazenar_pedido_incorreto(pedido, erro, bucket_name, object_key)
        return

    # Convertendo os valores numéricos (float) para Decimal antes de inserir no DynamoDB
    pedido = converter_floats_para_decimal(pedido)

    # Inserir o pedido no DynamoDB
    inserir_pedido_dynamodb(pedido)

def inserir_pedido_dynamodb(pedido):
    try:
        # Inserindo no DynamoDB
        table.put_item(Item=pedido)
        logger.info(f"Pedido {pedido['orderId']} com status {pedido.get('status', 'desconhecido')} inserido no DynamoDB")
    except Exception as e:
        logger.error(f"Erro ao inserir o pedido {pedido['orderId']} no DynamoDB: {e}")
        raise e

def armazenar_pedido_incorreto(pedido, motivo_erro, bucket_name, object_key):
    error_timestamp = datetime.utcnow().isoformat()

    # Se o pedido não tiver orderId, gerar um ID temporário
    order_id = pedido.get('orderId', gerar_order_id())

    item_incorreto = {
        'orderId': order_id,  # Usar o ID gerado se orderId estiver ausente
        'errorTimestamp': error_timestamp,
        'bucketName': bucket_name,
        'fileName': object_key,
        'orderData': converter_floats_para_decimal(pedido),  # Convertendo floats para Decimal
        'errorReason': motivo_erro
    }

    try:
        # Inserir no DynamoDB
        table_incorretos.put_item(Item=item_incorreto)
        logger.info(f"Pedido {order_id} armazenado em PedidosIncorretosTable com erro: {motivo_erro}")
    except Exception as e:
        logger.error(f"Erro ao inserir o pedido incorreto {order_id} no DynamoDB: {e}")
        raise e
