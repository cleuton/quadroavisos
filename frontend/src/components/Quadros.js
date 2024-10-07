import React, {useState, useContext, useEffect} from "react";
import { UsuarioContext } from "../context/UsuarioContext";
import { Link } from 'react-router-dom';
import { formatarDataHora } from '../utils/funcoes';

export default function Quadros() {
    const [quadros, setQuadros] = useState([]);
    const { usuario } = useContext(UsuarioContext);
    
    useEffect(() => {
        fetch(`http://localhost:5000/quadros`, {
            method: 'GET',
            headers: {
              'Authorization': `Bearer ${usuario.token}`, 
            }})
        .then((response) => response.json())
        .then((data) => setQuadros(data));
    }, [usuario]);
    
    return (
        <div className="container">
        <h1>Quadros</h1>
        {quadros.map((quadro) => (
            <div key={quadro.id}>
                <Link to={`/quadros/${quadro.id}?pagina=1&qtdemsg=10`} state={{ descricao: quadro.descricao}}>
                    <h2 className="descricao">{quadro.descricao}</h2>
                </Link>
                {quadro.titulo ?                   
                <div className="mensagem">
                    {quadro.icone ?
                    <img src={`/images/${quadro.icone}`} alt="Ícone" className="icone" />
                    : <img src={`/images/${quadro.normal}`} alt="Ícone" className="icone" />} 
                    <span className="data-hora">{formatarDataHora(quadro.dataHora)}</span>
                    <h3 className="titulo">{quadro.titulo}</h3>
                </div>
                : <p>Nenhuma mensagem cadastrada</p>}
            </div>
        ))}
        {quadros && quadros.length === 0 && <p>Nenhum quadro cadastrado</p>}
        </div>
    );
}