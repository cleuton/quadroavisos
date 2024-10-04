// components/Header.js
import React from 'react';
import { Link } from 'react-router-dom';
import Logout from './Logout';
import { UsuarioContext } from '../context/UsuarioContext';

export default function Header() {
  const { usuario } = React.useContext(UsuarioContext);
  return (
    <header>
      <nav className="navbar">
        <div className="navbar-left">
          <Link to="/">
            <img src="logo.png" alt="Ghost Company" className="logo" />
          </Link>
        </div>
        <div className="navbar-center">
          <ul className="nav-links">
            <li>
              <Link to="/">Início</Link>
            </li>
            <li>
              <Link to="/perfil">Perfil</Link>
            </li>
            <li>
              <Link to="/sistemas">Sistemas</Link>
            </li>
          </ul>
        </div>
        <div className="navbar-right">
          {usuario ? (
            <div>
              <span>Olá, </span>
              <span>{usuario.nome}&nbsp;</span>
              {usuario.admin && <span className="dot"></span>}
              &nbsp;
              <Logout />
            </div>
          ) : (
            <span>Não autenticado</span>
          )}
        </div>
      </nav>
    </header>
  );
}
