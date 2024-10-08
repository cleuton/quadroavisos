import React, { useState, useEffect, useContext } from 'react';
import { useParams, useSearchParams, useLocation, Link, useNavigate } from 'react-router-dom';
import { UsuarioContext } from '../context/UsuarioContext';
import { formatarDataHora } from '../utils/funcoes';

function QuadroMensagens() {
  const { id } = useParams(); // Obtém o id do quadro da rota
  const location = useLocation();
  const [searchParams] = useSearchParams(); // Obtém os parâmetros de query string
  const { usuario } = useContext(UsuarioContext);
  const [mensagens, setMensagens] = useState([]);
  const [loading, setLoading] = useState(true);

  const [descricao, setDescricao] = useState(location.state?.descricao);
  const navigate = useNavigate();

  useEffect(() => {
    if (!descricao) {
      fetch(`/api/elementos/${id}`)
        .then((res) => res.json())
        .then((data) => setDescricao(data.descricao))
        .catch((error) => console.error(error));
    }
  }, [id, descricao]);



  // Obtém os parâmetros de query string com valores padrão
  const pagina = searchParams.get('pagina') || '1';
  const qtdemsg = searchParams.get('qtdemsg') || '10';

  useEffect(() => {
    fetch(`http://localhost:5000/mensagens/${id}?pagina=${pagina}&qtdemsg=${qtdemsg}`, {
      method: 'GET',
      headers: {
        'Authorization': `Bearer ${usuario.token}`,
      }
    })
    .then((response) => response.json())
    .then((data) => {
      setMensagens(data);
      setLoading(false);
    })
    .catch((error) => {
      console.error('Erro ao buscar mensagens:', error);
      setMensagens([]);
      setLoading(false);
    });
  }, [id, pagina, qtdemsg, usuario]);

  if (!descricao) {
    return <p>Carregando...</p>;
  }

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
    navigate('/mensagem/editar', { state: { adicionarOuEditarMensagem, index, mensagem: index !== null ? mensagens[index] : null } });
  };

  return (
    <div className="container">
      <button className="button-right" onClick={() => irParaEditarMensagem()}>Nova mensagem</button>
      <h1>Mensagens: {descricao}</h1>
      {loading ? (
        <p>Carregando...</p>
      ) : mensagens.length > 0 ? (
        mensagens.map((mensagem) => (
          <div key={mensagem.id} className="mensagem">
          {mensagem.icone ?
          <img src={`/images/${mensagem.icone}`} alt="Ícone" className="icone" />
          : <img src={`/images/normal.png`} alt="Ícone" className="icone" />} 
          <span className="data-hora">{formatarDataHora(mensagem.dataHora)}</span>
          <Link to={`/mensagem/${mensagem.id}`}><h3 className="titulo">{mensagem.titulo}</h3></Link>
          </div>

        ))
      ) : (
        <p>Nenhuma mensagem encontrada.</p>
      )}
    </div>
  );
}

export default QuadroMensagens;
