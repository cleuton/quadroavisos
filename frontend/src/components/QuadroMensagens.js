import React, { useState, useEffect, useContext } from 'react';
import { useParams, useSearchParams } from 'react-router-dom';
import { UsuarioContext } from '../context/UsuarioContext';

function QuadroMensagens() {
  const { id } = useParams(); // Obtém o id do quadro da rota
  const [searchParams] = useSearchParams(); // Obtém os parâmetros de query string
  const { usuario } = useContext(UsuarioContext);
  const [mensagens, setMensagens] = useState([]);
  const [loading, setLoading] = useState(true);

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

  return (
    <div className="container">
      <h1>Mensagens do Quadro {id}</h1>
      {loading ? (
        <p>Carregando...</p>
      ) : mensagens.length > 0 ? (
        mensagens.map((mensagem) => (
          <div key={mensagem.id}>
            {/* Renderize o conteúdo da mensagem conforme necessário */}
            <p>{mensagem.texto}</p>
          </div>
        ))
      ) : (
        <p>Nenhuma mensagem encontrada.</p>
      )}
    </div>
  );
}

export default QuadroMensagens;
