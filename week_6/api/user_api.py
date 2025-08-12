from flask import jsonify, request
from flask.views import MethodView

from models.user_repository import UserRepository
from engine.eng import engine

class UserAPI(MethodView):
    def __init__(self):
        self.user_repo = UserRepository(engine)

    def get(self, id=None):
        if id is None:
            return jsonify(self.user_repo.get_all())
        else:
            return jsonify(self.user_repo.get_one(id))
        
    def post(self):
        data = request.get_json()
        new_user = self.user_repo.add_user(data["name"])
        return jsonify(new_user), 201
    
    def patch(self, id=None):
        data = request.get_json()
        updated_user = self.user_repo.update_username(id, data["name"])
        return jsonify(updated_user), 201
    
    def delete(self, id=None):
        deleted_user = self.user_repo.delete_user_with_id(id)
        return jsonify(deleted_user), 201


