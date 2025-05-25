from db.db import DbManager 
from populators.users_populator import UserPopulator
from populators.rental_populator import RentalPopulator
from populators.car_populator import CarPopulator
from managers.json_manager import JsonManager
from models.rental_repository import RentalRepository
from models.user_repository import UserRepository
from models.car_repository import CarRepository
from api import app, register_api, UserItemAPI, CarItemAPI, RentalItemAPI

# Creating and populating intances for populating, db_manager, and repositories

"------Database manager------"
db_manager = DbManager(
    db_name="postgres", password="jovan", user="postgres", host="localhost",
)

users_json_file = JsonManager('C:/Users/jovan/Documents/module_2/week_5.2/data//users.json')
cars_json_file = JsonManager('C:/Users/jovan/Documents/module_2/week_5.2/data//cars.json')
rental_file = JsonManager('C:/Users/jovan/Documents/module_2/week_5.2/data//car_user.json')

"------Repositories------"
user_repository = UserRepository(db_manager)
cars_repository = CarRepository(db_manager)
rental_repository = RentalRepository(db_manager)

"------Populators------"
user_populator = UserPopulator(users_json_file, user_repository)
car_populator = CarPopulator(cars_repository, cars_json_file)
rental_populator = RentalPopulator(rental_file, rental_repository)

#Use commented lines once or it will crash 💀 

# user_populator.populate_users()
# car_populator.populate_cars()
# rental_populator.populate_table()

"------Register for endpoints------"

def empty_tables():
    try:
        rental_repository.empty_table()
        user_repository.empty_table()
        cars_repository.empty_table()
    except:
        print("Error emptying tables.")

def reiniciate_counter():
    db_manager.cursor.execute("")

if __name__ == '__main__':
    register_api(app, user_repository, UserItemAPI, 'user')
    register_api(app, cars_repository, CarItemAPI, 'car')
    register_api(app, rental_repository, RentalItemAPI, 'rental')
    app.run(debug=True)
