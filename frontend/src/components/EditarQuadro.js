import React, { useState, useEffect, useRef } from 'react';
import { useLocation, useNavigate } from 'react-router-dom';


export default function EditarQuadro() {
  const nomeInputRef = useRef(null);
  const location = useLocation();
  const navigate = useNavigate();
  var { index, quadro_atual } = location.state;

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
    // O backend tem que retornar o id do novo quadro e nós temos que atualizar o quadro com esse id *******
    setQuadro(quadro);
    // Navegar de volta para Quadros com o novo quadro como state
    navigate("/quadros", { state: { index, novoQuadro: quadro } });
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

        <button type="submit" onClick={salvarQuadro}>
          {index !== null ? "Salvar" : "Adicionar"}
        </button>
        <button className="cancel" onClick={() => navigate("/quadros", {state: null})}>
          Cancelar
        </button>        
      </form>
    </div>
  );
}