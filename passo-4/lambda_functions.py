import json
import boto3
import os
import logging

# Configuração de logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Inicializa os clientes S3 e SNS
    s3_client = boto3.client('s3')
    sns_client = boto3.client('sns')
    
    # Obter variáveis de ambiente
    bucket_name = os.environ['BUCKET_NAME']  # Nome do bucket S3
    sns_topic_arn = os.environ['SNS_TOPIC_ARN']  # ARN do tópico SNS
    url_expiration = int(os.environ.get('URL_EXPIRATION', '600'))  # Expiração em segundos
    
    logger.info(f"Iniciando processamento do evento: {json.dumps(event)}")
    
    # Iterar sobre os registros do DynamoDB Stream
    for record in event['Records']:
        logger.info(f"Processando registro ID: {record['eventID']} - Evento: {record['eventName']}")
        
        if record['eventName'] == 'INSERT':
            try:
                # Extrair os dados do novo item inserido
                new_image = record['dynamodb']['NewImage']
                
                # Extrair campos específicos
                order_id = new_image['orderId']['S']
                error_timestamp = new_image['errorTimestamp']['S']
                error_reason = new_image['errorReason']['S']
                bucket_name_item = new_image['bucketName']['S']
                file_name = new_image['fileName']['S']
                
                logger.info(f"Dados extraídos - orderId: {order_id}, fileName: {file_name}")
                
                # Extrair orderData como um JSON dinâmico
                order_data_map = new_image.get('orderData', {}).get('M', {})
                order_data = extract_order_data(order_data_map)
                
                logger.info(f"Dados do pedido extraídos: {json.dumps(order_data)}")
                
                # Gerar a URL pré-assinada
                presigned_url = s3_client.generate_presigned_url(
                    'get_object',
                    Params={'Bucket': bucket_name, 'Key': file_name},
                    ExpiresIn=url_expiration
                )
                
                logger.info(f"URL pré-assinada gerada: {presigned_url}")
                
                # Criar a mensagem para o SNS com todos os detalhes
                message = {
                    'object_key': file_name,
                    'presigned_url': presigned_url,
                    'order_details': {
                        'orderId': order_id,
                        'errorTimestamp': error_timestamp,
                        'errorReason': error_reason,
                        'bucketName': bucket_name_item,
                        'orderData': order_data  # JSON dinâmico
                    }
                }
                
                logger.info(f"Mensagem SNS a ser enviada: {json.dumps(message)}")
                
                # Publicar a mensagem no SNS
                sns_response = sns_client.publish(
                    TopicArn=sns_topic_arn,
                    Message=json.dumps(message),
                    Subject='Detalhes do Pedido Incorreto e URL Pré-Assinada'
                )
                
                logger.info(f"Mensagem publicada no SNS com MessageId: {sns_response['MessageId']}")
            
            except Exception as e:
                logger.error(f"Erro ao processar o registro ID {record['eventID']}: {str(e)}")
                continue  # Continuar com o próximo registro
        
        else:
            logger.info(f"Evento ignorado: {record['eventName']}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('URLs pré-assinadas geradas e enviadas via SNS.')
    }

def extract_order_data(order_data_map):
    """
    Converte o Map do DynamoDB para um dicionário Python.
    Trata apenas tipos simples (String, Number). Para tipos mais complexos,
    é necessário expandir esta função.
    """
    order_data = {}
    for key, value in order_data_map.items():
        if 'S' in value:
            order_data[key] = value['S']
        elif 'N' in value:
            order_data[key] = value['N']
        elif 'M' in value:
            order_data[key] = extract_order_data(value['M'])  # Recursivo para Maps aninhados
        elif 'L' in value:
            order_data[key] = extract_list(value['L'])  # Função para listas
        else:
            order_data[key] = None  # Tipo não tratado
    return order_data

def extract_list(list_values):
    """
    Converte uma lista do DynamoDB para uma lista Python.
    Trata apenas tipos simples e Maps aninhados.
    """
    result_list = []
    for item in list_values:
        if 'S' in item:
            result_list.append(item['S'])
        elif 'N' in item:
            result_list.append(item['N'])
        elif 'M' in item:
            result_list.append(extract_order_data(item['M']))  # Recursivo para Maps aninhados
        elif 'L' in item:
            result_list.append(extract_list(item['L']))  # Recursivo para listas aninhadas
        else:
            result_list.append(None)  # Tipo não tratado
    return result_list
