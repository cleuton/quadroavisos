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