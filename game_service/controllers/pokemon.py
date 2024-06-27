from typing import Optional

from fastapi import APIRouter, HTTPException, Query, Depends
from models.mysql_database import get_db
from models.schema import Pokemon

router = APIRouter(
    prefix='/pokemon',
    tags=['This is all  requests for pokemon resources ']
)


@router.get("/")
def get_pokemon(pokemon_id: Optional[int]=Query(None), pokemon_name: Optional[str]=Query(None),pokemon_type: Optional[str]=Query(None), pokemon_db=Depends(get_db)):
    """
    retrieve a pokemon by its id or its name or gets all the pokemons of the type 
    :param pokemon_id: the id of pokemon to retrieve
    :param pokemon_name: the name of pokemon to retrieve
    :param pokemon_type: the type of pokemon to retrieve
    :param pokemon_db: Dependency to fetch the database.
    :return: pokemon data or none if not found
    """
    if pokemon_id:
        return pokemon_db.get_pokemon_by_id(pokemon_id)
    if pokemon_name:
        return pokemon_db.get_pokemon_by_name(pokemon_name)
    if pokemon_type:
        res =  pokemon_db.get_pokemon_by_type(pokemon_type)
        print(res)
        return res 
    raise HTTPException(status_code=400, detail="No Id, name or type was given")


@router.get("/trainers")
def get_pokemon_trainer(pokemon_name:str,pokemon_db=Depends(get_db))-> list | None:
    """
    Retrieves a list of trainers who own a Pokemon with the given name.
    :param pokemon_name: the name of the pokemon to search for.
    :param pokemon_db: Dependency to fetch the db
    :return: A list of trainers who own pokemon
    """
    return pokemon_db.get_trainers_of_pokemon(pokemon_name)


@router.post("/")
def create_pokemon(pokemon: Pokemon, pokemon_db=Depends(get_db)):
    """

    :param pokemon:  the pokemon data to be created
    :param pokemon_db:  Dependency to fetch the database.
    :return:
    """
    pokemon_data = [pokemon.id, pokemon.name, pokemon.height, pokemon.weight]
    pokemon_added = pokemon_db.add_pokemon(pokemon_data)
    pokemon_db.add_pokemonsTypes(pokemon.id, pokemon.types)

    if pokemon_added:
        return {"message": "Pokemon added successfully."}
    raise HTTPException(status_code=400, detail="someting went wrong!")
    
@router.delete("/")
def delete_pokemon_from_trainer(trainer_id: str, pokemon_id: str, pokemon_db=Depends(get_db)):
    """
    delete a pokemon owned by trainer
    :param trainer_name: the name of trainer who own a pokemon to be deleted..
    :param pokemon_name: the name of pokemon to be deleted
    :param pokemon_db: Dependency to fetch the database.
    :return:
    """
    pokemon_db.delete_pokemon(pokemon_id,trainer_id)
    return {"message": "Pokemon deleted successfully"}
    
    
