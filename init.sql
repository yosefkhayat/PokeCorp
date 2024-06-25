CREATE DATABASE db_pokemon;

USE db_pokemon;

CREATE TABLE pokemons (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    height FLOAT NOT NULL,
    weight FLOAT NOT NULL
);

CREATE TABLE trainers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    town VARCHAR(100) NOT NULL
);

CREATE TABLE team (
    trainer_id INT,
    pokemon_id INT,
    PRIMARY KEY (trainer_id, pokemon_id),
    FOREIGN KEY (trainer_id) REFERENCES trainers(id) ON DELETE CASCADE,
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE
);

CREATE TABLE types (
    name VARCHAR(100) PRIMARY KEY NOT NULL
);

CREATE TABLE pokemonsTypes (
    type_name VARCHAR(100),
    pokemon_id INT,
    PRIMARY KEY (type_name, pokemon_id),
    FOREIGN KEY (type_name) REFERENCES types(name) ON DELETE CASCADE,
    FOREIGN KEY (pokemon_id) REFERENCES pokemons(id) ON DELETE CASCADE
);