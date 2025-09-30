# Todo List API

A simple Todo List application built with Python FastAPI, SQLAlchemy, and SQLite database.

## Features

- ✅ Create new todos
- 📋 View all todos
- 🔍 Get specific todo by ID
- ✏️ Update todo (title, description, completion status)
- 🗑️ Delete todos
- 📊 Filter completed/pending todos
- 🕒 Automatic timestamps (created_at, updated_at)
- 💾 **Persistent storage with SQLite database**
- 🔄 **Database migrations and schema management**

## Setup

1. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

2. **Run the application:**

   ```bash
   python main.py
   ```

   Or using uvicorn directly:

   ```bash
   uvicorn main:app --reload
   ```

3. **Access the API:**
   - API will be available at: `http://localhost:8000`
   - Interactive API docs (Swagger UI): `http://localhost:8000/docs`
   - Alternative API docs (ReDoc): `http://localhost:8000/redoc`

## API Endpoints

| Method | Endpoint           | Description         |
| ------ | ------------------ | ------------------- |
| GET    | `/`                | Welcome message     |
| GET    | `/todos`           | Get all todos       |
| GET    | `/todos/{todo_id}` | Get specific todo   |
| POST   | `/todos`           | Create new todo     |
| PUT    | `/todos/{todo_id}` | Update todo         |
| DELETE | `/todos/{todo_id}` | Delete todo         |
| GET    | `/todos/completed` | Get completed todos |
| GET    | `/todos/pending`   | Get pending todos   |

## Example Usage

### Create a new todo:

```bash
curl -X POST "http://localhost:8000/todos" \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "description": "Complete the tutorial"}'
```

### Get all todos:

```bash
curl -X GET "http://localhost:8000/todos"
```

### Update a todo:

```bash
curl -X PUT "http://localhost:8000/todos/1" \
     -H "Content-Type: application/json" \
     -d '{"completed": true}'
```

### Delete a todo:

```bash
curl -X DELETE "http://localhost:8000/todos/1"
```

## Data Models

### TodoCreate

- `title` (required): Todo title
- `description` (optional): Todo description

### TodoUpdate

- `title` (optional): Updated title
- `description` (optional): Updated description
- `completed` (optional): Completion status

### Todo

- `id`: Unique identifier
- `title`: Todo title
- `description`: Todo description
- `completed`: Completion status (default: false)
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

## Database

- **SQLite Database**: The app uses SQLite for persistent storage (`todos.db` file)
- **SQLAlchemy ORM**: Object-Relational Mapping for database operations
- **Automatic Schema Creation**: Database tables are created automatically on first run
- **Connection Management**: Proper database session handling with FastAPI dependencies

## Notes

- **Persistent Storage**: Todos are now stored in a SQLite database and persist between server restarts
- **Production Ready**: Uses proper database session management and SQLAlchemy ORM
- **Automatic Validation**: The API includes automatic data validation using Pydantic models
- **Interactive Docs**: FastAPI automatically generates interactive API documentation
- **Database File**: A `todos.db` file will be created in your project directory to store data
