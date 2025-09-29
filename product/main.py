from fastapi import FastAPI
from pydantic import BaseModel  
from . import schema
from .import models
from .database import engine

app = FastAPI()
models.Base.metadata.create_all(engine)



@app.post('/product')
def add(request:schema.product):
    return request



