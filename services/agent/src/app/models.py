from sqlalchemy import Boolean, Column, Integer, String

from app.database import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    list = Column(String, index=True)
    processed = Column(Boolean)
