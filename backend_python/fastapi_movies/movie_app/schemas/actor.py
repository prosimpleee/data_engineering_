from pydantic import BaseModel


class ActorBase(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class ActorSchemeCreate(ActorBase):
    pass


class ActorSchemeOut(BaseModel):
    id: int


class ActorCreate(BaseModel):
    id: int


class ActorGet(ActorBase):
    id: int

    class Config:
        schema_extra = {
            "example": {
                "first_name": "Denzel",
                "last_name": "Washington",
            }
        }