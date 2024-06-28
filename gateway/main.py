from typing import Optional
from fastapi import  FastAPI, HTTPException, Query



from models.entities_db import MySQL_Entities, PokeAPI_Entities, Images_Entities
from models.schema import Pokemon

#from controllers import pokemon#, trainer

server = FastAPI()
#server.include_router(pokemon.router)
e = MySQL_Entities("game_service_container:8000", "http")
pokeApi = PokeAPI_Entities("pokeapi.co/api/v2/pokemon/","https")
image_service = Images_Entities("picture_container:8002","http")
# if __name__ == "__main__":
#     uvicorn.run(server, host="0.0.0.0", port=8001)

@server.get("/pokemon")
def get_pokemon_specie(pokemon_specie):
    """
    retreive pokemon specie by name
    :param pokemon_specie: the name of the specie
    :return: id, name, height, weight, types (all of them). And the Pokémon image 
    """
    pokemon_details = e.get_pokemon_by_name(pokemon_specie)
    if not pokemon_details:
            raise HTTPException(status_code=404, detail="No Pokemon found for the given name")
    image = image_service.get_image_by_pokemon_name(pokemon_specie)
    pokemon ={ "id": pokemon_details[0], "name":pokemon_details[1], "height" : pokemon_details[2], "weight" : pokemon_details[3], "types": pokemon_details[4], "image": image}
    return pokemon

@server.get("/")
def get_pokemon_with_filtering(pokemon_name:Optional[str]=Query(None), pokemon_type: Optional[str] = Query(None)):
    """
    retreive pokemon with optinal filetering by trainer_name or pokemon type
    :param pokemon_name: the names of the trainers to filter by
    :param pokemon_type: the type of pokemon to filter by
    :return:
    """
    if pokemon_name:
        pokemon = e.get_pokemon_by_name(pokemon_name) 
        if not pokemon:
            raise HTTPException(status_code=404, detail="No Pokemon found for the given name")
        trainers = e.get_pokemon_trainers(pokemon[0])
        return trainers or {"message":"the pokemon has No trainers yet!"}
        
    if pokemon_type:
        pokemons = e.get_pokemon_by_type(pokemon_type)
        if not pokemons:
            raise HTTPException(status_code=404, detail="No Pokemon found for the given type")
        return pokemons

    raise HTTPException(status_code=400, detail="At least one search parameter must be provided")

@server.get("/trainer")
def get_pokemons_by_trainer(trainer_name:str):
    """
    retreive all pokemons by trainer name
    :param trainer_name: the name of trainer to get all of his pokemons
    :return: list of pokemons
    """
    if not e.get_trainer_by_name(trainer_name):
            raise HTTPException(status_code = 400,detail="No trainer with this name in the database")
    pokemons = e.get_pokemon_by_trainer(trainer_name)
    if not pokemons:
        raise HTTPException(status_code=404, detail="No Pokemon found for the given trainer")
    return pokemons


@server.delete("/")
def delete_pokemon_from_trainer(trainer_name: str, pokemon_name: str):
    """
    delete a pokemon owned by trainer
    :param trainer_name: the name of trainer who own a pokemon to be deleted..
    :param pokemon_name: the name of pokemon to be deleted
    :param pokemon_db: Dependency to fetch the database.
    :return:
    """
    pokemon = e.get_pokemon_by_name(pokemon_name)
    if not pokemon:
            raise HTTPException(status_code = 400,detail="No pokemon with this name in the database")
    trainer = e.get_trainer_by_name(trainer_name)
    if not trainer:
            raise HTTPException(status_code = 400,detail="No trainer with this name in the database")
    if not e.check_pokemon_is_with_trainer(pokemon[0],trainer[0]):
         raise HTTPException(status_code = 400,detail="pokemon and trainer is not team!")
    e.delete_pokemon_from_trainer(pokemon[0],trainer[0])
    
    return {"message": "Pokemon deleted successfully"}

@server.post("/trainer")
def add_pokemon_to_trainer(pokemon_name: str, trainer_name: str):
    """
    :param trainer_id: the id of trainer who will own the pokemon
    :param pokemon_id: the Id of pokemon to be added
    :param pokemon_db: Dependency to fetch the db
    :return: None
    """
    pokemon = e.get_pokemon_by_name(pokemon_name)
    if not pokemon:
            raise HTTPException(status_code = 400,detail="No pokemon with this name in the database")
    trainer = e.get_trainer_by_name(trainer_name)
    if not trainer:
            raise HTTPException(status_code = 400,detail="No trainer with this name in the database")
    if e.check_pokemon_is_with_trainer(pokemon[0],trainer[0]):
         raise HTTPException(status_code = 400,detail="pokemon and trainer is team!")
    if e.add_pokemon_to_trainer(pokemon[0], trainer[0]):
        print("Pokemon added successfully to trainer.")
        return {"message": "Pokemon added successfully to trainer."}

@server.post("/")
def create_pokemon(pokemon_name):
    """
    :param pokemon:  the pokemon data to be created
    :param pokemon_db:  Dependency to fetch the database.
    :return:
    """
    existing_pokemon = e.get_pokemon_by_name(pokemon_name)
    if existing_pokemon:
        raise HTTPException(status_code=409, detail="Pokemon found with the given name")
    pokemon = pokeApi.get_pokemon_from_api(pokemon_name)
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found with the given name in the pokeApi")
    image_url= pokeApi.get_image_url(pokemon_name)
    if not image_url:
        raise HTTPException(status_code=404, detail="Pokemon image not found with the given name in the pokeApi")
    pokemon_added = e.add_pokemon(pokemon)
    if pokemon_added:
        image_service.post_image_by_pokemon_name(pokemon_name,image_url)
        return {"message": "Pokemon added successfully."}
    
@server.post("/evolve-pokemon")
def evolve_pokemon(pokemon_name:str,trainer_name:str):
    """

    :param pokemon: the name of pokemon to be envolved.
    :param trainer: the name of trainer who own the pokemon
    :param pokemon_db:  Dependency to fetch the database.
    :return:
    """
    pokemon_id = e.get_pokemon_by_name(pokemon_name)[0]
    if not pokemon_id:
        raise HTTPException(status_code=404, detail="No Pokémon found with the given name")
    trainer_id = e.get_trainer_by_name(trainer_name)[0]
    if not trainer_id:
        raise HTTPException(status_code=404, detail="No Trainer found with the given name")
    if not e.check_pokemon_is_with_trainer(pokemon_id,trainer_id):
        raise HTTPException(status_code=400, detail="Pokémon is not in trainer hand")
    evolved_pokemon = pokeApi.get_next_evolve_pokemon_name(pokemon_name)   
    if not evolved_pokemon:
        raise HTTPException(status_code=403, detail="Pokémon has reach max evoloution")
    evolved_pokemon_id = e.get_pokemon_by_name(evolved_pokemon)[0]
    if not evolved_pokemon_id:
        create_pokemon(evolved_pokemon)
        evolved_pokemon_id = e.get_pokemon_by_name(evolved_pokemon)[0]
    if e.check_pokemon_is_with_trainer(evolved_pokemon_id,trainer_id):
        raise HTTPException(status_code=400, detail="can't evolve Pokémon, the trainer has the evolved pokemon in hand")
    e.delete_pokemon_from_trainer(pokemon_id,trainer_id)
    pokemon_evolved = e.add_pokemon_to_trainer(evolved_pokemon_id,trainer_id)
    if pokemon_evolved:
        print("Pokemon evolved successfully.")
        return {"message": "Pokemon evolved successfully."}


