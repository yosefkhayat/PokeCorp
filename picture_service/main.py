from typing import Optional
from fastapi import Depends, FastAPI, HTTPException, Query
import requests
import uvicorn
from models.mongo_db import get_db

#from controllers import pokemon#, trainer

server = FastAPI()
#server.include_router(pokemon.router)

if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8000)



@server.get("/test")
def test():
    return {"message":"server is working properly!"}

@server.get("/" )
def get_image_by_name(image_name, pokemon_db=Depends(get_db)):
    fs = pokemon_db.find_image_by_name(image_name)
    return pokemon_db.read_image(fs)


@server.delete("/" )
def delete_image_by_id(image_id, pokemon_db=Depends(get_db)):
    fs =  pokemon_db.find_image_by_name(image_id)
    return pokemon_db.read_image(fs)

@server.post("/")
def insert_image(image_url,pokemon_name, pokemon_db=Depends(get_db)):
    return pokemon_db.insert_image_from_url(image_url,pokemon_name)
