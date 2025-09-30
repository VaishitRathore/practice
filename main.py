from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import List, Optional
from datetime import datetime

# Database setup
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy model
class TodoModel(Base):
    __tablename__ = "todos"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    completed = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Create tables
Base.metadata.create_all(bind=engine)

# Pydantic models
class TodoCreate(BaseModel):
    title: str
    description: Optional[str] = None

class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None

class Todo(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    completed: bool = False
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Dependency to get database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI(title="Todo List API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Welcome to Todo List API "}

@app.get("/todos", response_model=List[Todo])
async def get_todos(db: Session = Depends(get_db)):
    """Get all todos"""
    todos = db.query(TodoModel).all()
    return todos

@app.get("/todos/{todo_id}", response_model=Todo)
async def get_todo(todo_id: int, db: Session = Depends(get_db)):
    """Get a specific todo by ID"""
    todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    return todo

@app.post("/todos", response_model=Todo)
async def create_todo(todo: TodoCreate, db: Session = Depends(get_db)):
    """Create a new todo"""
    db_todo = TodoModel(
        title=todo.title,
        description=todo.description,
        completed=False
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.put("/todos/{todo_id}", response_model=Todo)
async def update_todo(todo_id: int, todo_update: TodoUpdate, db: Session = Depends(get_db)):
    """Update a todo"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    # Update fields if provided
    if todo_update.title is not None:
        db_todo.title = todo_update.title
    if todo_update.description is not None:
        db_todo.description = todo_update.description
    if todo_update.completed is not None:
        db_todo.completed = todo_update.completed
    
    db_todo.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_todo)
    return db_todo

@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int, db: Session = Depends(get_db)):
    """Delete a todo"""
    db_todo = db.query(TodoModel).filter(TodoModel.id == todo_id).first()
    if db_todo is None:
        raise HTTPException(status_code=404, detail="Todo not found")
    
    title = db_todo.title
    db.delete(db_todo)
    db.commit()
    return {"message": f"Todo '{title}' deleted successfully"}

@app.get("/todos/completed", response_model=List[Todo])
async def get_completed_todos(db: Session = Depends(get_db)):
    """Get all completed todos"""
    todos = db.query(TodoModel).filter(TodoModel.completed == True).all()
    return todos

@app.get("/todos/pending", response_model=List[Todo])
async def get_pending_todos(db: Session = Depends(get_db)):
    """Get all pending todos"""
    todos = db.query(TodoModel).filter(TodoModel.completed == False).all()
    return todos

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
