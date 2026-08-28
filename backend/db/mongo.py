from pymongo import MongoClient
from config import MONGO_URI, MONGO_DB_NAME

_client = MongoClient(MONGO_URI)
db = _client[MONGO_DB_NAME]
