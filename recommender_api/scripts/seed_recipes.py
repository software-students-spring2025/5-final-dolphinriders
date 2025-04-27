#!/usr/bin/env python
import os, json
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # reads MONGO_URI & DB_NAME from ../.env

client = MongoClient(os.getenv("MONGO_URI"))
db = client[os.getenv("DB_NAME")]

# load your starter data
with open("starter_recipes.json") as f:
    docs = json.load(f)

# clear out old data & insert
db.recipes.delete_many({})
res = db.recipes.insert_many(docs)
print(f"Seeded {len(res.inserted_ids)} recipes.")
