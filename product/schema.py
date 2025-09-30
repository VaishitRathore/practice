from pydantic import BaseModel

class product(BaseModel):
    name: str
    description: str 
    price: int
    

class Seller(BaseModel):
    name: str
    age: int
    email : str
    class Config:
        orm_mode = True

class displayProduct(BaseModel):
    name: str
    description: str
    class Config:
        orm_mode = True

class login(BaseModel):
    username: str
    password: str
