import React, { useState, useEffect, useRef, useContext } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';
import { UsuarioContext } from "../context/UsuarioContext";

export default function EditarQuadro() {
  const nomeInputRef = useRef(null);
  const location = useLocation();
  const navigate = useNavigate();
  var { index, quadro_atual } = location.state;
  const { usuario } = useContext(UsuarioContext);
  const [erro, setErro] = useState("");

  if (!quadro_atual) {
      quadro_atual = {id: 0, nome: "", descricao: "", dono: 0, publico: false, qtde_mensagens: 0};
  }
  const [quadro, setQuadro] = useState(quadro_atual);

  useEffect(() => {
    if (nomeInputRef.current) {
      nomeInputRef.current.focus();
    }
  }, []);


  const salvarQuadro = () => {
    if (quadro.id !== 0) {
      // está editando um quadro já existente
      quadro.dono = usuario.id;
      fetch(`http://localhost:5000/quadros/${quadro.id}`, {
        method: "PUT",
        headers: { 
          "Content-Type": "application/json",
          'Authorization': `Bearer ${usuario.token}`
        },
        body: JSON.stringify({
          id: quadro.id,
          nome: quadro.nome,
          descricao: quadro.descricao,
          dono: quadro.dono,
          publico: quadro.publico,
        }),
      })
      .then((response) => {
        if (response.ok) {
          navigate("/quadros", { state: { index, novoQuadro: quadro } });
        }
      })
      .catch((error) => {
        console.error("Erro ao atualizar quadro: ", error);
        setErro(error.message || 'Erro na conexão com o servidor.');
      });
    } else {
      // está adicionando um novo quadro
      // Gravar o novo quadro no backend
      quadro.dono = usuario.id;
      fetch(`http://localhost:5000/quadros`, {
        method: "POST",
        headers: { 
          "Content-Type": "application/json",
          'Authorization': `Bearer ${usuario.token}`
        },
        body: JSON.stringify(quadro),
      })
      .then((response) => {
        if (response.ok) {
          return response.json();
        }
        throw response;
      })
      .then((resposta) => {
        quadro.id = resposta.idQuadro;
        setQuadro(quadro);
        // Navegar de volta para Quadros com o novo quadro como state
        navigate("/quadros", { state: { index, novoQuadro: quadro } });

      })
      .catch((error) => {
        console.error("Erro ao salvar quadro: ", error);
        setErro(error.message || 'Erro na conexão com o servidor.');
      });
    }
  };

  // Função para atualizar o estado do quadro dinamicamente com base no campo
  const handleChange = (e) => {
    const { name, value } = e.target;
    setQuadro((prevQuadro) => ({
      ...prevQuadro,
      [name]: value,
    }));
  };


  return (
    <div className="form-center">
      <h1>{index !== null ? "Editar Quadro" : "Adicionar Novo Quadro"}</h1>
      {erro && <p style={{ color: 'red' }}>{erro}</p>}
      <form className="form-quadro" onSubmit={(e) => { e.preventDefault(); salvarQuadro(); }}>
        <div>
          <label htmlFor="nome">Nome do Quadro:</label>
          <input
            type="text"
            id="nome"
            name="nome"
            ref={nomeInputRef}
            value={quadro.nome}
            onChange={handleChange}
            placeholder="Digite o nome do quadro"
            required
          />
        </div>
        
        <div>
          <label htmlFor="descricao">Descrição do Quadro:</label>
          <textarea
            id="descricao"
            name="descricao"
            value={quadro.descricao}
            onChange={handleChange}
            placeholder="Digite a descrição do quadro"
            required
          />
        </div>

        <button type="submit">
          {index !== null ? "Salvar" : "Adicionar"}
        </button>
        <button className="cancel" onClick={() => navigate("/quadros", {state: null})}>
          Cancelar
        </button>        
      </form>
    </div>
  );
}