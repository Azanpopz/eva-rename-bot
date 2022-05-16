"""Importing"""
from os import environ


class Config(object):
    API_ID = int(environ.get("API_ID", 0))
    API_HASH = environ.get("API_HASH", "")
    BOT_TOKEN = environ.get("BOT_TOKEN", "")
    DATABASE_URI = environ.get("DATABASE_URI", "")
