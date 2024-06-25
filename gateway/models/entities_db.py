import requests
from utils.route_generator import Route_generator as Generator

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
    
    def add_pokemon(self,pokemon):
        url = self.generator.generate_route("pokemon/",params={"pokemon": pokemon})
        requests.post(url).json()
        return True
    
class PokeAPI_Entities(Entities):
    def get_pokemons_evolve_chain(self, pokemon_name):
        """
            retrieve a pokemon chain by its name from PokeAPI
            :param pokemon: the name of pokemon to retrieve
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