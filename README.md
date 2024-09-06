# Quadro de avisos

É uma aplicação exemplo de backend **Python** muito simples. A intenção é demonstrar como criar uma aplicação simples, porém completa, com: Banco de dados, autenticação e segurança, que pode até ser utilizada em Produção.

## Caso de uso: Acesso inicial sem login

Ao fazer um request para o raiz da aplicação, a rota `/api/quadro` é invocada e lista os quadros de mensagens públicos, com a última mensagen postada em cada um. 

Ao selecionar um **quadro** público, suas mensagens são listadas em ordem decrescente. A listagem de mensagens é: ícone, data, título com link. Ao clicar no link, os dados completos da mensagem são retornados.

- Rota para selecionar um quadro específico: `/api/quadro`. São listadas as **20** últimas mensagens. O usuário pode paginar com as querystrings: `start` e `offset`: `/api/quadro/12?start=50&offset=20`.

- Rota para selecionar uma mensagem: `/api/mensagem/id`.

Para acessar os quadros privados, é necessário fazer **login**.

## Caso de uso: Login

O **frontend** faz um request para `/api/login` passando seu **email** e a **senha** e vê a lista de quadros privados e públicos aos quais ele tem acesso, cada um com o título da última mensagem postada.

O comportamento de selecionar um quadro ou uma mensagem é igual ao "Acesso inicial".

- Pendências do db_quadros e db_mensagens: Ao acessar a lista de quadros, cada um tem que trazer a última mensagem. Não precisa ser completa. Só data, ícone e título. 
