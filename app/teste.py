from database.db_usuario import validar_usuario, obter_usuario

if __name__=="__main__":
    email = 'carlos@example.com'
    password = 'senha789'
    
    usuario = validar_usuario(email, password)

    if usuario:
        print(f"Usuário OK. Nome: {usuario.nome}, Data de Nascimento: {usuario.dataNascimento}")
    else:
        print("*** Usuário não encontrado!")

    usuario2 = obter_usuario(usuario.id)

    if usuario2:
        print(f"Usuário por ID OK. Nome: {usuario.nome}, Data de Nascimento: {usuario.dataNascimento}")
    else:
        print("*** Usuário não encontrado!")
