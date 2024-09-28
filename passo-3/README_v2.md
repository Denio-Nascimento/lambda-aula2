
# Projeto AWS Lambda: Processamento de Pedidos com Validação e Armazenamento no DynamoDB

Este projeto implementa uma função AWS Lambda que processa arquivos JSON com pedidos enviados para um bucket S3. O objetivo é validar e inserir os pedidos no DynamoDB, e, caso ocorram erros de validação, mover os pedidos incorretos para uma tabela separada de erros.

## Funcionalidades Principais

1. **Processamento de Pedidos**:
   - A função é ativada por eventos do S3 quando um arquivo JSON é carregado no bucket.
   - O arquivo JSON pode conter um único pedido ou uma lista de pedidos.
   - Todos os campos são validados e, em caso de erro, o pedido é movido para uma tabela de pedidos incorretos.

2. **Validação de Campos Obrigatórios**:
   - Os campos `customerName`, `customerEmail`, `totalAmount`, e `orderDate` são obrigatórios.
   - `totalAmount` deve ser um valor numérico válido.
   - `orderDate` deve ser uma data válida.
   - Se o campo `orderId` estiver ausente, o pedido será movido para a tabela de erros.

3. **Tratamento de Erros**:
   - Se qualquer campo obrigatório estiver ausente ou inválido, o pedido é armazenado na tabela `PedidosIncorretosTable`.
   - Erros de conversão de tipo (como `float` para `Decimal`) são tratados.
   - Se o pedido estiver correto, ele será inserido na tabela `PedidosTable`.

## Estrutura do Projeto

- `lambda_function.py`: Código principal da função Lambda.
- `README.md`: Este arquivo de documentação.
- Arquivos JSON de exemplo para teste: `pedidos_lote_erro-01.json`, `pedidos_lote01.json`, etc.

## Fluxo de Execução

1. **Recebimento do evento S3**: 
   - A Lambda é invocada sempre que um arquivo é enviado para o bucket S3 configurado.
   
2. **Processamento do arquivo JSON**:
   - O conteúdo do arquivo é lido e analisado. Se o arquivo estiver mal formatado, um erro de formato JSON é retornado.
   
3. **Validação dos pedidos**:
   - Cada pedido é validado. Caso algum campo obrigatório esteja ausente ou inválido, o pedido é movido para a tabela `PedidosIncorretosTable`.
   
4. **Armazenamento**:
   - Pedidos válidos são inseridos na tabela `PedidosTable`. Pedidos inválidos são inseridos na tabela `PedidosIncorretosTable`.

## Estrutura das Tabelas no DynamoDB

### Tabela `PedidosTable`

| Nome do Campo | Tipo        | Descrição                |
|---------------|-------------|--------------------------|
| `orderId`     | String      | ID do pedido (PK)         |
| `customerName`| String      | Nome do cliente           |
| `customerEmail`| String     | Email do cliente          |
| `totalAmount` | Decimal     | Valor total do pedido     |
| `orderDate`   | String      | Data do pedido            |
| `status`      | String      | Status do pedido          |

### Tabela `PedidosIncorretosTable`

| Nome do Campo  | Tipo        | Descrição                            |
|----------------|-------------|--------------------------------------|
| `orderId`      | String      | ID do pedido (pode ser gerado) (PK)  |
| `errorTimestamp`| String     | Timestamp do erro                    |
| `bucketName`   | String      | Nome do bucket de origem             |
| `fileName`     | String      | Nome do arquivo processado           |
| `orderData`    | Map         | Dados do pedido com erros            |
| `errorReason`  | String      | Motivo do erro                       |

## Exemplo de JSON de Pedido

```json
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
  }
]
```

## Como Testar

1. Crie as tabelas no DynamoDB (`PedidosTable` e `PedidosIncorretosTable`).
2. Suba a função Lambda com o código fornecido no arquivo `lambda_function.py`.
3. Configure um gatilho no S3 para invocar a Lambda quando arquivos forem enviados ao bucket.
4. Teste fazendo upload de arquivos JSON com pedidos para o bucket S3.
5. Verifique os logs no CloudWatch e os dados inseridos no DynamoDB.

## Permissões Necessárias

A Lambda deve ter permissões para:
- `s3:GetObject`
- `dynamodb:PutItem`
- `logs:CreateLogGroup`, `logs:CreateLogStream`, e `logs:PutLogEvents` (para logging no CloudWatch)

Exemplo de política IAM:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:ListBucket",
                "dynamodb:PutItem",
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": [
                "arn:aws:s3:::nome-do-bucket/*",
                "arn:aws:dynamodb:REGIAO:ID_DA_CONTA:table/PedidosTable",
                "arn:aws:dynamodb:REGIAO:ID_DA_CONTA:table/PedidosIncorretosTable",
                "arn:aws:logs:REGIAO:ID_DA_CONTA:*"
            ]
        }
    ]
}
```

## Contato

Caso tenha dúvidas ou sugestões, entre em contato.
