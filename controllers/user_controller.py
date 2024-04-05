# user_controller.py

from flask import jsonify, request
from Model.user_model import User
from services.auth_service import gerar_token, verificar_credenciais

def login():
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
        return jsonify({'mensagem': 'Por favor, forneça o nome de usuário e senha'}), 400

    if verificar_credenciais(username, password):
        token = gerar_token(username)
        return jsonify({'token': token}), 200
    else:
        return jsonify({'mensagem': 'Credenciais inválidas'}), 401
