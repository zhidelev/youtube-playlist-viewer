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
    db_item = db.query(models.Playlist).filter(models.Playlist.list == item.list).first()
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
    playlist = db.query(models.Playlist).filter(models.Playlist.id == item_id).first()
    return db.query(models.Video).filter(models.Video.list_id == playlist.list).all()


def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(**video.model_dump())
    db.add(db_video)
    db.commit()
    db.refresh(db_video)
    return db_video
