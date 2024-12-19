# Todo app for learning FastAPI

This is a todo application intended to learn FastAPI, using the following features and packages

- SQLite as database
- FastAPI Router
- pydantic for validation
- sqlalchemy as ORM

### 1. Create virtual environment

```bash
python -m venv appenv
```
### 2. Activate virtual environment

```bash
.\appenv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. To run application

```bash
uvicorn main:app --reload
```

### 5. Swagger docs
http://localhost:8000/docs

### 6. Redocs
http://localhost:8000/redoc