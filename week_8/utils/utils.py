from flask import request, jsonify
import functools
from jwt_manager.jwt_manager import jwt_manager
from cache_manager import cache_manager
from db.user_manager import db

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
        def wrapper(*args, **kwargs):
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

def format_fruit(data):
    date = data["entry_date"]
    data["entry_date"] = date.timestamp()
    return data

def get_fruit_from_db_or_cache(id):
    cache_key = f"fruits:{id}"

    data = cache_manager.get_hash(cache_key)
    if data:
        return data
    
    data = db.get_fruit_by_id(id)
    if data:
        formated_data = format_fruit(data)
        cache_manager.store_hashed_fruit(id, formated_data)
        return data
    
    return jsonify(error="No fruits to retrieve.")


def get_all_fruits_from_db_or_cache(key):
    data = cache_manager.get_all_similar_keys(key)
    if data:
        print("From Redis")
        return data
    
    data = db.get_fruits()
    if data:
        print("from DB")
        return data

    return None

def post_fruit(data):
    name = data.get("name")
    price = data.get("price")
    entry_date = data.get("entry_date")
    stock = data.get("stock")

    new_product = db.insert_fruit(name, price, entry_date, stock)

    formated_fruit = format_fruit(new_product)
    cache_manager.store_hashed_fruit(new_product.get("id"), formated_fruit)

    if new_product is None:
        return {"error": "error inserting fruit."}
    return new_product

def delete_keys(data, *args):
    for key in args:
        if key in data:
            del data[key]
    return data