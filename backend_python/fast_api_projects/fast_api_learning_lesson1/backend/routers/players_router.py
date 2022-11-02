from fastapi import APIRouter, HTTPException
from starlette.responses import Response
from datetime import datetime
from typing import List

from routers.schemas import Player, PlayersList, UpdatePlayerSchema


our_players = [
    Player(id=1, name='Lionel Messi', username='messi19', age=35, created_at=datetime.now()),
    Player(id=2, name='Cristiano Ronaldo', username='criro7', age=37, created_at=datetime.now()),
    Player(id=3, name='Mike Maignan', username='maignan', age=25, created_at=datetime.now()),
    Player(id=4, name='Theo Hernandez', username='theo21', age=26, created_at=datetime.now())
    # The same, out object User with fields in User class
]

# GET, POST, PUT, DELETE + router
players_router = APIRouter(prefix='/players')

# GET method
@players_router.get('/all_players', name='all players', response_model=List[Player])
def all_players():
    return our_players


@players_router.get('/count_players', response_model=PlayersList)
def count_players():
    return PlayersList(count=len(our_players), players=our_players)


@players_router.get('/{player_id}', response_model=Player)
def only_one_player(player_id: int):
    for count, player in enumerate(our_players, start=1):
        if player.id == player_id:
            return player
    raise HTTPException(status_code=404, detail='Player Not Found')

# POST method
@players_router.post('/create_player', name='add new player', response_model=Player)
def create_player(player: Player):
    our_players.append(player)
    return player


# DELETE method
@players_router.delete('/{player_id}', name='Delete Player', response_class=Response)
def delete_player(player_id: int):
    for count, player in enumerate(tuple(our_players)):
        if player.id == player_id:
            del our_players[count]
            break
    return Response(status_code=204)


# PUT method
@players_router.put('/{player_id}', name='Update our player by player_id', response_model=Player)
def update_fields_player(player_id: int, new_player_fields: UpdatePlayerSchema):
    our_data = new_player_fields.dict()
    for index in range(len(our_players)):
        if our_players[index].id == player_id:
            for key in our_data:
                if our_data[key] is not None:
                    setattr(our_players[index], key, our_data[key])
            return our_players[index]
    raise HTTPException(status_code=404, detail='Player Not Found')
