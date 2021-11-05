import asyncio
import sys

from motor import motor_asyncio
from mrjoker import MONGO_DB_URL
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError


MONGO_DB = "MrJoker"


client = MongoClient()
client = MongoClient(MONGO_DB_URL, 27017)[MONGO_DB]
motor = motor_asyncio.AsyncIOMotorClient(MONGO_DB_URL, 27017)
db = motor[MONGO_DB]
db = client["mrjoker"]

try:
    asyncio.get_event_loop().run_until_complete(motor.server_info())
except ServerSelectionTimeoutError:
    sys.exit(log.critical("Can't connect to mongodb! Exiting..."))
