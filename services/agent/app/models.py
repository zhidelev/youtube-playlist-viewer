from sqlalchemy import Boolean, Column, ForeignKey, Integer, String

from .database import Base


class Playlist(Base):
    __tablename__ = "playlists"

    id = Column(Integer, primary_key=True, index=True)
    list = Column(String, index=True)
    processed = Column(Boolean)


class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    list_id = Column(Integer, ForeignKey("playlists.id"))
    youtube_id = Column(String, index=True)
    title = Column(String, default="")
    description = Column(String, default="")
    privacy_status = Column(String)
    view_count = Column(Integer, default=0)
    like_count = Column(Integer, default=0)
    dislike_count = Column(Integer, default=0)
    comment_count = Column(Integer, default=0)
