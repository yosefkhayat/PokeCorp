import io
import json
import mysql.connector
import requests
import pymongo
from gridfs import GridFS

JSON_URL="./pokemons_data.json"
POKEMONAPI_URL = "https://pokeapi.co/api/v2/pokemon/"

MYSQL_CONFIG = {
    'user': 'root',
    'host': 'mysql_container',
    'port': '3306',
    'database': 'db_pokemon'
}

MONGO_CONFIG = {
    "url":"mongodb://mongo_container:27017/",
    "database":"pictures"
}

def read_json():
    with open(JSON_URL, 'r') as file:
        data = json.load(file)
    return data


mydb = mysql.connector.connect(**MYSQL_CONFIG)
cursor = mydb.cursor()

myclient = pymongo.MongoClient(MONGO_CONFIG["url"])
mongodb = myclient[MONGO_CONFIG["database"]]
fs = GridFS(mongodb)


db = read_json()
types=[]
""" Pokemons"""
for pokemon in db:
    sql_insert_query = """
    INSERT INTO pokemons (id, name, height, weight)
    VALUES (%s, %s, %s, %s);
    """
    pokemons_data = (pokemon["id"], pokemon["name"], pokemon["height"], pokemon["weight"])
    cursor.execute(sql_insert_query, pokemons_data)
    name = pokemon["name"]
    url=f"{POKEMONAPI_URL}{name}"
    response = requests.get(url).json()
    picture_url = response["sprites"]["front_default"]
    image_response = requests.get(picture_url)
    image_data = image_response.content
    image_stream = io.BytesIO(image_data)
    fs.put(image_stream, filename=pokemon["name"])
    for t in response["types"]:
        type= t["type"]["name"]
        if type not in types:
            sql_insert_query = """
            INSERT INTO types (name)
            VALUES (%s);
            """
            types.append(type)
            cursor.execute(sql_insert_query, (type,))
        sql_insert_query = """
        INSERT INTO pokemonsTypes (type_name,pokemon_id)
        VALUES (%s,%s);
        """
        cursor.execute(sql_insert_query, (type,pokemon["id"]))
    
mydb.commit()

names_owners=[]
for pokemon in db:
    for owner in pokemon["ownedBy"]:
        if owner["name"]not  in names_owners:
            sql_insert_query = """
                         INSERT INTO trainers (name,town)
                         VALUES (%s,%s);
                         """
            names_owners.append(owner["name"])
            cursor.execute(sql_insert_query, (owner["name"], owner["town"]))
mydb.commit()



dict_trainer={}
sql_select_trainers = """
        select * from trainers
        """
cursor.execute(sql_select_trainers)

rows = cursor.fetchall()
for row in rows:
    dict_trainer[row[1]]=row[0]

for pokemon in db:
    for trainer in pokemon["ownedBy"]:
        sql_insert_query = """
        INSERT INTO team (trainer_id,pokemon_id)
        VALUES (%s,%s);
        """
        cursor.execute(sql_insert_query, (dict_trainer[trainer["name"]],pokemon["id"]))

mydb.commit()

cursor.close()
mydb.close()