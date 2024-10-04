// components/Logout.js
import React, { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { UsuarioContext } from '../context/UsuarioContext';

const Logout = () => {
  const { setUsuario } = useContext(UsuarioContext);
  const navigate = useNavigate();

  const handleLogout = () => {
    setUsuario(null); // Limpa as informações do usuário
    navigate('/login'); // Redireciona para a página de login
  };

  return <button onClick={handleLogout}>Sair</button>;
};

export default Logout;
