from functools import wraps
from flask import Response, request, jsonify
import functools
from jwt_manager.jwt_manager import jwt_manager


def validate_user_data(data):
    if not data:
        return False, "Missing JSON body"
    if 'username' not in data or not isinstance(data['username'], str) or not data['username'].strip():
        return False, "Invalid or missing username"
    if 'password' not in data or not isinstance(data['password'], str) or len(data['password']) < 6:
        return False, "Password must be at least 6 characters"
    return True, None


def get_user_id(token):
    try:
        if token is not None:
            clean_token = token.replace("Bearer ", "")
            decoded = jwt_manager.decode(clean_token)

            if decoded is None:
                return None
            
            if decoded.get("data") and "password" in decoded["data"]:
                del decoded["data"]["password"]

            return decoded["data"]["id"]
        else:
            return None
    except Exception as e:
        return None

def access_with_roles(*allowed_roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):  # agregá kwargs por si el endpoint los necesita
            token = request.headers.get('Authorization')

            if not token:
                return jsonify({"error": "Token missing"}), 401
            
            test = token.replace("Bearer ","")
            user = jwt_manager.decode(test)

            user_role = user["data"]["role"]
            
            if user_role in allowed_roles:
                return func(*args, **kwargs)
            else:
                return jsonify({"error": "Access denied"}), 403

        return wrapper
    return decorator
