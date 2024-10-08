// components/PrivateRoute.js
import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { UsuarioContext } from '../context/UsuarioContext';
import {jwtDecode} from 'jwt-decode';

const PrivateRoute = ({ children }) => {
  const { usuario } = useContext(UsuarioContext);
  const { setUsuario } = useContext(UsuarioContext);

  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  // Função para verificar se o token expirou
  const isTokenExpired = (token) => {
    try {
      const { exp } = jwtDecode(token);
      const now = Date.now() / 1000; // Em segundos
      return exp < now;
    } catch (error) {
      console.error("Erro ao verificar o token:", error);
      return true; // Se houver erro ao decodificar, considere o token inválido
    }
  };

  // Verifica se o token está expirado
  if (usuario.token && isTokenExpired(usuario.token)) {
    setUsuario(null); // Limpa as informações do usuário
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default PrivateRoute;
