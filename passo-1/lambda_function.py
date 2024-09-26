import json
import boto3
import logging

# Inicializando o cliente do S3
s3 = boto3.client('s3')

# Setup do logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)


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
        
        # Printando o conteúdo do arquivo JSON
        logger.info(f"Conteúdo do arquivo {object_key}: {file_content}")
        
        return {
            'statusCode': 200,
            'body': json.dumps(f"Arquivo {object_key} processado com sucesso!")
        }
    
    except Exception as e:
        logger.error(f"Erro ao processar o arquivo do S3: {e}")
        raise e
