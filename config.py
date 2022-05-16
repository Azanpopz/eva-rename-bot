"""Importing"""
from os import environ
import os

class Config(object):
    API_ID = int(environ.get("API_ID", 0))
    API_HASH = environ.get("API_HASH", "")
    BOT_TOKEN = environ.get("BOT_TOKEN", "")
    DATABASE_URI = environ.get("DATABASE_URI", "")







class Con(object):
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "") # Make a bot from https://t.me/BotFather and enter the token here
    
    APP_ID = int(os.environ.get("API_ID", 12345)) # Get this value from https://my.telegram.org/apps
    
    API_HASH = os.environ.get("API_HASH", "") # Get this value from https://my.telegram.org/apps
    
    OWNER_ID = int(os.environ.get("OWNER_ID", None)) # Your(owner's) telegram id
    
    DATABASE_URI = os.environ.get("DATABASE_URI", "") # Get from MongoDB Atlas

    DOWNLOAD_LOCATION = "app//DOWNLOADS//" # The download location for users. (Don't change anything in 
