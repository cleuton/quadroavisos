import React, { useContext } from 'react';
import {UsuarioContext} from '../context/UsuarioContext';

const Logout = () => {
  const { setUsuario } = useContext(UsuarioContext);

  const handleLogout = () => {
    setUsuario(null); // Limpa as informações do usuário
  };

  return <button onClick={handleLogout}>Sair</button>;
};

export default Logout;
