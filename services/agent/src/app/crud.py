from sqlalchemy.orm import Session
import app.models as models
import app.schemas as schemas


def create_item(db: Session, item: schemas.Item):
    db_item = models.Item(list=item.list, processed=False)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Item).offset(skip).limit(limit).all()
