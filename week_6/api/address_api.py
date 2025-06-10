from flask import jsonify, request
from flask.views import MethodView

from models.address_repository import AddressRepository
from engine.eng import engine

class AddressAPI(MethodView):
    def __init__(self):
        self.address_repo = AddressRepository(engine)

    def get(self, id=None):
        if id is None:
            return jsonify(self.address_repo.get_all())
        else:
            return jsonify(self.address_repo.get_one(id))
        
    def post(self):
        data = request.get_json()
        new_address = self.address_repo.add_address(data["address"], data["user_id"])
        return jsonify(new_address), 201
    
    def patch(self, id=None):
        data = request.get_json()
        updated_address = self.address_repo.update_address(id, data["address"])
        return jsonify(updated_address), 201
    
    def delete(self, id=None):
        deleted_address = self.address_repo.delete_address_with_id(id)
        return jsonify(deleted_address), 201

