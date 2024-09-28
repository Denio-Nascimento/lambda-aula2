
***
# Teste de Validação: AWS Lambda com Pedidos com Erros

Este teste foi projetado para validar a função AWS Lambda que processa arquivos JSON com pedidos e realiza o tratamento de erros. O arquivo de teste contém cinco pedidos, cada um com um erro diferente, permitindo verificar se a Lambda lida corretamente com a validação e armazenamento de pedidos incorretos.

## Estrutura do Projeto

- **lambda_function.py**: Arquivo contendo o código da função Lambda.
- **README.md**: Este documento com a explicação e instruções para o teste.
- **pedidos_com_erros.json**: Arquivo JSON com cinco pedidos, cada um contendo um erro diferente.

## Arquivo de Teste: pedidos_com_erros.json

O arquivo `pedidos_com_erros.json` contém os seguintes pedidos, cada um com um erro específico para validar o tratamento de erros:

```json
[
  {
    "orderId": "100015",
    "customerName": "Paula Fernandes",
    "totalAmount": 340.00,
    "status": "Concluído",
    "orderDate": "2024-09-16T10:30:00Z"
    // Erro: Campo 'customerEmail' ausente
  },
  {
    "orderId": "100016",
    "customerName": "Carlos Lima",
    "customerEmail": "carlos.lima@email.com",
    "totalAmount": "invalid",  // Erro: Valor 'totalAmount' inválido (não numérico)
    "status": "Pendente",
    "orderDate": "2024-09-16T09:15:00Z"
  },
  {
    "orderId": "100017",
    "customerName": "Ana Pereira",
    "customerEmail": "ana.pereira@email.com",
    "totalAmount": 90.25,
    "status": "Pendente",
    "orderDate": "invalid-date"  // Erro: 'orderDate' com formato inválido
  },
  {
    "orderId": "100018",
    "customerName": "",  // Erro: 'customerName' está vazio
    "customerEmail": "jose.santos@email.com",
    "totalAmount": 45.50,
    "status": "Pendente",
    "orderDate": "2024-09-16T10:00:00Z"
  },
  {
    "customerName": "João Silva",
    "customerEmail": "joao.silva@email.com",
    "totalAmount": 120.75,
    "status": "Pendente",
    "orderDate": "2024-09-16T08:30:00Z"
    // Erro: Campo 'orderId' ausente (deverá ser gerado automaticamente)
  }
]
```

## Passos para o Teste

### 1. Upload do Arquivo JSON no S3
- Salve o conteúdo acima como `pedidos_com_erros.json`.
- Faça o upload do arquivo para o bucket S3 configurado para acionar a função Lambda.

### 2. Verificação do Processamento
- A função Lambda será invocada automaticamente pelo evento S3.
- A função Lambda irá processar os pedidos e aplicar validações.
  - **Pedidos válidos** serão inseridos na tabela DynamoDB `PedidosTable`.
  - **Pedidos com erros** serão armazenados na tabela `PedidosIncorretosTable` junto com o motivo do erro.

### 3. Verificação dos Logs
- Acesse os logs da função Lambda no **CloudWatch** para verificar como os pedidos foram processados.
- Mensagens de erro serão exibidas no formato:
  ```bash
  Pedido 100015 armazenado em PedidosIncorretosTable com erro: Campo ausente: customerEmail
  ```

### 4. Verificação nas Tabelas DynamoDB
- Acesse a tabela `PedidosTable` no DynamoDB para verificar se algum pedido foi armazenado corretamente.
- Verifique a tabela `PedidosIncorretosTable` para ver os pedidos com erros e o motivo de cada erro.

## Erros Simulados

1. **Pedido 100015**: Falta o campo `customerEmail`.
2. **Pedido 100016**: Valor inválido no campo `totalAmount`.
3. **Pedido 100017**: Data inválida no campo `orderDate`.
4. **Pedido 100018**: Nome do cliente (`customerName`) está vazio.
5. **Pedido sem `orderId`**: O campo `orderId` está ausente e deverá ser gerado automaticamente.

## Conclusão

Este teste foi desenvolvido para garantir que a função Lambda processe e valide corretamente os pedidos, armazenando aqueles com erros na tabela apropriada para análise e correção. Verifique tanto os logs no CloudWatch quanto os dados armazenados nas tabelas DynamoDB para validar o funcionamento da função.
***
