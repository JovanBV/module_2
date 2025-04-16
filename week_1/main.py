from flask import Flask, request, jsonify

app = Flask(__name__)

users_list = [
	{
		"email": "action.bronson@gmail.com",
		"password": "123@a!",
	},
]


@app.route("/register", methods=["POST"])
def register_user():
    try:
        if "email" not in request.json:
            raise ValueError("email missing from the body")

        if "password" not in request.json:
            raise ValueError("password missing from the body")

        users_list.append(
            {
                "email": request.json["email"],
                "password": request.json["password"],
            }
        )
        return users_list
    except ValueError as ex:
        return jsonify(message=str(ex)), 400
    except Exception as ex:
		    # enviar un mensaje por slack
        return jsonify(message=str(ex)), 500

if __name__ == '__main__':
    app.run(host="localhost", debug=True)