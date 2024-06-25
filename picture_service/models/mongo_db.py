from pymongo import MongoClient
from gridfs import GridFS
import requests
import io


def get_db():
    db = MongoDB(db_name='pokemon_pics')
    return db

class MongoDB:
    def __init__(self, host='localhost', port=27017, db_name=None):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.client = None
        self.db = None
        self.fs = None
        self.connect()
    
    def connect(self):
        self.client = MongoClient(self.host, self.port)
        if self.db_name:
            self.db = self.client[self.db_name]
            self.fs = GridFS(self.db)
    
    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None
            self.fs = None
    
    def insert_image_from_url(self, image_url, image_name=None):
        if self.fs:
            response = requests.get(image_url)
            if response.status_code == 200:
                image_data = response.content
                image_stream = io.BytesIO(image_data)
                return self.fs.put(image_stream, filename=image_name)
            else:
                raise Exception(f"Failed to fetch image from URL: {image_url}")
        else:
            raise Exception("Database is not connected.")
    
    def find_image_by_id(self, image_id):
        if self.fs:
            return self.fs.get(image_id)
        else:
            raise Exception("Database is not connected.")
    
    def find_image_by_name(self, image_name):
        if self.fs:
            return self.fs.find_one({'filename': image_name})
        else:
            raise Exception("Database is not connected.")
    
    def delete_image(self, image_id):
        if self.fs:
            self.fs.delete(image_id)
        else:
            raise Exception("Database is not connected.")
        
    def read_image(self, image):
        if image:
            # Read the data from GridFS
            file_data = image.read()

            # Convert the data to BytesIO object
            return io.BytesIO(file_data)
        else:
            return None

