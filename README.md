# Quadro de avisos

É uma aplicação exemplo de backend **Python** muito simples. A intenção é demonstrar como criar uma aplicação simples, porém completa, com: Banco de dados, autenticação e segurança, que pode até ser utilizada em Produção.

## Caso de uso: Acesso inicial sem login

Ao fazer um request para o raiz da aplicação, a rota `/api/quadro` é invocada e lista os quadros de mensagens públicos, com a última mensagen postada em cada um. 

É só isso que aparece quando o usuário não fez login. O resumo do quadro e alguns dados da última mensagem. E não há links. Não há como selecionar um quadro específico sem fazer login.

Ao selecionar um **quadro** público, suas mensagens são listadas em ordem decrescente. A listagem de mensagens é: ícone, data, título com link. Ao clicar no link, os dados completos da mensagem são retornados.

- Rota para selecionar um quadro específico: `/api/quadro`. São listadas as **20** últimas mensagens. O usuário pode paginar com as querystrings: `start` e `offset`: `/api/quadro/12?start=50&offset=20`.

- Rota para selecionar uma mensagem: `/api/mensagem/id`.

Para acessar os quadros privados, é necessário fazer **login**.

## Caso de uso: Login

O **frontend** faz um request para `/api/login` passando seu **email** e a **senha** e vê a lista de quadros privados e públicos aos quais ele tem acesso, cada um com o título da última mensagem postada. Para que um quadro apareça para o usuário, ele tem que ser membro APROVADO do quadro (só o dono do quadro pode aprovar). Caso ele seja administrador do site, ele vê todos os quadros, independentemente de ser membro, dono ou de ter sido aprovado.

Ao selecionar um **quadro**, suas mensagens são listadas em ordem decrescente. A listagem de mensagens é: ícone, data, título com link. Ao clicar no link, os dados completos da mensagem são retornados, inclusive as reações (e a última reação do usuário, que ele pode mudar).

- Rota para selecionar um quadro específico: `/api/quadro`. São listadas as **20** últimas mensagens. O usuário pode paginar com as querystrings: `start` e `offset`: `/api/quadro/12?start=50&offset=20`.

- Rota para selecionar uma mensagem: `/api/mensagem/id`. 

- Pendências: 
    3) Adicionar reação à mensagem

O comportamento de selecionar um quadro ou uma mensagem é igual ao "Acesso inicial".

