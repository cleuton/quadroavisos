import React, { useState, useContext } from 'react';
import {UsuarioContext} from '../context/UsuarioContext';

const SignIn = () => {
  const { setUsuario } = useContext(UsuarioContext);
  const [email, setEmail] = useState('');
  const [senha, setSenha] = useState('');
  const [erro, setErro] = useState('');
  
  const handleSubmit = (e) => {
    e.preventDefault();
    fetch('http://localhost:5000/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ email, senha }),
    })
      .then((resposta) => {
        if (resposta.ok) {
          return resposta.json();
        } else {
          return resposta.json().then((erroDados) => {
            throw new Error(erroDados.message || 'Erro ao fazer login.');
          });
        }
      })
      .then((dados) => {
        const token = dados.token;
        // Armazenar o token e atualizar o contexto
        setUsuario({ "id": dados.id, "nome": dados.nome, "admin": dados.admin, "token": token });
      })
      .catch((erro) => {
        console.error('Erro na requisição:', erro);
        setErro(erro.message || 'Erro na conexão com o servidor.');
      });
  };

  return (
    <div className="signin">
      <h2>Entrar</h2>
      {erro && <p style={{ color: 'red' }}>{erro}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Email:</label>
          <input
            type="text"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Senha:</label>
          <input
            type="password"
            value={senha}
            onChange={(e) => setSenha(e.target.value)}
            required
          />
        </div>
        <button type="submit">Entrar</button>
      </form>
    </div>
  );
};

export default SignIn;
