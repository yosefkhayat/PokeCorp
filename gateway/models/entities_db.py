import requests
from utils.route_generator import Route_generator as Generator
from models.schema import Pokemon

class Entities():
    def __init__(self,domain:str, protocol:str ,) -> None:
        self.generator = Generator(protocol=protocol,domain=domain)

class MySQL_Entities(Entities):
    def get_pokemon_by_name(self,pokemon_name):
        url = self.generator.generate_route("pokemon/", params={"pokemon_name":pokemon_name})
        pokemon = requests.get(url).json()
        return pokemon
    def get_pokemon_by_id(self,pokemon_id):
        url = self.generator.generate_route("pokemon/", params={"pokemon_id":pokemon_id})
        pokemon = requests.get(url).json()
        return pokemon
    
    def get_pokemon_by_type(self,pokemon_type):
        url = self.generator.generate_route("pokemon/", params={"pokemon_type":pokemon_type})
        pokemon = requests.get(url).json()
        return pokemon
    def get_pokemon_trainers(self,pokemon_name):
        url = self.generator.generate_route("pokemon/trainers",params={"pokemon_name":pokemon_name})
        pokemon = requests.get(url).json()
        return pokemon
    def get_trainer_by_name(self,trainer_name):
        url = self.generator.generate_route("trainer/",params={"trainer_name":trainer_name})
        trainer = requests.get(url).json()
        return trainer
    def get_pokemon_by_trainer(self,trainer_name):
        url = self.generator.generate_route("trainer/pokemons",params={"trainer_name":trainer_name})
        pokemon = requests.get(url).json()
        return pokemon
    def check_pokemon_is_with_trainer(self, pokemon_id, trainer_id):
        url = self.generator.generate_route("trainer/pokemon-exist",params={"trainer_id": trainer_id, "pokemon_id": pokemon_id})
        if requests.get(url).status_code == 200:
            return True
        return False
    def delete_pokemon_from_trainer(self, pokemon_id, trainer_id):
        url = self.generator.generate_route("pokemon/",params={"trainer_id": trainer_id, "pokemon_id": pokemon_id})
        requests.delete(url).json()
        return
    def add_pokemon_to_trainer(self, pokemon_id, trainer_id):
        url = self.generator.generate_route("trainer/",params={"trainer_id": trainer_id, "pokemon_id": pokemon_id})
        requests.post(url).json()
        return True
    
    def add_pokemon(self,pokemon:Pokemon):
        url = self.generator.generate_route("pokemon/")
        requests.post(url,json=pokemon.model_dump()).json()
        return True
    
class PokeAPI_Entities(Entities):
    def get_pokemon_from_api(self, pokemon_name):
        """
            retrieve a pokemon by its name from PokeAPI
            :param pokemon_name: the name of pokemon to retrieve
            :return: pokemon  chain data
        """
        url = self.generator.generate_route(pokemon_name)
        response = requests.get(url)
        if response.status_code==404:
            return None
        response = response.json()
        
        pokemon_id = response["id"]
        name= response["name"]
        height= response["height"]
        weight= response["weight"]
        types = [inner_list["type"]["name"]for inner_list in response["types"]]
        pokemon = Pokemon(id=pokemon_id,name=name,height=height,weight=weight,types=types)
        return pokemon

    def get_pokemons_evolve_chain(self, pokemon_name):
        """
            retrieve a pokemon chain by its name from PokeAPI
            :param pokemon_name: the name of pokemon to retrieve
            :return: pokemon  chain data
        """
        url = self.generator.generate_route(pokemon_name)
        response = requests.get(url).json()
        species_url = response["species"]["url"]
        response = requests.get(species_url).json()
        evolution_chain = response["evolution_chain"]["url"]
        response = requests.get(evolution_chain).json()
        return response["chain"]
    
    def get_next_evolve_pokemon_name(self,pokemon):
        """
            retrieve a pokemon name after evolve from given name and check if volve possible
            :param pokemon: the name of pokemon to retrieve
            :return: pokemon  evolve pokemon name none if cant evolve
        """
        evolve_chain = self.get_pokemons_evolve_chain(pokemon)
        while(evolve_chain["species"]["name"] != pokemon):
                evolve_chain=evolve_chain["evolves_to"][0]
        try:
            result = evolve_chain["evolves_to"][0]["species"]["name"]
        except IndexError:
            return None
        return result
    
    def get_image_url(self, pokemon_name):
        url = self.generator.generate_route(pokemon_name)
        response = requests.get(url)
        if response.status_code==404:
            return None
        response = response.json()
        return response["sprites"]["front_default"]

class Images_Entities(Entities):
    def post_image_by_pokemon_name(self, pokemon_name,picture_url):
        url = self.generator.generate_route("",params={"image_url": picture_url,"pokemon_name": pokemon_name})
        requests.post(url).json()
        return
    def get_image_by_pokemon_name(self, pokemon_name):
        url = self.generator.generate_route("",params={"pokemon_name": pokemon_name})
        image = requests.get(url)
        return image

        