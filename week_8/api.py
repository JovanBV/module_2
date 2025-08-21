from flask import Flask, request, jsonify, Response
from db.user_manager import db
from jwt_manager.jwt_manager import jwt_manager
from utils.utils import access_with_roles, get_user_id, get_fruit_from_db_or_cache, get_all_fruits_from_db_or_cache, format_fruit, post_fruit, delete_keys
from cache_manager import cache_manager


app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = db.insert_user(data["username"], data["password"], data["role"])
    if new_user is None:
        return jsonify({"error": "user name already in use."})
    
    new_data = delete_keys(new_user, "id", "password")

    token = jwt_manager.encode(new_data)
    cache_manager.store_hash(token, new_data)

    return jsonify(token=token)


@app.route("/me")
@access_with_roles("Admin", "User")
def me():
    token = request.headers.get('Authorization')

    if token:
        clean_token = token.replace("Bearer ", "")
        decoded = jwt_manager.decode(clean_token)

    data = cache_manager.get_hash(clean_token)
    if data:
        return jsonify(data)

    user_data = delete_keys(decoded, "password")
    cache_manager.store_hash(clean_token, user_data["data"])

    return jsonify(user_data["data"])


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        return jsonify({"error": "Missing username or password"}), 400
    user = db.login_user(username, password)

    if not user:
        return jsonify({"error": "Invalid credentials"}), 403
    
    token = jwt_manager.encode(user)
    return jsonify(token=token)


@app.route("/fruits", methods=["GET"])
@access_with_roles("Admin")
def get_all():
    data = get_all_fruits_from_db_or_cache("fruits")
    return jsonify(data)


@app.route("/fruits/<int:id>", methods=["GET"])
@access_with_roles("Admin")
def get_fruit(id):
    data = get_fruit_from_db_or_cache(id)
    return data


@app.route("/fruits", methods=["POST"])
@access_with_roles("Admin")
def create():
    new_fruit = request.get_json()

    posted_fruit = post_fruit(new_fruit)
    return jsonify(posted_fruit)


@app.route("/fruits/<int:id>", methods=["PATCH"])
@access_with_roles("Admin")
def update(id):
    cache_manager.delete_key(id)

    data = request.get_json()
    new_amount = data.get("amount")

    updated_fruit = db.update_fruit(id, new_amount)

    if not updated_fruit:
        return jsonify(error="Error updating the fruit.")
    return jsonify(updated_fruit)    


@app.route("/fruits/<int:id>", methods=["DELETE"])
@access_with_roles("Admin")
def delete(id):

    cache_manager.delete_fruit(id)
    deleted_fruit = db.delete_fruit(id)
    
    if not deleted_fruit:
        return jsonify(error="fruit not found."), 404
    
    return jsonify(deleted_fruit)

@app.route("/order/add", methods=["POST"])
@access_with_roles("Admin", "User")
def add_to_order():
    token = request.headers.get('Authorization')
    user_id = get_user_id(token)
    item_to_add = request.get_json()

    fruit_id = item_to_add.get("fruit_id")
    quantity = item_to_add.get("quantity")

    if not quantity or quantity <= 0:
        return jsonify(error="quantity error"), 400
    
    if not fruit_id:
        return jsonify(error="invalid fruit id"), 400

    inserted_item = db.add_item_to_order(user_id, fruit_id, quantity)
    
    if inserted_item is None:
        return jsonify(error="error adding item to order"), 400

    return jsonify(inserted_item)

@app.route("/order/pending", methods=["GET"])
@access_with_roles("Admin", "User")
def get_pending_order():
    token = request.headers.get("Authorization")
    user_id = get_user_id(token)
    pending_items = db.get_pending_order_items(user_id)

    if not pending_items:
        return jsonify({"message": "No pending order items."}), 200

    return jsonify(pending_items)

@app.route("/checkout", methods=["POST"])
@access_with_roles("Admin", "User")
def checkout():
    token = request.headers.get('Authorization')
    user_id = get_user_id(token)
    
    pending_items = db.get_pending_order_items(user_id)
    if not pending_items:
        return jsonify(error="No pending order to checkout."), 404

    result = db.confirm_order(user_id)
    
    if "error" in result:
        return jsonify(result), 400
    
    return jsonify({"message": "Order confirmed successfully", "order": result})

@app.route("/orders", methods=["GET"])
@access_with_roles("Admin", "User")
def get_user_orders():
    token = request.headers.get("Authorization")
    user_id = get_user_id(token)
    orders = db.get_user_orders(user_id)

    return jsonify(orders)

app.run(debug=True)