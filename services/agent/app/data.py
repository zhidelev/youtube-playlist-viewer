from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud
from .dependencies import get_db
from .schemas import Item, TrimmedItem

router = APIRouter()


@router.post("/data", tags=["data"], responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}})
def data(item: Item, db: Session = Depends(get_db)):
    # Example
    # https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK
    if item.url.query is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"There is no query string in the URL: {item.url}"},
        )
    d = dict()
    query_string = item.url.query
    for attr in query_string.split("&"):
        key, value = attr.split("=")
        d[key] = value
    t = TrimmedItem(list=d["list"])
    return crud.create_item(db=db, item=t)
