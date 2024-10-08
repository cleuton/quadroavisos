Agora entendi melhor o que você precisa. Vou mostrar como fazer a navegação entre os componentes `QuadroMensagens` e `EditarMensagem` usando o `react-router-dom` e garantindo que, ao voltar para o `QuadroMensagens`, a lista de mensagens seja atualizada corretamente.

### Cenário:
- **QuadroMensagens**: Exibe uma lista de mensagens.
- **EditarMensagem**: Permite criar ou editar uma mensagem.
- Após editar ou criar uma nova mensagem no `EditarMensagem`, o usuário é redirecionado de volta para o `QuadroMensagens`, e o estado (lista de mensagens) é atualizado.

A melhor maneira de implementar isso é manter o estado no `QuadroMensagens` e passar uma função de callback para o `EditarMensagem` que será responsável por atualizar o estado quando uma nova mensagem for adicionada ou editada.

### 1. **Estado em `QuadroMensagens` e navegação**

No `QuadroMensagens`, você pode manter o estado das mensagens e, ao clicar para editar ou adicionar, navegar para o `EditarMensagem`, passando a função de atualização de mensagens via `state`.

#### `QuadroMensagens.js`

```jsx
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

function QuadroMensagens() {
  const [mensagens, setMensagens] = useState(["Mensagem 1", "Mensagem 2"]);
  const navigate = useNavigate();

  const adicionarOuEditarMensagem = (novaMensagem, index = null) => {
    if (index !== null) {
      // Editando uma mensagem existente
      const mensagensAtualizadas = [...mensagens];
      mensagensAtualizadas[index] = novaMensagem;
      setMensagens(mensagensAtualizadas);
    } else {
      // Adicionando uma nova mensagem
      setMensagens([...mensagens, novaMensagem]);
    }
  };

  const irParaEditarMensagem = (index = null) => {
    navigate('/editar', { state: { adicionarOuEditarMensagem, index, mensagem: index !== null ? mensagens[index] : "" } });
  };

  return (
    <div>
      <h1>Quadro de Mensagens</h1>
      <ul>
        {mensagens.map((msg, index) => (
          <li key={index}>
            {msg} <button onClick={() => irParaEditarMensagem(index)}>Editar</button>
          </li>
        ))}
      </ul>
      <button onClick={() => irParaEditarMensagem()}>Adicionar Nova Mensagem</button>
    </div>
  );
}

export default QuadroMensagens;
```

### 2. **Recebendo o estado no `EditarMensagem`**

O `EditarMensagem` receberá a função `adicionarOuEditarMensagem` via `state` do `navigate`, permitindo que ele adicione ou edite uma mensagem. Após o envio, ele chamará essa função e redirecionará de volta ao `QuadroMensagens`.

#### `EditarMensagem.js`

```jsx
import React, { useState } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';

function EditarMensagem() {
  const location = useLocation();
  const { adicionarOuEditarMensagem, index, mensagem } = location.state;
  const [textoMensagem, setTextoMensagem] = useState(mensagem || "");
  const navigate = useNavigate();

  const salvarMensagem = () => {
    adicionarOuEditarMensagem(textoMensagem, index);
    navigate('/'); // Retorna para QuadroMensagens após salvar
  };

  return (
    <div>
      <h1>{index !== null ? "Editar Mensagem" : "Adicionar Nova Mensagem"}</h1>
      <textarea
        value={textoMensagem}
        onChange={(e) => setTextoMensagem(e.target.value)}
      />
      <button onClick={salvarMensagem}>{index !== null ? "Salvar" : "Adicionar"}</button>
    </div>
  );
}

export default EditarMensagem;
```

### 3. **Configuração das rotas no `App.js`**

Agora configure as rotas para o `QuadroMensagens` e `EditarMensagem` no `App.js` usando o `react-router-dom`.

#### `App.js`

```jsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import QuadroMensagens from './QuadroMensagens';
import EditarMensagem from './EditarMensagem';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<QuadroMensagens />} />
        <Route path="/editar" element={<EditarMensagem />} />
      </Routes>
    </Router>
  );
}

export default App;
```

### Como Funciona:
1. No `QuadroMensagens`, você mantém o estado das mensagens e fornece a função `adicionarOuEditarMensagem` que pode ser chamada ao criar ou editar uma mensagem.
2. Quando o usuário clica para editar ou adicionar uma nova mensagem, o `navigate` leva o usuário para o `EditarMensagem`, passando essa função via `state`.
3. No `EditarMensagem`, você usa a função passada para salvar ou editar a mensagem e, depois, retorna ao `QuadroMensagens` com o estado atualizado.

Essa abordagem mantém a navegação entre os componentes simples e permite a atualização de estado sem a necessidade de um estado global ou uma solução mais complexa.