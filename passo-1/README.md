# AWS Lambda: Processamento de Arquivo JSON de S3

Este repositório contém uma função AWS Lambda simples que simula o processamento de arquivos JSON armazenados no Amazon S3. Nesta versão introdutória, a função baixa o arquivo do S3 e imprime o conteúdo, sem interações adicionais com o DynamoDB.

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
- `pedido_001.json`: Arquivo de teste com informações de um pedido.

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
          "key": "caminho/para/pedido_001.json"
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
3. Faça upload do arquivo `pedido_001.json` para o bucket S3 configurado.
4. Verifique os logs da função Lambda no CloudWatch para visualizar o conteúdo do arquivo.

### Conteúdo do Arquivo `pedido_001.json`

O arquivo `pedido_001.json` contém as seguintes informações:

```json

{
    "orderId": "100006",
    "customerName": "Paula Fernandes",
    "customerEmail": "paula.fernandes@email.com",
    "totalAmount": 340.00,
    "status": "Concluído",
    "orderDate": "2024-09-16T10:30:00Z"
}

```

## Resultado Esperado

Ao executar o teste, o seguinte conteúdo deve ser registrado nos logs da Lambda no CloudWatch:

```json

INFO:Conteúdo do arquivo pedido_001.json: 
{
    "orderId": "100006",
    "customerName": "Paula Fernandes",
    "customerEmail": "paula.fernandes@email.com",
    "totalAmount": 340.00,
    "status": "Concluído",
    "orderDate": "2024-09-16T10:30:00Z"
}

```

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

Substitua `nome-do-seu-bucket` pelo nome real do seu bucket.

## Requisitos

- A função Lambda precisa ter as permissões corretas para acessar o S3.
- O arquivo `pedido_001.json` deve ser colocado no bucket correto.

## Próximos Passos

1. Evoluir a função para armazenar os dados extraídos no DynamoDB.
2. Adicionar tratamento de erros e outras otimizações.

## Contato

Para dúvidas ou sugestões, sinta-se à vontade para entrar em contato.
