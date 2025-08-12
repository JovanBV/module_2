from db.db_manager import Users
from sqlalchemy.orm import Session 
from sqlalchemy import select


class UserRepository:
    def __init__(self, engine):
        self.engine = engine

    def add_user(self, name: str) -> Users:
        with Session(self.engine) as session:
            user = Users(name=name)
            session.add(user)
            session.commit()
            session.refresh(user)
        return user.to_dict()
    
    def get_all(self) -> Users:
        try:
            with Session(self.engine) as session:
                stmt = select(Users)
                users = session.scalars(stmt).all()
                all_users = []

                for user in users:
                    all_users.append(user.to_dict())
                print(all_users)
                return all_users
        except Exception as error:
            print(f"Couldn't fetch all users. Error: ", error)


    def delete_user_with_id(self, id: int) -> Users:
        try:
            with Session(self.engine) as session:
                user = session.get(Users, id)
                if user == None:
                    return ({"id": "ID not found"})
                session.delete(user)
                session.commit()
                return user.to_dict()
        except Exception as error:
            print(f"Couldn't delete user with id: {id}. Error: ", error)

    def update_username(self, id, new_username) -> Users:
        try:
            with Session(self.engine) as session:
                user = session.get(Users, id)
                if user == None:
                    return ({"id": "ID not found"})
                user.name = new_username
                session.commit()
                session.refresh(user)
                return user.to_dict()
        except Exception as error:
            print(f"Couldn't update user with id: {id}. Error: ", error)

    def get_one(self, id=None) -> Users:
        try:
            with Session(self.engine) as session:
                user = session.get(Users, id)
                if user is None:
                    return {"ID not found": f"{id}"}
                return user.to_dict()
        except Exception as error:
            print("Error fetching one user.", error)