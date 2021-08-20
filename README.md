# Simple backend music library

Music library back-end api written using Python's FastAPI framework, SQLAlchemy (and ORM) . Data is persisted in SQLite (optional PostgreSQL).

## Dev

Install the Python dependencies

```python
poetry install
```

Run the app server with hot reload

```python
peotry run uvicorn album_fastapi.main:app --reload  
```