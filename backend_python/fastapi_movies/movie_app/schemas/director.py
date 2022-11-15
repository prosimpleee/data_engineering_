from pydantic import BaseModel


class DirectorBase(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class DirectorCreate(BaseModel):
    id: int


class DirectorSchemaOut(BaseModel):
    id: int
    last_name: str
    first_name: str

    class Config:
        orm_mode = True
