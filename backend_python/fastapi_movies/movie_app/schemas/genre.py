from pydantic import BaseModel


class GenreBase(BaseModel):
    name: str

    class Config:
        orm_mode = True


class GenreSchemeCreate(GenreBase):
    pass


class GenreSchemeOut(GenreBase):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "genre_name": "Western"
            }
        }



class GenresCreate(BaseModel):
    id: int





