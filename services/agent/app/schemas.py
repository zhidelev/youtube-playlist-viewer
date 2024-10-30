from pydantic import BaseModel, HttpUrl


class Item(BaseModel):
    url: HttpUrl


class TrimmedItem(BaseModel):
    list: str

    class Config:
        orm_mode = True


class Row(BaseModel):
    id: int
    list: str
    processed: bool
