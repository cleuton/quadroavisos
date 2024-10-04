// components/PrivateRoute.js
import React, { useContext } from 'react';
import { Navigate } from 'react-router-dom';
import { UsuarioContext } from '../context/UsuarioContext';

const PrivateRoute = ({ children }) => {
  const { usuario } = useContext(UsuarioContext);

  if (!usuario) {
    return <Navigate to="/login" replace />;
  }

  return children;
};

export default PrivateRoute;
