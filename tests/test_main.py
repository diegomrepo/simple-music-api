import os

import pytest as pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from album_fastapi.database import Base
from album_fastapi.main import app, get_db

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_read_main():
    response = client.get("/")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_create_artist():
    response = client.post(
        "/artists/",
        json={"name": "Beethoven"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Beethoven"
    assert "id" in data
    artist_id = data["id"]

    response = client.get(f"/artists/{artist_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["name"] == "Beethoven"
    assert data["id"] == artist_id


def test_create_album():
    response = client.post(
        "/album/",
        json={"title": "Greatest Masterpieces"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Greatest Masterpieces"
    assert "id" in data
    album_id = data["id"]

    response = client.get(f"/album/{album_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Greatest Masterpieces"
    assert data["id"] == album_id


def test_read_artist():
    artist_id = 1
    response = client.get(f"/artists/{artist_id}")
    assert response.status_code == 200
    assert response.json() == {
        "name": "Beethoven",
        "id": 1,
        "tracks": []
    }


def test_read_artists():
    artist_id = 1
    response = client.get("/artists/")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'Beethoven', 'tracks': []}]


def test_read_albums():
    response = client.get("/album/")
    assert response.status_code == 200, response.text
    # data = response.json()
    assert response.json() == [{'id': 1, 'title': 'Greatest Masterpieces', 'tracks': []}]


def test_create_track():
    artist_id = 1
    response = client.post(
        f"/artists/{artist_id}/tracks/",
        json={"title": "Moonlight"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "title": "Moonlight",
        "id": 1,
        "author_id": 1,
        "disk_id": None
    }

    
def test_read_tracks():
    response = client.get("/tracks/")
    assert response.status_code == 200, response.text
    assert response.json() == [{
        'title': 'Moonlight',
        'id': 1,
        'author_id': 1,
        'disk_id': None
    }]


@pytest.fixture(scope="session", autouse=True)
def cleanup(request):
    def remove_test_dir():
        os.remove("test.db")

    request.addfinalizer(remove_test_dir)
