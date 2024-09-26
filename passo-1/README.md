# AWS Lambda: Processamento de Arquivo JSON de S3

Este repositório contém uma função AWS Lambda simples que simula o processamento de arquivos JSON armazenados no Amazon S3. Esta é uma versão introdutória da função, que apenas baixa o arquivo do S3 e imprime o conteúdo, sem interações adicionais com outros serviços, como o DynamoDB.

## Como Funciona

A função Lambda é invocada por eventos do S3. Quando um arquivo JSON é enviado para o bucket S3 configurado, a função baixa o arquivo e registra o conteúdo nos logs.

### Fluxo de Execução

1. A função é ativada por um evento de upload no S3.
2. A função faz o download do arquivo JSON do bucket S3.
3. O conteúdo do arquivo é lido e impresso nos logs.
4. Nenhum dado é armazenado em outras fontes de dados como o DynamoDB nesta versão.

## Estrutura do Projeto

- `lambda_function.py`: Arquivo principal com a função Lambda.
- `README.md`: Este documento.

## Exemplo de Evento do S3

Você pode simular um evento S3 para testar a função com o seguinte JSON de exemplo:

```json

{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "nome-do-seu-bucket"
        },
        "object": {
          "key": "caminho/para/seu/arquivo.json"
        }
      }
    }
  ]
}

```

## Como Testar

Os alunos realizarão a atividade diretamente no console AWS, criando a função Lambda, configurando o gatilho S3 e verificando os logs.

1. No console da AWS, crie uma função Lambda.
2. Configure as permissões necessárias, incluindo a política adicional abaixo.
3. Faça upload de um arquivo JSON no bucket S3 configurado.
4. Verifique os logs da função Lambda no CloudWatch para visualizar o conteúdo do arquivo.

## Política de Permissões

Para que a função Lambda possa acessar os arquivos no bucket S3, é necessário adicionar a seguinte política ao role da função Lambda:

```json

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::nome-do-seu-bucket",
                "arn:aws:s3:::nome-do-seu-bucket/*"
            ]
        }
    ]
}


```

Substitua `nome-do-seu-bucket` pelo nome do seu bucket.

## Requisitos

- AWS CLI configurado (opcional)
- Função Lambda com permissões adequadas para acessar o bucket S3

## Próximos Passos

1. Evoluir a função para armazenar os dados extraídos no DynamoDB.
2. Adicionar tratamento de erros e outras otimizações.

## Contato

Para dúvidas ou sugestões, sinta-se à vontade para entrar em contato.

