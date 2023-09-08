from fastapi import APIRouter, Depends
from urllib.parse import urlparse
import app.crud as crud

from app.dependencies import get_db
from app.schemas import Item, TrimmedItem
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/data", tags=["data"])
async def data(item: Item, db: Session = Depends(get_db)):
    # Example
    # https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK
    results = urlparse(item.url).query
    d = dict()
    for attr in results.split("&"):
        key, value = attr.split("=")
        d[key] = value
    t = TrimmedItem(list=d["list"])
    return crud.create_item(db=db, item=t)
