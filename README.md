# Simple backend music library

Music library back-end api written using Python's FastAPI framework, SQLAlchemy (and ORM) . Data is persisted in SQLite (optional PostgreSQL).

## Dev

Install the Python dependencies

```python
poetry install
```

Run the app server with hot reload

```python
poetry run uvicorn album_fastapi.main:app --reload
```

Navigate to `/docs` in your browser to consume (or your favorite software).

## Tests

To run the unit tests

```python
poetry run pytest
```
