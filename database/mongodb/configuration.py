from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://root:root@cluster0.doahzj4.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# create or select database
mongo_db = client.files

# create or select table
mongo_db_collection = mongo_db['files']