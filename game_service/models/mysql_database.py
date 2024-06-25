import requests
from models.database import Database
import mysql.connector



def get_db():
    db = Mysql_database()
    return db


class Mysql_database(Database):
    def __init__(self):
        self.config = {
            'user': 'root',
            #'host': 'mysql_db',
            'host' : 'localhost',
            'port': '3306',
            'database': 'db_pokemon'
        }

        self.connetion = self.connect()

    def connect(self):
        mydb = mysql.connector.connect(**self.config)
        return mydb

    
    def __execute_query(self, query, commit=False,fetch_all = False):
        mydb = self.connect()
        cursor = mydb.cursor()
        cursor.execute(query)
        if commit:
            mydb.commit()
            return
        if fetch_all:
            query_res = cursor.fetchall()
            return [list(inner_list) for inner_list in query_res] or None
        return cursor.fetchone()
        
    
    def get_pokemon_by_id(self, id: int):
        query = f"""SELECT * FROM pokemons WHERE id = '{id}'"""
        return self.__execute_query(query)
    
    def get_pokemon_by_name(self, name: str):
        query = f"""SELECT * FROM pokemons WHERE name = '{name}'"""
        return self.__execute_query(query)
    
    def get_pokemon_by_type(self, type: str):
        query = f"SELECT p.name FROM pokemons p join pokemonsTypes pt on  p.id = pt.pokemon_id where pt.type_name = '{type}'"
        return self.__execute_query(query,fetch_all=True)
    
    def get_pokemons_by_trainer(self, trainer: str):
        query = f"""
        SELECT p.name
        FROM pokemons p
        JOIN team ON p.id = team.pokemon_id
        JOIN trainers t ON t.id = team.trainer_id
        WHERE t.name = '{trainer}';
        """
        return self.__execute_query(query,fetch_all=True)

    
    def get_trainer_by_id(self, id: int):
        query = f"""SELECT * FROM trainers WHERE id = '{id}'"""
        return self.__execute_query(query)
    
    def get_trainer_by_name(self, name: str):
        query = f"""SELECT * FROM trainers WHERE name = '{name}'"""
        return self.__execute_query(query)
    
    def get_all_trainers(self):
        query = "SELECT * FROM trainers"
        return self.__execute_query(query,fetch_all=True)
    
    def get_trainers_of_pokemon(self, pokemon: str):
        query = f"SELECT t.name FROM trainers t join team on  t.id = team.trainer_id where team.pokemon_id = '{pokemon}'"
        return self.__execute_query(query,fetch_all=True)
    
    def add_pokemonsTypes(self, pokemon_id: int, types: list):
        for type in types:
            query = f"""INSERT INTO pokemonsTypes (type_name, pokemon_id) VALUES ('{type}', {pokemon_id})"""
            self.__execute_query(query, commit=True)
        return True

    def add_type_to_typesTable(self, type: str):
        query = f"""INSERT INTO types (name) VALUES ('{type}')"""
        self.__execute_query(query, commit=True)
        return True

    def add_trainer_to_TrainerTable(self, name: str, town: str):
        query = f"""INSERT INTO trainers (name,town) VALUES ('{name}','{town}')"""
        self.__execute_query(query, commit=True)
        return True

    def add_pokemon_to_trainer(self, trainer_id,pokemon_id):
        query = f"""INSERT INTO team (trainer_id,pokemon_id) VALUES ('{trainer_id}', {pokemon_id})"""
        self.__execute_query(query, commit=True)
        return True
    
    def add_pokemon(self, data):
        query = f"INSERT INTO pokemons (id, name, height, weight) VALUES ({data[0]},'{data[1]}', {data[2]}, {data[3]});"
        try:

            self.__execute_query(query, commit=True)
            return True
        except Exception as e:
            print(f"Error occurred: {e}")
            return False

    def check_trainer_and_pokemon(self, pokemon_id: int, trainer_id:int):
        query = f"SELECT * from team where trainer_id={trainer_id} and pokemon_id={pokemon_id}"
        if self.__execute_query(query):
            return True
        return False

    def delete_pokemon(self,pokemon_id, trainer_id):
        query = f"DELETE FROM team WHERE trainer_id = {trainer_id} AND pokemon_id = {pokemon_id};"
        self.__execute_query(query,commit=True)
        


   