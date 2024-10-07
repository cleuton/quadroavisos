import React, { useState, useEffect, useContext }  from "react";
import { useParams } from 'react-router-dom';
import { formatarDataHora } from '../utils/funcoes';
import { UsuarioContext } from '../context/UsuarioContext';

const fetchImage = async (setImageSrc, id, token) => {
    try {
      const response = await fetch(`http://localhost:5000/mensagem/${id}/anexo`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
  
      if (!response.ok) {
        throw new Error(`Erro ao buscar a imagem: ${response.statusText}`);
      }
  
      const blob = await response.blob();  // Certifique-se de usar await aqui
      console.log('Blob:', blob);  // Verifica se o blob está sendo gerado corretamente
  
      const imageUrl = URL.createObjectURL(blob);
      setImageSrc(imageUrl);  // Aqui o URL temporário é gerado corretamente
    } catch (error) {
      console.error('Erro ao buscar anexo:', error);
    }
  };

export default function Mensagem() {
    const { id } = useParams(); // Obtém o id do quadro da rota
    const [ mensagem, setMensagem ] = useState(null);
    const { usuario } = useContext(UsuarioContext);
    const [imageSrc, setImageSrc] = useState(null);

    useEffect(() => {   
        fetch(`http://localhost:5000/mensagem/${id}`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${usuario.token}`, 
            }})
        .then((response) => response.json())
        .then((data) => {
            setMensagem(data);
            if (data.mensagem.anexo) {
                fetchImage(setImageSrc, id, usuario.token);
            }})
    }, [id, usuario.token, setMensagem]);

    if (!mensagem) {
        return <p>Carregando...</p>;
    }

    return (
        <div className="container">
            <div key={mensagem.mensagem.id} className="mensagem">
            {mensagem.mensagem.icone ? (
                <img src={`/images/${mensagem.mensagem.icone}`} alt="Ícone" className="icone" />
            ) : (
                <img src={`/images/normal.png`} alt="Ícone" className="icone" />
            )}
            <span className="data-hora">{formatarDataHora(mensagem.mensagem.dataHora)}</span>
            <h3 className="titulo">{mensagem.mensagem.titulo}</h3>
            <p>Autor:</p><p>{mensagem.mensagem.nomeUsuario}</p>
            <p>{mensagem.mensagem.texto}</p>
            {mensagem.mensagem.anexo && <img src={imageSrc} alt="Imagem" />}
            </div>
        </div>
    );
}