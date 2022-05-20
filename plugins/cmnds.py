




import os
import logging
import random
import asyncio
from Script import script
from pyrogram import Client, filters
from database.batch_db import get_batch
from pyrogram.errors.exceptions.bad_request_400 import ChatAdminRequired
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from database.ia_filterdb import Media, get_file_details, unpack_new_file_id
from database.users_chats_db import db
from info import CHANNELS, ADMINS, ADMIN, AUTH_CHANNEL, CUSTOM_FILE_CAPTION, LOG_CHANNEL, STC
from utils import get_size, is_subscribed, temp
import re
logger = logging.getLogger(__name__)


@Client.on_message(filters.command("start"))
async def start(client, message):
    if message.chat.type in ['group', 'supergroup']:
        buttons = [            
            [
                InlineKeyboardButton('🕵️MENU🕵️', url=f"https://t.me/{temp.U_NAME}?start=menu"),
            ]
            ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply(script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME), reply_markup=reply_markup)
        await asyncio.sleep(2) # 😢 https://github.com/EvamariaTG/EvaMaria/blob/master/plugins/p_ttishow.py#L17 😬 wait a bit, before checking.
        if not await db.get_chat(message.chat.id):
            total=await client.get_chat_members_count(message.chat.id)
            await client.send_message(LOG_CHANNEL, script.LOG_TEXT_G.format(message.chat.title, message.chat.id, total, "Unknown"))       
            await db.add_chat(message.chat.id, message.chat.title)
        return 
    if not await db.is_user_exist(message.from_user.id):
        await db.add_user(message.from_user.id, message.from_user.first_name)
        await client.send_message(LOG_CHANNEL, script.LOG_TEXT_P.format(message.from_user.id, message.from_user.mention))
    if len(message.command) != 2:
        buttons = [[            
            InlineKeyboardButton('🕵️MENU🕵️', callback_data='menu'),          
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        if message.from_user.id == ADMIN:
            await message.reply_sticker(
                sticker=random.choice(STC),
                reply_markup=reply_markup,

            )
            return
        info = await client.get_users(user_ids=message.from_user.id)
        # await message.reply(
        #     chat_id=message.chat.id,
        #     text=script.START_TXT.format(message.from_user.mention if message.from_user else message.chat.title, temp.U_NAME, temp.B_NAME),
        #     reply_markup=reply_markup,
        # )
        await message.reply_sticker(
            sticker=random.choice(STC),
            reply_markup=reply_markup,

        )
        await client.send_message(
            chat_id=ADMIN,
            text=script.USER_DETAILS.format(
                info.first_name,
                info.last_name,
                info.id, info.username,
                info.is_scam,
                info.is_restricted,
                info.status,
                info.dc_id
            )
        )


        # await message.reply_sticker(
        #     sticker=random.choice(STC),
        #     reply_markup=reply_markup,
        #
        # )
        return
    if AUTH_CHANNEL and not await is_subscribed(client, message):
        try:
            invite_link = await client.create_chat_invite_link(int(AUTH_CHANNEL))
        except ChatAdminRequired:
            logger.error("Make sure Bot is admin in Forcesub channel")
            return
        btn = [
            [
                InlineKeyboardButton(
                    "📩𝐉𝐨𝐢𝐧 𝐔𝐩𝐝𝐚𝐭𝐞𝐬 𝐂𝐡𝐚𝐧𝐧𝐞𝐥📩", url=invite_link.invite_link
                )
            ]
        ]

        if message.command[1] != "subscribe":
            btn.append([InlineKeyboardButton("📥𝐓𝐫𝐲 𝐀𝐠𝐚𝐢𝐧📥", callback_data=f"checksub#{message.command[1]}")])
        await client.send_message(
            chat_id=message.from_user.id,
            text="**Please Join My Updates Channel to use this Bot!**",
            reply_markup=InlineKeyboardMarkup(btn),
            parse_mode="markdown"
            )
        return
    if len(message.command) ==2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
            InlineKeyboardButton('🕵️𝐇𝐞𝐥𝐩🕵️', callback_data='help'),
            InlineKeyboardButton('😊𝐀𝐛𝐨𝐮𝐭😊', callback_data='about')
        ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_sticker(
            sticker=random.choice(STC),
            reply_markup=reply_markup,

        )
        return
    file_id = message.command[1]
    print(file_id)
    unique_id, f_id, file_ref, caption = await get_batch("Eva-V3", file_id)

    if unique_id:
        temp_msg = await message.reply("⏳ Wait 30 seconds to get the next size files")
        file_args = f_id.split("#")
        cap_args = caption.split("#")
        i = 0
        await asyncio.sleep(3)
        
        
        for b_file in file_args:
            f_caption = cap_args[i]
            if f_caption is None:
                f_caption = ""
            f_caption = f_caption + f"\n\n<code>┈•••✿</code>😄😄😄<code>✿•••┈</code>"
            i += 1
            try:
                    k = await message.reply(f"⏳DOWNLOADING⏳◎ ◎")
                    await asyncio.sleep(1)
                    await k.delete()
                    k = await message.reply(f"⏳DOWNLOADING⏳◎ ◎ ◎ ◎")
                    await asyncio.sleep(1)
                    await k.delete()
                    
                    k = await client.send_cached_media(
                    chat_id=message.from_user.id,
                    file_id=b_file,
                    caption=f_caption,
                    parse_mode="html",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton(
                                    '🎭 ⭕️ ᴄᴏɴᴛᴀᴄᴛ ᴍᴇ ⭕️', url=f'https://t.me/mazhatthullikal'
                                )
                            ]
                        ]
                    )
                )
                         
                    
            except Exception as err:
                return await message.reply(f"{str(err)}")
            
        return await message.reply(f"<b><a href='https://t.me/NasraniChatGroup'>Thank For Using Me...</a></b>")
        


    files_ = await get_file_details(file_id)
    if not files_:
        return await message.reply('No such file exist.')
    files = files_[0]
    title = files.file_name
    size=get_size(files.file_size)
    f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=files.caption
    if CUSTOM_FILE_CAPTION:
        try:
            f_caption=CUSTOM_FILE_CAPTION.format(file_name=title, file_size=size, file_caption=f_caption)
        except Exception as e:
            logger.exception(e)
            f_caption=f_caption
    if f_caption is None:
        f_caption = f"{files.file_name}"
    
   
    buttons = [
                    [
                        InlineKeyboardButton('💌 SUBSCRIBE ✅', url=f"https://t.me/{temp.U_NAME}?start={file_id}")
                    ],
                    [
                        InlineKeyboardButton('💌 SUBSCRIBE ✅', url='https://t.me/bigmoviesworld'),
                        InlineKeyboardButton('💌 SUBSCRIBE ✅', url='https://t.me/bigmoviesworld')
                    ],
                    [
                        InlineKeyboardButton('💌 SUBSCRIBE ✅', url='https://t.me/bigmoviesworld'),
                        InlineKeyboardButton('💌 SUBSCRIBE ✅', url='https://t.me/bigmoviesworld')
                  
                    ]
                    ]
    k = await client.send_cached_media(
        chat_id=message.from_user.id,
        file_id=file_id,
        caption=f_caption,
        reply_markup=InlineKeyboardMarkup(buttons),
        parse_mode="html"
                
        )
    await message.reply(f"<b><a href='https://t.me/NasraniChatGroup'>Thank For Using Me...</a></b>")
    await message.reply_sticker(
            sticker=random.choice(STC),

        )
    


            







@Client.on_message(filters.command('channel') & filters.user(ADMINS))
async def channel_info(bot, message):
           
    """Send basic information of channel"""
    if isinstance(CHANNELS, (int, str)):
        channels = [CHANNELS]
    elif isinstance(CHANNELS, list):
        channels = CHANNELS
    else:
        raise ValueError("Unexpected type of CHANNELS")

    text = '📑 **Indexed channels/groups**\n'
    for channel in channels:
        chat = await bot.get_chat(channel)
        if chat.username:
            text += '\n@' + chat.username
        else:
            text += '\n' + chat.title or chat.first_name

    text += f'\n\n**Total:** {len(CHANNELS)}'

    if len(text) < 4096:
        await message.reply(text)
    else:
        file = 'Indexed channels.txt'
        with open(file, 'w') as f:
            f.write(text)
        await message.reply_document(file)
        os.remove(file)


@Client.on_message(filters.command('logs') & filters.user(ADMINS))
async def log_file(bot, message):
    """Send log file"""
    try:
        await message.reply_document('TelegramBot.log')
    except Exception as e:
        await message.reply(str(e))

@Client.on_message(filters.command('delete') & filters.user(ADMINS))
async def delete(bot, message):
    """Delete file from database"""
    reply = message.reply_to_message
    if reply and reply.media:
        msg = await message.reply("Processing...⏳", quote=True)
    else:
        await message.reply('Reply to file with /delete which you want to delete', quote=True)
        return

    for file_type in ("document", "video", "audio"):
        media = getattr(reply, file_type, None)
        if media is not None:
            break
    else:
        await msg.edit('This is not supported file format')
        return
    
    file_id, file_ref = unpack_new_file_id(media.file_id)

    result = await Media.collection.delete_one({
        '_id': file_id,
    })
    if result.deleted_count:
        await msg.edit('File is successfully deleted from database')
    else:
        file_name = re.sub(r"(_|\-|\.|\+)", " ", str(media.file_name))
        result = await Media.collection.delete_one({
            'file_name': file_name,
            'file_size': media.file_size,
            'mime_type': media.mime_type
            })
        if result.deleted_count:
            await msg.edit('File is successfully deleted from database')
        else:
            # files indexed before https://github.com/EvamariaTG/EvaMaria/commit/f3d2a1bcb155faf44178e5d7a685a1b533e714bf#diff-86b613edf1748372103e94cacff3b578b36b698ef9c16817bb98fe9ef22fb669R39 
            # have original file name.
            result = await Media.collection.delete_one({
                'file_name': media.file_name,
                'file_size': media.file_size,
                'mime_type': media.mime_type
            })
            if result.deleted_count:
                await msg.edit('File is successfully deleted from database')
            else:
                await msg.edit('File not found in database')


@Client.on_message(filters.command('deleteall') & filters.user(ADMINS))
async def delete_all_index(bot, message):
    await message.reply_text(
        'This will delete all indexed files.\nDo you want to continue??',
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="YES", callback_data="autofilter_delete"
                    )
                ],
                [
                    InlineKeyboardButton(
                        text="CANCEL", callback_data="close_data"
                    )
                ],
            ]
        ),
        quote=True,
    )


@Client.on_callback_query(filters.regex(r'^autofilter_delete'))
async def delete_all_index_confirm(bot, message):
    await Media.collection.drop()
    await message.answer()
    await message.message.edit('Succesfully Deleted All The Indexed Files.')

