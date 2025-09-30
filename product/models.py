from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base
from sqlalchemy.orm import relationship


class product(Base):
    __tablename__ = "products"
    id= Column(Integer, primary_key=True, index=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    sellers_id = Column(Integer, ForeignKey("sellers.id"))
    seller = relationship("Seller", back_populates="products")

    
class Seller(Base):
    __tablename__ = "sellers"
    id= Column(Integer, primary_key=True, index=True)
    username = Column(String)
    age = Column(Integer)
    email = Column(String) 

class login(Base):
    __tablename__ = "login"
    id= Column(Integer, primary_key=True, index=True)
    username = Column(String)
    password = Column(String)
