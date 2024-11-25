from sqlalchemy import func
from sqlalchemy.orm import Session

from . import models, schemas


def create_item(db: Session, item: schemas.TrimmedItem):
    # Checking if item is already in the database
    result = db.query(models.Playlist).filter(models.Playlist.list == item.list).first()
    if result:
        return result

    db_item = models.Playlist(list=item.list, processed=False)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def process_item(db: Session, item: schemas.TrimmedItem):
    db_item: models.Playlist | None = db.query(models.Playlist).filter(models.Playlist.list == item.list).first()
    if db_item:
        db_item.processed = True
        db.commit()
        db.refresh(db_item)
    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Playlist).offset(skip).limit(limit).all()


def get_item(db: Session, item_id):
    # Get max id in a table
    max_id = db.query(models.Playlist).order_by(models.Playlist.id.desc()).first().id
    if item_id > max_id:
        return None
    return db.query(models.Playlist).filter(models.Playlist.id == item_id).first()


def get_playlist_id_by_list(db: Session, list_id) -> int:
    found_id = db.query(models.Playlist).filter(models.Playlist.list == list_id).first().id
    return int(found_id) if found_id else 0


def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(**video.model_dump())
    found_id = db.query(models.Video).filter(models.Video.youtube_id == video.youtube_id).first()
    if found_id:
        db.update(db_video).where(models.Video.youtube_id == video.youtube_id)
        db.commit()
        return found_id
    db.add(db_video)
    db.refresh(db_video)
    return db_video


def get_videos(db: Session, list_id: str):
    return (
        db.query(models.Video)
        .join(models.Playlist)
        .filter(models.Playlist.list == list_id)
        .group_by(models.Video.youtube_id, models.Video.id)
        .order_by(func.max(models.Video.view_count).desc())
        .limit(5)
        .all()
    )
