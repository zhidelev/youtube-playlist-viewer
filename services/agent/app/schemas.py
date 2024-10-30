from pydantic import BaseModel, HttpUrl, Field


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


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    skip: int = Field(0, ge=0, le=1000)
    limit: int = Field(100, gt=0, le=100)
