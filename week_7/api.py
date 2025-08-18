from flask import Flask, request, jsonify, Response
from db.user_manager import db
from jwt_manager.jwt_manager import jwt_manager
from utils.utils import access_with_roles, get_user_id

app = Flask(__name__)

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    new_user = db.insert_user(data["username"], data["password"], data["role"])
    if new_user is None:
        return jsonify({"error": "user name already in use."})
    
    token = jwt_manager.encode(new_user)
    return jsonify(token=token)


@app.route("/me")
@access_with_roles("Admin", "User")
def me():
    token = request.headers.get('Authorization')
    try:
        if token is not None:
            clean_token = token.replace("Bearer ", "")
            decoded = jwt_manager.decode(clean_token)

            if decoded is None:
                return jsonify({"error": "Invalid token"}), 401
            
            if decoded.get("data") and "password" in decoded["data"]:
                del decoded["data"]["password"]

            return jsonify(decoded["data"])
        else:
            return jsonify({"error": "No token provided"}), 401
    except Exception as e:
        return Response(response=Exception, status=500)


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
    all_fruits = db.get_fruits()
    return jsonify(all_fruits)


@app.route("/fruits/<int:id>", methods=["GET"])
@access_with_roles("Admin")
def get_fruit(id):
    fruit = db.get_fruit_by_id(id)
    if fruit is None:
        return jsonify(error="fruit not found."), 404
    return jsonify(fruit)


@app.route("/fruits/create", methods=["POST"])
@access_with_roles("Admin")
def create():
    new_fruit = request.get_json()

    name = new_fruit.get("name")
    price = new_fruit.get("price")
    entry_date = new_fruit.get("entry_date")
    stock = new_fruit.get("stock")

    new_product = db.insert_fruit(name, price, entry_date, stock)
    if new_product is None:
        return jsonify({"error": "error inserting fruit."})
    return jsonify(new_product)


@app.route("/fruits/update", methods=["PATCH"])
@access_with_roles("Admin")
def update():
    fruit_to_update = request.get_json()

    new_amount = fruit_to_update.get("amount")
    id = fruit_to_update.get("id")

    updated_fruit = db.update_fruit(id, new_amount)

    if updated_fruit is None:
        return jsonify(error="error updating fruit.")
    return jsonify(updated_fruit)


@app.route("/fruits/delete/<int:id>", methods=["DELETE"])
@access_with_roles("Admin")
def delete(id):

    deleted_fruit = db.delete_fruit(id)
    
    if deleted_fruit is None:
        return jsonify(error="fruit not found."), 404
    
    return jsonify(deleted_fruit_id = deleted_fruit)

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