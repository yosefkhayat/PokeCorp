from fastapi import FastAPI
import uvicorn

from controllers import pokemon, trainer

server = FastAPI()
server.include_router(pokemon.router)
server.include_router(trainer.router)


if __name__ == "__main__":
    uvicorn.run(server, host="0.0.0.0", port=8000)
    
#test the server is up
@server.get("/")
def test():
    return {"msg":"server is working properly"}

