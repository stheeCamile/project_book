import jwt
import datetime
import mysql.connector
from flask import request, abort, current_app
from functools import wraps
import secrets

from config.config import db_config
from Model.user_model import User

SECRET_KEY = secrets.token_hex(32)

def gerar_token(usuario):
    payload = {
        'usuario': usuario,
        'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)  # Token expira em 1 hora
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
    return token

def verificar_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return payload['usuario']
    except jwt.ExpiredSignatureError:
        return 'Token expirado. Faça login novamente.'
    except jwt.InvalidTokenError:
        return 'Token inválido. Faça login novamente.'

def verificar_credenciais(username, password):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor(dictionary=True)

        query = "SELECT * FROM users WHERE username = %s AND password = %s"
        cursor.execute(query, (username, password))

        usuario = cursor.fetchone()

        cursor.close()
        conn.close()

        if usuario:
            return True
        else:
            return False

    except mysql.connector.Error as err:
        print("Erro ao verificar credenciais:", err)
        return False

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token = request.headers["Authorization"].split(" ")[1]
        if not token:
            return {
                "message": "Authentication Token is missing!",
                "data": None,
                "error": "Unauthorized"
            }, 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User().get_by_id(data["user_id"])
            if current_user is None:
                return {
                "message": "Invalid Authentication token!",
                "data": None,
                "error": "Unauthorized"
            }, 401
            if not current_user["active"]:
                abort(403)
        except Exception as e:
            return {
                "message": "Something went wrong",
                "data": None,
                "error": str(e)
            }, 500

        return f(current_user, *args, **kwargs)

    return decorated
