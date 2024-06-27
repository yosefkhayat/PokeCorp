from fastapi import FastAPI
import uvicorn

from controllers import pokemon, trainer

server = FastAPI()
server.include_router(pokemon.router)
server.include_router(trainer.router)


    
#test the server is up
@server.get("/test")
def test():
    return {"msg":"server is working properly"}

