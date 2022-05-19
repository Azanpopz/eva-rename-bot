from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram import Client, filters
import asyncio

api_id: int = 1778836
api_hash: str = "7bcf61fcd32b8652cd5876b02dcf57ae"
token: str = "5328651309:AAFx1aoxzzEpK4-KxC4Ay03qd4rXDTEgrPM"



DONATESTARTTEXT: str = """
text  
"""


@Client.on_message(filters.service)
async def service(client, Message):
    await asyncio.sleep(60)
    await Message.delete()


@Client.on_message(filters.private)
async def start(client, Message):
    await Message.reply(
        DONATESTARTTEXT,
    )


@Client.on_message(filters.group & filters.command("command@botname"))
async def main(client, Message):
    await Message.reply("""text""")


@Client.on_message(filters.group & filters.command("command"))
async def main(client, Message):
    await Message.reply("""text""")



