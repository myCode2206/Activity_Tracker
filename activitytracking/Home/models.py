# from django.db import models
from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client["MynewDB"]


person_collection=db['user']