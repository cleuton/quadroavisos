import React, { useState, useEffect } from 'react';

const UsuarioContext = React.createContext();

const UsuarioProvider = ({ children }) => {
  // Estado inicial do usuário, pode ser null ou um objeto vazio
  const [usuario, setUsuario] = useState(null);

  // Opcional: persistir o estado do usuário usando localStorage
  useEffect(() => {
    const usuarioArmazenado = localStorage.getItem('usuario');
    if (usuarioArmazenado) {
      setUsuario(JSON.parse(usuarioArmazenado));
    }
  }, []);

  // Atualizar o localStorage sempre que o usuário mudar
  useEffect(() => {
    if (usuario) {
      localStorage.setItem('usuario', JSON.stringify(usuario));
    } else {
      localStorage.removeItem('usuario');
    }
  }, [usuario]);

  return (
    <UsuarioContext.Provider value={{ usuario, setUsuario }}>
      {children}
    </UsuarioContext.Provider>
  );
};

export { UsuarioContext, UsuarioProvider };

