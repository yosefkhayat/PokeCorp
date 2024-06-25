from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from models.mysql_database import  get_db

router = APIRouter(
    prefix='/trainer',
    tags=['This is all  requests for trainers resources ']
)


@router.get("/")
def get_trainer(trainer_id: Optional[int]=Query(None), trainer_name: Optional[str]=Query(None), pokemon_db=Depends(get_db)):
    """
    retrieve a trainer by its id or name
    :param pokemon_id: the id of pokemon to retrieve
    :param pokemon_db: Dependency to fetch the database.
    :return: trainer data
    """
    if trainer_id:
        return pokemon_db.get_trainer_by_id(trainer_id) 
    if trainer_name:
        return pokemon_db.get_trainer_by_name(trainer_name)
    raise HTTPException(status_code=400, detail="No Id, name or type was given")

@router.get("/pokemon-exist")
def pokemon_exist_in_trainer(trainer_id, pokemon_id, pokemon_db=Depends(get_db)):
    """
    checks a pokemon and trainer comination
    :param pokemon_id: the id of pokemon to check
    :param trainer_id: the id of trainer to check
    :param pokemon_db: Dependency to fetch the database.
    :return: pokemon data
    """
    if pokemon_db.check_trainer_and_pokemon(pokemon_id, trainer_id):
        return {"message": "trainer and pokemon are team!"}
    raise HTTPException(status_code=404, detail="trainer and pokemon are not team!")

@router.get("/pokemons")
def get_trainer(trainer_name:str, pokemon_db=Depends(get_db)):
    """
    retrieve a pokemon by its id
    :param pokemon_id: the id of pokemon to retrieve
    :param pokemon_db: Dependency to fetch the database.
    :return: pokemon data
    """
    return pokemon_db.get_pokemons_by_trainer(trainer_name)


@router.post("/")
def add_pokemon_to_trainer(trainer_id, pokemon_id, pokemon_db=Depends(get_db)):
    if pokemon_db.add_pokemon_to_trainer(trainer_id,pokemon_id):
        return {"message":"successfuly add pokemon to trainer"}