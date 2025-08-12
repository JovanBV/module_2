from db.db_manager import Address
from sqlalchemy.orm import Session 
from sqlalchemy import select
from psycopg2.errors import ForeignKeyViolation
from sqlalchemy.exc import IntegrityError

class AddressRepository:
    def __init__(self, engine):
        self.engine = engine

    def add_address(self, address: str, user_id: int) -> Address:
        try:
            with Session(self.engine) as session:
                address = Address(address=address, user_id=user_id)
                session.add(address)
                session.commit()
                session.refresh(address)
            return address.to_dict()
        except IntegrityError as error:
            if isinstance(error.orig, ForeignKeyViolation):
                print("Couldn't add new address because user_id doesn't exist or is not valid. Error:", error)
            else:
                print("Integrity error occurred:", error)

    def get_all(self) -> Address:
        try:
            with Session(self.engine) as session:
                stmt = select(Address)
                address = session.scalars(stmt).all()
                all_addresses = []

                for entry in address:
                    all_addresses.append(entry.to_dict())
                return all_addresses
        except Exception as error:
            print(f"Couldn't fetch all addresses. Error: ", error)


    def delete_address_with_id(self, id: int) -> Address:
        try:
            with Session(self.engine) as session:
                address = session.get(Address, id)
                if address == None:
                    return ({"id": "ID not found"})
                session.delete(address)
                session.commit()
                return address.to_dict()
        except Exception as error:
            print(f"Couldn't delete address with id: {id}. Error: ", error)

    def update_address(self, id, new_address) -> Address:
        try:
            with Session(self.engine) as session:
                address = session.get(Address, id)
                if address == None:
                    return ({"id": "ID not found"})
                address.address = new_address
                session.commit()
                session.refresh(address)
                return address.to_dict()
        except Exception as error:
            print(f"Couldn't update user with id: {id}. Error: ", error)


    def get_one(self, id=None) -> Address:
        try:
            with Session(self.engine) as session:
                user = session.get(Address, id)
                if user is None:
                    return {"ID not found": f"{id}"}
                return user.to_dict()
        except Exception as error:
            print("Error fetching one Address.", error)