import os
from dotenv import load_dotenv
from pymongo import MongoClient
import certifi 

load_dotenv()

MONGO_URI = os.getenv("MONGO")
DB = os.getenv("DB")


client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())

db = client[DB]
user_collections = db["users"]
