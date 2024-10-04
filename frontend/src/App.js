// App.js
import React, { useContext } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import './styles.css';
import Header from './components/Header';
import { UsuarioProvider, UsuarioContext } from './context/UsuarioContext';
import SignIn from './components/SignIn';
import Quadros from './components/Quadros';
import PrivateRoute from './components/PrivateRoute';
import QuadroMensagens from './components/QuadroMensagens';

function App() {
  return (
    <UsuarioProvider>
      <Router>
        <Header />
        <Main />
      </Router>
    </UsuarioProvider>
  );
}

function Main() {
  const { usuario } = useContext(UsuarioContext);

  return (
    <Routes>
      {/* Rota de login */}
      <Route
        path="/login"
        element={
          usuario ? <Navigate to="/quadros" replace /> : <SignIn />
        }
      />

      {/* Rotas protegidas */}
      <Route
        path="/quadros"
        element={
          <PrivateRoute>
            <Quadros />
          </PrivateRoute>
        }
      />
      {/* Rota para exibir as mensagens do quadro */}
      <Route
        path="/quadros/:id"
        element={
          <PrivateRoute>
            <QuadroMensagens />
          </PrivateRoute>
        }
      />      

      {/* Redirecionar para /quadros se estiver logado, senão para /login */}
      <Route
        path="/"
        element={
          usuario ? <Navigate to="/quadros" replace /> : <Navigate to="/login" replace />
        }
      />

      {/* Rota para páginas não encontradas */}
      <Route
        path="*"
        element={<h1>Página não encontrada</h1>}
      />
    </Routes>
  );
}

export default App;
