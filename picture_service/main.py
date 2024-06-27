
from fastapi import Depends, FastAPI, HTTPException, Query
from models.mongo_db import get_db


server = FastAPI()


@server.get("/test")
def test():
    return {"message":"server is working properly!"}

@server.get("/" )
def get_image_by_name(pokemon_name:str, pokemon_db=Depends(get_db)):
    """
    getting an image from the mongodb database
    :param pokemon_name:  the pokemon data to be created
    :param pokemon_db:  Dependency to fetch the database.
    :return: image in Bytes format
    """
    fs = pokemon_db.find_image_by_name(pokemon_name)
    if fs:
        return pokemon_db.read_image(fs)
    raise HTTPException(status_code=404, detail="pokemon image not exist!")
    


@server.delete("/" )
def delete_image_by_id(image_name, pokemon_db=Depends(get_db)):
    """
    deleting an image from the mongodb database
    :param pokemon_name:  the pokemon data to be deleted
    :param pokemon_db:  Dependency to fetch the database.
    :return: 200 ok
    """
    fs = pokemon_db.find_image_by_name(image_name)
    if fs:
        pokemon_db.delete_image(fs._id)
        return {"messege":"deleted successfully!"}
    raise HTTPException(status_code=404, detail="pokemon image not exist!")
    

@server.post("/")
def insert_image(image_url,pokemon_name, pokemon_db=Depends(get_db)):
    """
    adding an image to the mongodb database
    :param pokemon_name:  the pokemon data to be created
    :param image_url:  the pokemon image url to be download and save in the database
    :param pokemon_db:  Dependency to fetch the database.
    :return: 200 ok
    """
    fs = pokemon_db.find_image_by_name(pokemon_name)
    if not fs:
        pokemon_db.insert_image_from_url(image_url,pokemon_name)
        return {"messege":"image added successfully!"}
    raise HTTPException(status_code=400, detail="pokemon image exists!")