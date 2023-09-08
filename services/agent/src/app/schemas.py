from pydantic import BaseModel


class Item(BaseModel):
    url: str


class TrimmedItem(BaseModel):
    list: str

    class Config:
        orm_mode = True
