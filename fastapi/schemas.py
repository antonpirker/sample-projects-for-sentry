from pydantic import BaseModel


class ShowBase(BaseModel):
    title: str
    description: str
    show_type: str
    categories: str
    release_year: int
    director: str
    cast: str
    countries: str
    duration: str
    rating: str
    date_added: str


class ShowCreate(ShowBase):
    pass


class Show(ShowBase):
    id: int

    class Config:
        orm_mode = True
