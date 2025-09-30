from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel  
from . import schema
from .import models
from sqlalchemy.orm import Session
from fastapi import Depends
from .database import engine
from .database import SessionLocal
from typing import List




app = FastAPI()
models.Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:    
        db.close()

#product route
@app.get('/products', response_model=List[schema.displayProduct])
def products(db: Session = Depends(get_db)):
    products = db.query(models.product).all()
    return products

@app.get('/product/{id}')
def product(id:int,db: Session = Depends(get_db)):
    product = db.query(models.product).filter(models.product.id==id).first()
    return product

@app.post('/product')
def add(request:schema.product,db: Session = Depends(get_db)):
    new_product = models.product(name=request.name,price=request.price,quantity=request.quantity, seller_id=1 )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    return request

@app.delete('/product/{id}')
def delete(id:int,db: Session = Depends(get_db)):
    product = db.query(models.product).filter(models.product.id==id).delete()
    db.commit()
    return 'done'

@app.put('/product/{id}')
def update(id:int,request:schema.product,db: Session = Depends(get_db)):
    product = db.query(models.product).filter(models.product.id==id)
    if not product.first():
        pass
    product.update({
        models.product.name:request.name,
        models.product.price:request.price,
        models.product.quantity:request.quantity
    })
    db.commit()
    return 'updated'


#seller route

@app.post('/seller')
def create_seller(request:schema.Seller,db: Session = Depends(get_db)):
    new_seller = models.Seller(username=request.name,age=request.age,email=request.email)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return request

#login route

@app.post('/login')
def login(request:schema.login,db: Session = Depends(get_db)):
    return request

