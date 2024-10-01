import React from "react";
import Logout from "./Logout";
import { UsuarioContext } from "../context/UsuarioContext";

export default function Header() {
    const { usuario } = React.useContext(UsuarioContext);
    return (
        <header>
            <nav className="navbar">
                <div className="navbar-left">
                    <img src="logo.png" alt="Ghost Company" className="logo" />
                </div>
                <div className="navbar-center">
                    <ul className="nav-links">
                        <li><a href="/">Início</a></li>
                        <li><a href="/perfil">Perfil</a></li>
                        <li><a href="/sistemas">Sistemas</a></li>
                    </ul>
                </div>
                <div className="navbar-right">
                    {usuario ? (
                        <div>
                            <span>Olá, </span>
                            <span>{usuario.nome}</span>
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
