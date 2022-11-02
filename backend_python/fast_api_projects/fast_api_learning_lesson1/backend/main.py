

from fastapi import FastAPI
from routers.players_router import players_router

app = FastAPI(
    title='Lesson_1',
    version='0.0.1'
)


app.include_router(players_router)
