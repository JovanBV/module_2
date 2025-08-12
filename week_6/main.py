from db.db_manager import Base
from utils.create_app import create_app
from engine.eng import engine
from utils.api_registry import register_api
from api.user_api import UserAPI
from api.address_api import AddressAPI
from api.car_api import CarAPI

if __name__ == '__main__':
    
    Base.metadata.create_all(engine)
    app = create_app()
    
    register_api(app, UserAPI, "user")
    register_api(app, AddressAPI, "address")
    register_api(app, CarAPI, "car")

    app.run(debug=True)