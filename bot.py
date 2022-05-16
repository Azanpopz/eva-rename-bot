import logging
import logging.config

# Get logging configurations
logging.config.fileConfig('logging.conf')
logging.getLogger().setLevel(logging.INFO)
logging.getLogger("pyrogram").setLevel(logging.ERROR)
logging.getLogger("imdbpy").setLevel(logging.ERROR)

from pyrogram import Client, __version__
from pyrogram.raw.all import layer
from database.ia_filterdb import Media
from database.users_chats_db import db
from info import SESSION, API_ID, API_HASH, BOT_TOKEN, LOG_STR   


from utils import temp


from pyrogram import Client
import os


from config import *



#!/usr/bin/env python3


"""Importing"""
# Importing External Packages
from pyrogram import Client, idle

# Importing Inbuilt Packages
import logging
from os import path, makedirs, remove

# Importing Credentials & Required Data
try:
    from testexp.config import Con
except ModuleNotFoundError:
    from config import Con


'''For Displaying Errors&Warnings Better'''
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)

# No task on staring bot
try:
    remove('task.txt')
except FileNotFoundError:
    pass

"""Starting Bot"""
if __name__ == "__main__" :
    # Creating download directories, if they does not exists
    if not path.isdir(Config.DOWNLOAD_LOCATION):
        makedirs(Con.DOWNLOAD_LOCATION)
    plugins = dict(
        root="plugins"
    )
    app = Client(
        "URL_Uploader",
        bot_token=Con.BOT_TOKEN,
        api_id=Con.APP_ID,
        api_hash=Con.API_HASH,
        plugins=plugins
    )











BOT_TOKEN = os.environ.get("BOT_TOKEN", "")

API_ID = int(os.environ.get("API_ID", ""))

API_HASH = os.environ.get("API_HASH", "")

if __name__ == "__main__" :
    plugins = dict(
        root="plugins"
    )
    app = Client(
        "renamer",
        bot_token=BOT_TOKEN,
        api_id=API_ID,
        api_hash=API_HASH,
        plugins=plugins
    )






class Bot(Client):

    def __init__(self):
        super().__init__(
            session_name=SESSION,
            api_id=API_ID,
            api_hash=API_HASH,
            bot_token=BOT_TOKEN,            
            workers=50,
            plugins={"root": "plugins"},
            sleep_threshold=5,
            parse_mode="html",
        )
    
    async def start(self):
        b_users, b_chats = await db.get_banned()
        temp.BANNED_USERS = b_users
        temp.BANNED_CHATS = b_chats
        await super().start()
        await Media.ensure_indexes()
        me = await self.get_me()
        temp.ME = me.id
        temp.MENTION = me.mention
        temp.U_NAME = me.username
        temp.B_NAME = me.first_name
        self.username = '@' + me.username
        logging.info(f"{me.first_name} with for Pyrogram v{__version__} (Layer {layer}) started on {me.username}.")
        logging.info(LOG_STR)

    async def stop(self, *args):
        await super().stop()
        logging.info("Bot stopped. Bye.")


app = Bot()
app.run()
