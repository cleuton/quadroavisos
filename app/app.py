from datetime import timedelta

from flask import Flask
from flask_jwt_extended import JWTManager
from web.login import auth_blueprint
from web.quadros import quadros_blueprint
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

# Configuração da chave secreta para o JWT
app.config['JWT_SECRET_KEY'] = 'minha_chave_secreta'  # Substitua pela sua chave secreta
# Definindo o tempo de expiração padrão
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(minutes=120)  # Tokens de acesso expiram em 30 minutos

# Inicializa o JWTManager
jwt = JWTManager(app)

# Registro dos blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(quadros_blueprint)

if __name__ == '__main__':
    app.run(debug=True)
