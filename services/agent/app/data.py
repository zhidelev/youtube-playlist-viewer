from typing import Annotated

from fastapi import APIRouter, BackgroundTasks, Depends, Query, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from . import crud
from .dependencies import get_db
from .schemas import FilterParams, Item, TrimmedItem
from .tasks import process_playlist

router = APIRouter()


@router.post("/data", tags=["data"], responses={status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"}})
def data(item: Item, tasks: BackgroundTasks, db: Session = Depends(get_db)):
    # Example
    # https://youtube.com/playlist?list=PL0MRiRrXAvRhuVf-g4o3IO0jmpLQgubZK
    if "youtube.com" not in item.url.host:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"URL is not a YouTube playlist: {item.url}. Host: {item.url.host}"},
        )
    if item.url.query is None:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"There is no query string in the URL: {item.url}"},
        )
    d = dict()
    query_string = item.url.query
    for attr in query_string.split("&"):
        key, value = attr.split("=")
        if key == "list":
            d["list"] = value
    t = TrimmedItem(list=d["list"])
    tasks.add_task(process_playlist, d["list"], db)
    return crud.create_item(db=db, item=t)


@router.get("/lists", tags=["data"])
def get_lists(filter_query: Annotated[FilterParams, Query()], db: Session = Depends(get_db)):
    return crud.get_items(db, skip=filter_query.skip, limit=filter_query.limit)


@router.get(
    "/list/{list_id}",
    tags=["data"],
    responses={
        status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
        status.HTTP_404_NOT_FOUND: {"description": "Not Found"},
    },
)
def get_list(list_id: str, db: Session = Depends(get_db)):
    try:
        casted_list_id = int(list_id)
    except ValueError:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"Invalid list ID: {list_id}"},
        )
    if casted_list_id < 1:
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": f"Invalid list ID: {list_id}"},
        )
    result = crud.get_item(db, casted_list_id)
    if result is None:
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error": f"List with ID {list_id} not found"},
        )
    return result
