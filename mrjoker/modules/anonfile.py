import os
import sys
import time
import logging
import pyrogram
import aiohttp
import asyncio
import requests
import aiofiles
from random import randint
from mrjoker.function.progress import progress
from pyrogram.errors import UserNotParticipant, UserBannedInChannel
from pyrogram import Client, filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InlineQuery, InputTextMessageContent

from mrjoker import pbot
#from mrjoker import 


UPDATES_CHANNEL = "mrjokerloggroup"
DOWNLOAD = "./"

# vars
#APP_ID = Config.APP_ID
#API_HASH = Config.API_HASH
#BOT_TOKEN = Config.BOT_TOKEN

   
#bot = Client(
#    "AnonFilesBot",
#    api_id=APP_ID,
 #   api_hash=API_HASH,
#    bot_token=BOT_TOKEN)



''' 
        
@bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    text = START_TEXT
    reply_markup = START_BUTTONS
    await update.reply_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )
'''
      
@pbot.on_message(filters.media & filters.private & filters.command(["an"]))
async def upload(client, message):
    if UPDATES_CHANNEL is not None:
        try:
            user = await client.get_chat_member(UPDATES_CHANNEL, message.chat.id)
            if user.status == "kicked":
                await client.send_message(
                    chat_id=message.chat.id,
                    text="**Sᴏʀʀʏ, Yᴏᴜ ᴀʀᴇ Bᴀɴɴᴇᴅ ᴛᴏ ᴜsᴇ ᴍᴇ! Cᴏɴᴛᴀᴄᴛ** [Support](https://t.me/lkhitech).",
                    parse_mode="markdown",
                    disable_web_page_preview=True
                )
                return
        except UserNotParticipant:
            await client.send_message(
                chat_id=message.chat.id,
                text="**Pʟᴇᴀsᴇ Jᴏɪɴ Mʏ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ Tᴏ Usᴇ Mᴇ 🏃‍♂**",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("Jᴏɪɴ Uᴘᴅᴀᴛᴇs Cʜᴀɴɴᴇʟ", url=f"https://t.me/{UPDATES_CHANNEL}")
                        ]
                    ]
                ),
                parse_mode="markdown"
            )
            return
        except Exception:
            await client.send_message(
                chat_id=message.chat.id,
                text="**Sᴏᴍᴇᴛʜɪɴɢ ᴡᴇɴᴛ Wʀᴏɴɢ! Cᴏɴᴛᴀᴄᴛ ᴍʏ** [Support](https://t.me/lkhitech).",
                parse_mode="markdown",
                disable_web_page_preview=True)
            return
    m = await message.reply("**Dᴏᴡɴʟᴏᴀᴅɪɴɢ Yᴏᴜʀ FIʟᴇs Tᴏ Mʏ Sᴇʀᴠᴇʀ ....** 😈")
    now = time.time()
    sed = await bot.download_media(
                message, DOWNLOAD,
          progress=progress,
          progress_args=(
            "**Uᴘʟᴏᴀᴅ Pʀᴏᴄᴇss Sᴛᴀʀᴇᴅ Wᴀɪᴛ ᴀɴᴅ Wᴀᴛᴄʜ Mᴀɢɪᴄ**\n**Iᴛs Tᴀᴋᴇ ᴛɪᴍᴇ Aᴄᴄᴏʀᴅɪɴɢ Yᴏᴜʀ Fɪʟᴇs Sɪᴢᴇ** \n\n**ᴇᴛᴀ:** ", 
            m,
            now
            )
        )
    try:
        files = {'file': open(sed, 'rb')}
        await m.edit("**Uᴘʟᴏᴀᴅɪɴɢ ᴛᴏ AɴᴏɴFIʟᴇs Sᴇʀᴠᴇʀ Pʟᴇᴀsᴇ Wᴀɪᴛ**")
        callapi = requests.post("https://api.anonfiles.com/upload", files=files)
        text = callapi.json()
        output = f"""
<u>**Fɪʟᴇ Uᴘʟᴏᴀᴅᴇᴅ Tᴏ AɴᴏɴFɪʟᴇs**</u>

**📂 Fɪʟᴇ Nᴀᴍᴇ:** {text['data']['file']['metadata']['name']}

**📦 Fɪʟᴇ Sɪᴢᴇ:** {text['data']['file']['metadata']['size']['readable']}

**📥Dᴏᴡɴʟᴏᴀᴅ Lɪɴᴋ:** `{text['data']['file']['url']['full']}`

🔅__MᴀɪɴTᴀɪɴᴇᴅ Bʏ__ :** @AvishkarPatil**"""
        btn = InlineKeyboardMarkup(
                                [[InlineKeyboardButton("Dᴏᴡɴʟᴏᴀᴅ Fɪʟᴇ", url=f"{text['data']['file']['url']['full']}")]])
        await m.edit(output, reply_markup=btn)
        os.remove(sed)
    except Exception:
        await m.edit("__Pʀᴏᴄᴇss Fᴀɪʟᴇᴅ, Mᴀʏʙᴇ Tɪᴍᴇ Oᴜᴛ Dᴜᴇ Tᴏ Lᴀʀɢᴇ Fɪʟᴇ Sɪᴢᴇ!__")
        return
      
@pbot.on_message(filters.regex(pattern="https://cdn-") & filters.private & ~filters.edited)
async def url(client, message):
    msg = await message.reply("__Cʜᴇᴄᴋɪɴɢ Uʀʟ...__")
    lenk = message.text
    cap = "© @AvishkarPatil"
    thumb = "./thumb.jpg"
    try:
         await msg.edit("**Bɪɢ Fɪʟᴇs Wɪʟʟ Tᴀᴋᴇ Mᴏʀᴇ Tɪᴍᴇ, Dᴏɴ'ᴛ Pᴀɴɪᴄ!**")
         filename = await download(lenk)
         await msg.edit("Uploading File To Telegram...")
         await message.reply_document(filename, caption=cap, thumb=thumb)
         await msg.delete()
         os.remove(filename)
    except Exception:
        await msg.edit("__Pʀᴏᴄᴇss Fᴀɪʟᴇᴅ, Mᴀʏʙᴇ Tɪᴍᴇ Oᴜᴛ Dᴜᴇ Tᴏ Lᴀʀɢᴇ Fɪʟᴇ Sɪᴢᴇ!__")
        
async def download(url):
    ext = url.split(".")[-1]
    filename = str(randint(1000, 9999)) + "." + ext
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(filename, mode='wb')
                await f.write(await resp.read())
                await f.close()
    return filename
        
        
#pbot.start()
#print("AnonFilesBot Is Started!,  if Have Any Problems contact @AvishkarPatil")
#idle()
