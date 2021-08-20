from sqlalchemy.orm import Session

from . import models, schemas


def get_artist(db: Session, artist_id: int):
    return db.query(models.Artist).filter(models.Artist.id == artist_id).first()


def get_album(db: Session, album_id: int):
    return db.query(models.Album).filter(models.Album.id == album_id).first()


def get_artist_by_name(db: Session, name: str):
    return db.query(models.Artist).filter(models.Artist.name == name).first()


def get_album_by_title(db: Session, title: str):
    return db.query(models.Album).filter(models.Album.title == title).first()


def get_artists(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Artist).offset(skip).limit(limit).all()


def get_albums(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Album).offset(skip).limit(limit).all()


def create_artist(db: Session, artist: schemas.ArtistCreate):
    db_artist = models.Artist(name=artist.name)
    db.add(db_artist)
    db.commit()
    db.refresh(db_artist)
    return db_artist


def create_album(db: Session, album: schemas.AlbumCreate):
    db_album = models.Album(title=album.title)
    db.add(db_album)
    db.commit()
    db.refresh(db_album)
    return db_album


def get_tracks(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Track).offset(skip).limit(limit).all()


def create_artist_track(db: Session, track: schemas.TrackCreate, artist_id: int):
    db_track = models.Track(**track.dict(), author_id=artist_id)
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track


def add_album_track(db: Session, track_id: int, album_id: int):
    db_track = db.query(models.Track).filter(models.Track.id == track_id).one_or_none()
    if db_track is None:
        return None
    db_track.disk_id = album_id
    db.add(db_track)
    db.commit()
    db.refresh(db_track)
    return db_track
