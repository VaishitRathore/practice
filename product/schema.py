from pydantic import BaseModel

class product(BaseModel):
    name: str
    description: str 
    price: int
    