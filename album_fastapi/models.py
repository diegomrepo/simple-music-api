from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base


class Artist(Base):
    __tablename__ = "artists"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)

    tracks = relationship("Track", back_populates="author")

# In this model tracks must have a single author and album (opt)
class Track(Base):
    __tablename__ = "tracks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    author_id = Column(Integer, ForeignKey("artists.id"))
    disk_id = Column(Integer, ForeignKey("album.id"))

    author = relationship("Artist", back_populates="tracks")
    disk = relationship("Album", back_populates="tracks")


# Albums are compilations (can have many artists e.g. Soundtracks)
class Album(Base):
    __tablename__ = "album"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)

    tracks = relationship("Track", back_populates="disk")
