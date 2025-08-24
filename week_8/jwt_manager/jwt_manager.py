import jwt
from jwt.exceptions import InvalidKeyError
import time

class JWT_Manager:
    def __init__(self):
        self.private_key = ""
        self.public_key = ""

    def encode(self, data):
        try:
            payload = {
                "data": data,
                "iat": int(time.time())
            }
            return jwt.encode(payload, self.private_key, algorithm="RS256")
        except Exception as e:
            print("Error encoding the data: ", e)

    def decode(self, token) :
        try:
            return jwt.decode(token, self.public_key, algorithms=["RS256"])
        except Exception as e:
            print("Error decoding JWT:", e)
            return None
        



jwt_manager = JWT_Manager()