from db.db_manager import Cars
from sqlalchemy.orm import Session
from sqlalchemy import select
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError


class CarRepository:
    def __init__(self, engine):
        self.engine = engine

    def add_car(self, make: str, model: str, user_id: int) -> Cars:
        try:
            with Session(self.engine) as session:
                car = Cars(make=make, model=model, user_id=user_id)
                session.add(car)
                session.commit()
                session.refresh(car)
            return car.to_dict()
        except IntegrityError as error:
            if isinstance(error.orig, ForeignKeyViolation):
                print("Couldn't add new car because user_id doesn't exist or is not valid. Error:", error)
            else:
                print("Integrity error occurred:", error)

    def get_all(self) -> Cars:
        try:
            with Session(self.engine) as session:
                stmt = select(Cars)
                cars = session.scalars(stmt).all()
                all_cars = []
                for entry in cars:
                    all_cars.append(entry.to_dict())
                return all_cars
        except Exception as error:
            print(f"Couldn't fetch all cars. Error: ", error)

    def delete_car_with_id(self, id: int) -> Cars:
        try:
            with Session(self.engine) as session:
                car = session.get(Cars, id)
                if car == None:
                    return ({"id": "ID not found"})
                session.delete(car)
                session.commit()
                return car.to_dict()
        except Exception as error:
            print(f"Couldn't delete car with id: {id}. Error: ", error)

    def update_car_owner(self, id, new_owner) -> Cars:
        try:
            with Session(self.engine) as session:
                car = session.get(Cars, id)
                if car == None:
                    return ({"id": "ID not found"})
                car.user_id = new_owner
                session.commit()
                session.refresh(car)
                return car.to_dict()
        except IntegrityError as error:
            if isinstance(error.orig, ForeignKeyViolation):
                print("Couldn't update car owner because user_id is not a valid user. Error:", error)
            else:
                print("Integrity error occurred:", error)

    def get_one(self, id=None) -> Cars:
        try:
            with Session(self.engine) as session:
                user = session.get(Cars, id)
                if user is None:
                    return {"ID not found": f"{id}"}
                return user.to_dict()
        except Exception as error:
            print("Error fetching one car.", error)