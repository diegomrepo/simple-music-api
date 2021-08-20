from typing import List, Optional
from pydantic import BaseModel


class TrackBase(BaseModel):
    title: str


class TrackCreate(TrackBase):
    pass


class Track(TrackBase):
    id: int
    author_id: int
    disk_id: Optional[int] = None

    class Config:
        orm_mode = True


class ArtistBase(BaseModel):
    name: str


class ArtistCreate(ArtistBase):
    pass


class Artist(ArtistBase):
    id: int
    tracks: List[Track] = []

    class Config:
        orm_mode = True


class AlbumBase(BaseModel):
    title: str


class AlbumCreate(AlbumBase):
    pass


class Album(AlbumBase):
    id: int
    tracks: List[Track] = []

    class Config:
        orm_mode = True
