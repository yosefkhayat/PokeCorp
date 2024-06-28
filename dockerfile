# 
FROM python:3.11.3

# 
COPY ./requirements.txt /requirements.txt

# 
RUN pip install --no-cache-dir --upgrade -r /requirements.txt


COPY ./json_migration.py /
COPY ./pokemons_data.json /
CMD sh -c "sleep 250 && python /json_migration.py "