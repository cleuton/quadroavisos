import logo from './logo.svg';
import './styles.css';
import React, {useContext} from 'react';
import Header from './components/Header';
import { UsuarioProvider, UsuarioContext } from './context/UsuarioContext';
import SignIn from './components/SignIn';
import Quadros from './components/Quadros';

function App() {
  const { usuario } = useContext(UsuarioContext);
  return (
    <div className="App">
      <Header />
      {!usuario && 
        <SignIn />}
      {usuario && <Quadros />}
    </div>
  );
}

export default App;
