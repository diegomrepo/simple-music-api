from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/artists/", response_model=schemas.Artist)
def create_artist(artist: schemas.ArtistCreate, db: Session = Depends(get_db)):
    db_artist = crud.get_artist_by_name(db, name=artist.name)
    if db_artist:
        raise HTTPException(status_code=400, detail="Name already registered")
    return crud.create_artist(db=db, artist=artist)


@app.post("/album/", response_model=schemas.Album)
def create_album(album: schemas.AlbumCreate, db: Session = Depends(get_db)):
    db_album = crud.get_album_by_title(db, title=album.title)
    if db_album:
        raise HTTPException(status_code=400, detail="Title already registered")
    return crud.create_album(db=db, album=album)


@app.get("/artists/", response_model=List[schemas.Artist])
def read_artists(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    artists = crud.get_artists(db, skip=skip, limit=limit)
    return artists


@app.get("/album/", response_model=List[schemas.Album])
def read_albums(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    albums = crud.get_albums(db, skip=skip, limit=limit)
    return albums


@app.get("/artists/{artist_id}", response_model=schemas.Artist)
def read_artist(artist_id: int, db: Session = Depends(get_db)):
    db_artist = crud.get_artist(db, artist_id=artist_id)
    if db_artist is None:
        raise HTTPException(status_code=404, detail="Artist not found")
    return db_artist


@app.get("/album/{album_id}", response_model=schemas.Album)
def read_album(album_id: int, db: Session = Depends(get_db)):
    db_album = crud.get_album(db, album_id=album_id)
    if db_album is None:
        raise HTTPException(status_code=404, detail="Album not found")
    return db_album


@app.post("/artists/{artist_id}/tracks/", response_model=schemas.Track)
def create_track_for_artist(
    artist_id: int, track: schemas.TrackCreate, db: Session = Depends(get_db)
):
    return crud.create_artist_track(db=db, track=track, artist_id=artist_id)


@app.post("/album/{album_id}/track/{track_id}", response_model=schemas.Album)
def add_track_to_album(
        album_id: int, track_id: int, db: Session = Depends(get_db)
):
    return crud.add_album_track(db=db, track_id=track_id, album_id=album_id)


@app.get("/tracks/", response_model=List[schemas.Track])
def read_tracks(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tracks = crud.get_tracks(db, skip=skip, limit=limit)
    return tracks
