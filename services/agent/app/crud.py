from sqlalchemy.orm import Session

from . import models, schemas


def create_item(db: Session, item: schemas.Item):
    db_item = models.Item(list=item.list, processed=False)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()
