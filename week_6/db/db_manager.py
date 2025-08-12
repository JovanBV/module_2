from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from typing import List, Optional

class Base(DeclarativeBase):
    pass

class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(20))

    addresses: Mapped[List["Address"]] = relationship(back_populates="user")
    cars: Mapped[List["Cars"]] = relationship(back_populates="user")

    def __repr__(self) -> str:
        return f"User(id={self.id}, name= {self.name})"
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

class Address(Base):
    __tablename__ = "addresses"

    id: Mapped[int] = mapped_column(primary_key=True)
    address: Mapped[str] = mapped_column(String(40))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped["Users"] = relationship(back_populates="addresses")

    def __repr__(self) -> str:
        return f"Address(id={self.id}, address= {self.address}, user_id= {self.user_id})"
    

    def to_dict(self):
        return {
            "id": self.id,
            "address": self.address,
            "user_id": self.user_id
        }


class Cars(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(primary_key=True)
    make: Mapped[str] = mapped_column(String(20))
    model: Mapped[str] = mapped_column(String(20))

    user_id: Mapped[Optional[int]] = mapped_column(ForeignKey("users.id"), nullable=True)
    user: Mapped["Users"] = relationship(back_populates="cars")

    def __repr__(self) -> str:
        return f"Cars(id={self.id}, make= {self.make}, model= {self.model}, user_id= {self.user_id})"

    def to_dict(self):
        return {
            "id": self.id,
            "make": self.make,
            "model": self.model,
            "user_id": self.user_id
        }