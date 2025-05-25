
from flask import Flask, request, jsonify
from flask.views import MethodView
from models.car_repository import CarRepository
from models.user_repository import UserRepository
from models.rental_repository import RentalRepository
from db.db import DbManager

app = Flask(__name__)

class CarItemAPI(MethodView):
    def __init__(self, repo):
        self.repo = repo

    def get(self, id=None):
        try:
            sort_by = request.args.get("sort_by", "id")
            value = request.args.get("value", "")
            if id is not None:
                car = self.repo.get_by_id(id)
                return jsonify(car)
            
            elif sort_by and value:
                item = self.repo.sort(sort_by, value)
                if not item:
                    return jsonify({"error": "No data to fetch"}), 400
                return jsonify(item)
            
            elif not sort_by or not value:
                item = self.repo.get_all()
                return jsonify(item)

        except Exception as error:
            return jsonify({"error": f"Error fetching data: {error}"}), 400

    def post(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Missing request data"}), 400

            required_fields = ['make', 'model', 'year', 'condition']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

            make = data['make']
            model = data['model']
            year = data['year']
            condition = data['condition']

            id = self.repo.add_entry(make, model, year, condition)
            item = self.repo.get_by_id(id)
            return jsonify(item), 201
        except Exception:
            self.repo.db_manager.connection.rollback()
            return jsonify({"Error: ": f"Error posting data."})

    def patch(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request data"}), 400

        car_id = data.get('id')
        new_value = data.get('value')

        if not car_id or new_value is None:
            return jsonify({"error": "Missing id or value"}), 400
        
        if not new_value in self.repo.valid_car_condition:
            return jsonify({"error": "New condition is not valid."}), 400

        result = self.repo.update_with_id(car_id, new_value, "Condition", self.repo.valid_car_condition)

        if isinstance(result, dict) and "error" in result:
            return jsonify(result), 400

        car = self.repo.get_by_id(car_id)
        return jsonify(car)
    

class UserItemAPI(MethodView):
    def __init__(self, repo):
        self.repo = repo

    def get(self, id=None):
        try:
            sort_by = request.args.get("sort_by", "id")
            value = request.args.get("value", "")
            if id is not None:
                car = self.repo.get_by_id(id)
                return jsonify(car)
            
            elif sort_by and value:
                item = self.repo.sort(sort_by, value)
                if not item:
                    return jsonify({"error": "No data to fetch"}), 400
                return jsonify(item)
            
            elif not sort_by or not value:
                item = self.repo.get_all()
                return jsonify(item)

        except Exception as error:
            return jsonify({"error": f"Error fetching data: {error}"}), 400


    def post(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Missing request data"}), 400

            required_fields = ['name', 'email', 'user_name', 'birth_date', 'account_status']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

            name = data['name']
            email = data['email']
            user_name = data['user_name']
            password = data['password']
            birth_date = data['birth_date']
            account_status = data['account_status']

            id = self.repo.add_entry(name, email, user_name, password, birth_date, account_status)

            item = self.repo.get_by_id(id)
            return jsonify(item), 201
        except Exception:
            self.repo.db_manager.connection.rollback()
            return jsonify({"Error: ": f"Error posting data."})
    
    def patch(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request data"}), 400

        user_id = data.get('id')
        new_value = data.get('value')

        if not user_id or new_value is None:
            return jsonify({"error": "Missing id or value"}), 400
        
        if not new_value in self.repo.valid_account_status:
            return jsonify({"error": "New condition is not valid."}), 400

        result = self.repo.update_with_id(user_id, new_value, "account_status", self.repo.valid_account_status)

        if isinstance(result, dict) and "error" in result:
            return jsonify(result), 400

        user = self.repo.get_by_id(user_id)
        return jsonify(user)

class RentalItemAPI(MethodView):
    def __init__(self, repo):
        self.repo = repo

    def get(self, id=None):
        try:
            sort_by = request.args.get("sort_by", "id")
            value = request.args.get("value", "")
            if id is not None:
                car = self.repo.get_by_id(id)
                return jsonify(car)
            
            elif sort_by and value:
                item = self.repo.sort(sort_by, value)
                if not item:
                    return jsonify({"error": "No data to fetch"}), 400
                return jsonify(item)
            
            elif not sort_by or not value:
                item = self.repo.get_all()
                return jsonify(item)

        except Exception as error:
            return jsonify({"error": f"Error fetching data: {error}"}), 400

    def post(self):
        try:
            data = request.get_json()
            if not data:
                return jsonify({"error": "Missing request data"}), 400

            required_fields = ['car_id', 'user_id', 'rent_status']
            missing_fields = [field for field in required_fields if not data.get(field)]
            if missing_fields:
                return jsonify({"error": f"Missing fields: {', '.join(missing_fields)}"}), 400

            car_id = data['car_id']
            user_id = data['user_id']
            rent_status = data['rent_status']

            if not rent_status in self.repo.valid_account_status:
                return jsonify({"error": "Rent_status is not valid."}), 400

            id = self.repo.add_entry(car_id, user_id, rent_status)
            item = self.repo.get_by_id(id)
            return jsonify(item), 201
        except Exception:
            self.repo.db_manager.connection.rollback()
            return jsonify({"Error: ": f"Error posting data."})

    def patch(self):
        data = request.get_json()
        if not data:
            return jsonify({"error": "Missing request data"}), 400

        id = data.get('id')
        new_status = data.get('new_status')

        if not id or new_status is None :
            return jsonify({"error": "Missing id or value"}), 400
        
        if not new_status in self.repo.valid_account_status:
            return jsonify({"error": "New condition is not valid."}), 400

        result = self.repo.update_with_id(id, new_status, "rent_status", self.repo.valid_account_status)
        if isinstance(result, dict) and "error" in result:
            return jsonify(result), 400

        rental = self.repo.get_by_id(id)
        return jsonify(rental)

def register_api(app, model, API, name):
    item = API.as_view(f'{name}', model)
    app.add_url_rule(f'/{name}/<int:id>', view_func=item)
    app.add_url_rule(f'/{name}', view_func=item)



