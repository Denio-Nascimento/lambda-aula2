# AWS Lambda: Inserindo Lote de Pedidos no DynamoDB a partir de Arquivo JSON no S3

Este repositório contém uma função AWS Lambda que processa um arquivo JSON com um lote de pedidos enviado para um bucket S3 e insere os dados no DynamoDB. O JSON contém uma lista de pedidos, como no arquivo de exemplo `pedidos_lote01.json`.

## Como Funciona

A função Lambda é invocada por eventos do S3. Quando um arquivo JSON contendo múltiplos pedidos é enviado para o bucket S3 configurado, a função faz o download do arquivo, lê o conteúdo e insere cada pedido na tabela DynamoDB.

### Fluxo de Execução

1. A função é ativada por um evento de upload no S3.
2. A função faz o download do arquivo JSON do bucket S3.
3. O conteúdo do arquivo é lido e cada pedido é inserido no DynamoDB.
4. A função lida com erros específicos, como a ausência do arquivo no S3, e registra as mensagens apropriadas nos logs.

## Estrutura do Projeto

- `lambda_function.py`: Arquivo principal com a função Lambda.
- `README.md`: Este documento.
- `pedidos_lote01.json`: Arquivo de teste com informações de um lote de pedidos.
- `pedidos_lote02.json`: Segundo arquivo de teste.
- `pedidos_lote03.json`: Terceiro arquivo de teste.

## Exemplo de Evento do S3

Você pode simular um evento S3 para testar a função com o seguinte JSON de exemplo:

```JSON

{
  "Records": [
    {
      "s3": {
        "bucket": {
          "name": "nome-do-seu-bucket"
        },
        "object": {
          "key": "caminho/para/pedidos_lote01.json"
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
3. Faça upload do arquivo `pedidos_lote01.json` para o bucket S3 configurado.
4. Verifique os logs da função Lambda no CloudWatch para visualizar o processamento do arquivo.
5. Para os arquivos `pedidos_lote02.json` e `pedidos_lote03.json`, configure o **S3 Event Notification** no bucket S3. Ao inserir os arquivos no bucket, o evento do S3 invocará a função Lambda automaticamente. 
6. Após o upload dos arquivos `pedidos_lote02.json` e `pedidos_lote03.json`, verifique os logs no CloudWatch para confirmar o processamento e consulte o DynamoDB para verificar se os pedidos foram inseridos corretamente.

### Conteúdo do Arquivo `pedidos_lote01.json`

O arquivo `pedidos_lote01.json` contém a seguinte lista de pedidos:

```JSON

[
  {
    "orderId": "100001",
    "customerName": "João Silva",
    "customerEmail": "joao.silva@email.com",
    "totalAmount": 120.75,
    "status": "Pendente",
    "orderDate": "2024-09-16T08:30:00Z"
  },
  {
    "orderId": "100002",
    "customerName": "Maria Souza",
    "customerEmail": "maria.souza@email.com",
    "totalAmount": 75.99,
    "status": "Pendente",
    "orderDate": "2024-09-16T09:00:00Z"
  },
  {
    "orderId": "100003",
    "customerName": "Carlos Lima",
    "customerEmail": "carlos.lima@email.com",
    "totalAmount": 250.50,
    "status": "Pendente",
    "orderDate": "2024-09-16T09:15:00Z"
  },
  {
    "orderId": "100004",
    "customerName": "Ana Pereira",
    "customerEmail": "ana.pereira@email.com",
    "totalAmount": 90.25,
    "status": "Pendente",
    "orderDate": "2024-09-16T09:45:00Z"
  },
  {
    "orderId": "100005",
    "customerName": "José Santos",
    "customerEmail": "jose.santos@email.com",
    "totalAmount": 45.50,
    "status": "Pendente",
    "orderDate": "2024-09-16T10:00:00Z"
  }
]

```

## Resultado Esperado

Ao executar o teste, a função Lambda deve inserir cada pedido da lista no DynamoDB e os seguintes logs devem ser exibidos no CloudWatch:

```

INFO:Pedido 100001 com status Pendente inserido no DynamoDB.
INFO:Pedido 100002 com status Pendente inserido no DynamoDB.
INFO:Pedido 100003 com status Pendente inserido no DynamoDB.
INFO:Pedido 100004 com status Pendente inserido no DynamoDB.
INFO:Pedido 100005 com status Pendente inserido no DynamoDB.

```

Se ocorrer algum erro ao processar o arquivo ou inserir os pedidos, uma mensagem apropriada será registrada no log.

## Política de Permissões

Para que a função Lambda possa acessar os arquivos no bucket S3 e inserir itens no DynamoDB, é necessário adicionar a seguinte política ao IAM Role da função Lambda:

```JSON

{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket",
                "dynamodb:PutItem"
            ],
            "Resource": [
                "arn:aws:s3:::nome-do-seu-bucket",
                "arn:aws:s3:::nome-do-seu-bucket/*",
                "arn:aws:dynamodb:REGIAO:ID_DA_CONTA:table/PedidosTable"
            ]
        }
    ]
}

```

Substitua `nome-do-seu-bucket` pelo nome real do seu bucket S3 e `PedidosTable` pelo nome da sua tabela no DynamoDB. Não se esqueça de ajustar a `REGIAO` e o `ID_DA_CONTA` conforme sua configuração.

## Requisitos

- A função Lambda precisa ter as permissões corretas para acessar o S3 e inserir itens no DynamoDB.
- O arquivo `pedidos_lote01.json` deve ser colocado no bucket correto.
- Configure o evento de notificação do S3 para invocar a função Lambda ao enviar os arquivos `pedidos_lote02.json` e `pedidos_lote03.json`.

## Próximos Passos

1. Adicionar validação dos pedidos e tratamento de erros em versões futuras.
2. Evoluir a função para lidar com arquivos maiores e adicionar mais tratamentos de exceção.

## Contato

Para dúvidas ou sugestões, sinta-se à vontade para entrar em contato.

