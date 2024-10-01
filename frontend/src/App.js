import logo from './logo.svg';
import './styles.css';
import Header from './components/Header';
import { UsuarioProvider, UsuarioContext } from './context/UsuarioContext';
import SignIn from './components/SignIn';
import React, {useContext} from 'react';

function App() {
  const { usuario } = useContext(UsuarioContext);
  return (
    <div className="App">
      <Header />
      {!usuario && 
        <SignIn />}
    </div>
  );
}

export default App;
