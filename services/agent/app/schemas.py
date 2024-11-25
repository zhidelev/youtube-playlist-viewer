from pydantic import BaseModel, Field, HttpUrl


class Item(BaseModel):
    url: HttpUrl


class TrimmedItem(BaseModel):
    list: str

    class ConfigDict:
        orm_mode = True


class VideoCreate(BaseModel):
    youtube_id: str
    list_id: int
    title: str
    description: str
    privacy_status: str
    view_count: int
    like_count: int
    dislike_count: int
    comment_count: int

    class ConfigDict:
        orm_mode = True


class Row(BaseModel):
    id: int
    list: str
    processed: bool


class FilterParams(BaseModel):
    model_config = {"extra": "forbid"}

    skip: int = Field(0, ge=0, le=1000)
    limit: int = Field(100, gt=0, le=100)
