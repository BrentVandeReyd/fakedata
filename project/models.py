from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    fakename = relationship("Item", back_populates="fakedata")


class Item(Base):
    __tablename__ = "fakedata"

    id = Column(Integer, primary_key=True, index=True)

    fakename = Column(String, index=True)
    ip_id = Column(Integer, ForeignKey("Ip.id"))
    owner = Column(Integer, ForeignKey("users.id"))
    fakedata = relationship("User", back_populates="fakename")
    ip = relationship("Ip", back_populates="fakedata")

class Ip(Base):
    __tablename__ = "Ip"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, index=True)
    fakedata = relationship("Item", back_populates="ip")

