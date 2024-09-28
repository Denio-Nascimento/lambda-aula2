# Projeto Pedidos: Processamento de Pedidos e Geração de URLs Pré-assinadas

Este projeto implementa um fluxo de processamento de pedidos utilizando **AWS Lambda**, **S3**, **DynamoDB**, **DynamoDB Streams** e **SNS**. Ele é dividido em duas partes principais:

## 1. Processamento e Validação de Pedidos

A primeira função **AWS Lambda** é acionada quando arquivos JSON contendo pedidos são enviados para um bucket **S3**. A função realiza a validação dos pedidos e, conforme o resultado da validação:

- Se o pedido for válido, ele é inserido em uma tabela **DynamoDB**.
- Se o pedido contiver erros (como campos obrigatórios ausentes ou dados incorretos), ele é movido para uma **tabela separada de erros** no DynamoDB. Isso permite um tratamento posterior desses pedidos incorretos.

### Validações realizadas:
- Verificação de campos obrigatórios como `customerName`, `totalAmount`, `orderDate`, etc.
- Geração de um `orderId` aleatório se o pedido não o possuir.
- Armazenamento de pedidos válidos e incorretos em tabelas DynamoDB distintas.

### Objetivo:
Este fluxo automatiza a inserção e a validação de pedidos, além de permitir o tratamento e monitoramento de pedidos incorretos.

## 2. Geração de URLs Pré-assinadas e Notificações

A segunda função **AWS Lambda** é acionada por eventos do **DynamoDB Streams** quando um novo item é inserido na **tabela de erros** no DynamoDB. A função realiza as seguintes tarefas:

- **Gera uma URL pré-assinada** para o arquivo JSON do pedido armazenado no **S3**, permitindo o acesso temporário ao arquivo.
- **Envia uma notificação** com a URL pré-assinada e os detalhes do pedido incorreto para um tópico **SNS**, permitindo que outros sistemas recebam informações para corrigir os erros.

### Fluxo de Trabalho:
1. Um novo item com erro é inserido na tabela de erros do DynamoDB.
2. A Lambda é invocada pelo **DynamoDB Streams**.
3. A função gera uma URL pré-assinada para o arquivo no S3.
4. A função envia os detalhes do pedido e a URL para um tópico SNS, notificando sistemas externos.

## Tecnologias Utilizadas

- **AWS Lambda**: Para processar os pedidos e gerar as URLs pré-assinadas.
- **Amazon S3**: Para armazenar os arquivos JSON contendo os pedidos.
- **Amazon DynamoDB**: Para armazenar os pedidos válidos e os pedidos com erros em tabelas separadas.
- **DynamoDB Streams**: Para invocar a Lambda sempre que um pedido incorreto for inserido na tabela de erros.
- **Amazon SNS**: Para enviar notificações com os detalhes dos pedidos incorretos e as URLs pré-assinadas.

## Configurações Necessárias

1. **Bucket S3**: Onde os arquivos de pedidos JSON serão armazenados.
2. **Tabelas DynamoDB**: 
   - Uma para pedidos válidos.
   - Uma para pedidos incorretos.
3. **DynamoDB Streams**: Ativado na tabela de erros para disparar a segunda função Lambda.
4. **Tópico SNS**: Para receber notificações de pedidos incorretos.

### Permissões

- As funções Lambda precisam das seguintes permissões:
  - **S3**: `s3:GetObject` para gerar as URLs pré-assinadas.
  - **DynamoDB**: `dynamodb:PutItem` para inserir pedidos nas tabelas e `dynamodb:StreamRead` para ler eventos do stream.
  - **SNS**: `sns:Publish` para enviar notificações.
  - **CloudWatch Logs**: Para registrar logs de execução.

## Execução

1. Enviar um arquivo JSON de pedido para o bucket S3.
2. A função Lambda processará e validará o pedido.
3. Pedidos válidos serão armazenados na tabela DynamoDB, e pedidos incorretos serão movidos para a tabela de erros.
4. Se um pedido incorreto for armazenado na tabela de erros, a segunda função Lambda será invocada pelo DynamoDB Stream, gerando a URL pré-assinada e enviando uma notificação para o SNS.

## Contribuição

Contribuições são bem-vindas! Sinta-se à vontade para abrir issues ou enviar pull requests.
