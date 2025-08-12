from flask import jsonify, request
from flask.views import MethodView

from models.car_repository import CarRepository
from engine.eng import engine

class CarAPI(MethodView):
    def __init__(self):
        self.car_repo = CarRepository(engine)

    def get(self, id=None):
        if id is None:
            return jsonify(self.car_repo.get_all())
        else:
            return jsonify(self.car_repo.get_one(id))
        
    def post(self):
        data = request.get_json()
        if not "user_id" in data:
            user_id = None
        else:
            user_id = data["user_id"]
        new_car = self.car_repo.add_car(data["make"], data["model"], user_id)
        return jsonify(new_car), 201
    
    def patch(self, id=None):
        data = request.get_json()
        updated_car = self.car_repo.update_car_owner(id, data["user_id"])
        return jsonify(updated_car), 201
    
    def delete(self, id=None):
        deleted_car = self.car_repo.delete_car_with_id(id)
        return jsonify(deleted_car), 201

