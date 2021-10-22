#--------------------------------------------------------------------------Saavn Music------------------------------------
import os
import requests
import wget
from pyrogram import filters

from mrjoker import pbot as mrjoker 
from mrjoker.services.dk import get_arg


@mrjoker.on_message(filters.command("saavn"))
async def song(client, message):
    message.chat.id
    message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("**Enter song name❗**")
        return ""
    m = await message.reply_text(
        "**Downloading your song,**\n**Plz wait** ⏳️"
    )
    try:
        r = requests.get(f"https://jostapi.herokuapp.com/saavn?query={args}")
    except Exception as e:
        await m.edit(str(e))
        return
    sname = r.json()[0]["song"]
    slink = r.json()[0]["media_url"]
    ssingers = r.json()[0]["singers"]
    file = wget.download(slink)
    ffile = file.replace("mp4", "m4a")
    os.rename(file, ffile)
    await message.reply_audio(audio=ffile, title=sname, performer=ssingers)
    os.remove(ffile)
    await m.delete()


#-------------------------------------------------------------------------------Deezer Music--------------------------------------------- 


import os
import aiofiles
import aiohttp
from pyrogram import filters
from mrjoker import pbot as mrjoker

ARQ = "https://thearq.tech/"

async def fetch(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            try:
                data = await resp.json()
            except:
                data = await resp.text()
    return data

async def download_song(url):
    song_name = f"mrjoker.mp3"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                f = await aiofiles.open(song_name, mode="wb")
                await f.write(await resp.read())
                await f.close()
    return song_name


@mrjoker.on_message(filters.command("deezer"))
async def deezer(_, message):
    if len(message.command) < 2:
        await message.reply_text("**Downloading your song Deezer** ,\n**Plz wait** ⏳️")
        return
    text = message.text.split(None, 1)[1]
    query = text.replace(" ", "%20")
    m = await message.reply_text("**Searching...**")
    try:
        r = await fetch(f"{ARQ}deezer?query={query}&count=1")
        title = r[0]["title"]
        url = r[0]["url"]
        artist = r[0]["artist"]
    except Exception as e:
        await m.edit(str(e))
        return
    await m.edit("**Downloading...**")
    song = await download_song(url)
    await m.edit("**Uploading...**")
    await message.reply_audio(audio=song, title=title, performer=artist)
    os.remove(song)
    await m.delete()

#-------------------------------------------------------------------------YT Audio-----------------------------------------------------------

import os
import aiohttp
from pyrogram import filters
from pytube import YouTube
from youtubesearchpython import VideosSearch

from mrjoker import LOGGER, pbot
from mrjoker.utils.ut import get_arg


def yt_search(song):
    videosSearch = VideosSearch(song, limit=1)
    result = videosSearch.result()
    if not result:
        return False
    else:
        video_id = result["result"][0]["id"]
        url = f"https://youtu.be/{video_id}"
        return url


class AioHttp:
    @staticmethod
    async def get_json(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.json()

    @staticmethod
    async def get_text(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.text()

    @staticmethod
    async def get_raw(link):
        async with aiohttp.ClientSession() as session:
            async with session.get(link) as resp:
                return await resp.read()


@pbot.on_message(filters.command("song"))
async def song(client, message):
    message.chat.id
    user_id = message.from_user["id"]
    args = get_arg(message) + " " + "song"
    if args.startswith(" "):
        await message.reply("**Enter a song name.** **Check** `/help`")
        return ""
    status = await message.reply("**Processing...**")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("**Song not found😪**.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("**Failed to download song**")
        LOGGER.error(ex)
        return ""
    os.rename(download, f"{str(user_id)}.mp3")
    await pbot.send_chat_action(message.chat.id, "upload_audio")
    await pbot.send_audio(
        chat_id=message.chat.id,
        audio=f"{str(user_id)}.mp3",
        duration=int(yt.length),
        title=str(yt.title),
        performer=str(yt.author),
        reply_to_message_id=message.message_id,
    )
    await status.delete()
    os.remove(f"{str(user_id)}.mp3")
    
#---------------------------------------------------YT VIDEO-------------------------------------    
    
import asyncio
import math
import os
import time
import wget
from random import randint
from urllib.parse import urlparse

import aiofiles
import aiohttp
import requests
import youtube_dl
from yt_dlp import YoutubeDL
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import *
from youtube_search import YoutubeSearch

from mrjoker.conf import get_str_key
from mrjoker import pbot

@pbot.on_message(filters.command(["video"]))
async def video(pbot, message):
    ydl_opts = {
        'format':'best',
        'keepvideo':True,
        'prefer_ffmpeg':False,
        'geo_bypass':True,
        'outtmpl':'%(title)s.%(ext)s',
        'quite':True
    }
    query = " ".join(message.command[1:])
    try:
        results = YoutubeSearch(query, max_results=1).to_dict()
        link = f"https://youtube.com{results[0]['url_suffix']}"
        title = results[0]["title"][:40]
        thumbnail = results[0]["thumbnails"][0]
        thumb_name = f"thumb{title}.jpg"
        thumb = requests.get(thumbnail, allow_redirects=True)
        open(thumb_name, "wb").write(thumb.content)
        duration = results[0]["duration"]
        results[0]["url_suffix"]
        results[0]["views"]
        rby = message.from_user.mention
    except Exception as e:
        print(e)
    try:
        msg = await message.reply("**Deezer**")
        with YoutubeDL(ydl_opts) as ytdl:
            ytdl_data = ytdl.extract_info(link, download=True)
            file_name = ytdl.prepare_filename(ytdl_data)
    except Exception as e:
        return await msg.edit(f"🚫 **error:** {str(e)}")
    preview = wget.download(thumbnail)
    await msg.edit("**Uploading Video...**")
    await message.reply_video(
        file_name,
        duration=int(ytdl_data["duration"]),
        thumb=preview,
        caption=ytdl_data['title'])
    try:
        os.remove(file_name)
        await msg.delete()
    except Exception as e:
        print(e)  

   
    
#------------------------------------------------------------------Lyrics-----------------------------------------------------------------
import io
import os


import lyricsgenius
from pyrogram import filters
from tswift import Song

from mrjoker.conf import get_str_key
from mrjoker import pbot

GENIUS = get_str_key("GENIUS_API_TOKEN", None)


@pbot.on_message(filters.command(["lyric", "lyrics"]))
async def _(client, message):
    lel = await message.reply("**Searching For Lyrics.....**")
    query = message.text
    if not query:
        await lel.edit("`What I am Supposed to find `")
        return

    song = ""
    song = Song.find_song(query)
    if song:
        if song.lyrics:
            reply = song.format()
        else:
            reply = "Couldn't find any lyrics for that song! try with artist name along with song if still doesnt work try `.glyrics`"
    else:
        reply = "lyrics not found! try with artist name along with song if still doesnt work try `.glyrics`"

    if len(reply) > 4095:
        with io.BytesIO(str.encode(reply)) as out_file:
            out_file.name = "lyrics.text"
            await client.send_document(
                message.chat.id,
                out_file,
                force_document=True,
                allow_cache=False,
                caption=query,
                reply_to_msg_id=message.message_id,
            )
            await lel.delete()
    else:
        await lel.edit(reply)  # edit or reply


@pbot.on_message(filters.command(["glyric", "glyrics"]))
async def lyrics(client, message):

    if r"-" in message.text:
        pass
    else:
        await message.reply(
            "`Error: please use '-' as divider for <artist> and <song>`\n"
            "eg: `.glyrics Nicki Minaj - Super Bass`"
        )
        return

    if GENIUS is None:
        await message.reply(
            "`Provide genius access token to config.py or Heroku Config first kthxbye!`"
        )
    else:
        genius = lyricsgenius.Genius(GENIUS)
        try:
            args = message.text.split(".lyrics")[1].split("-")
            artist = args[0].strip(" ")
            song = args[1].strip(" ")
        except Exception:
            await message.reply("`Lel please provide artist and song names`")
            return

    if len(args) < 1:
        await message.reply("`Please provide artist and song names`")
        return

    lel = await message.reply(f"`Searching lyrics for {artist} - {song}...`")

    try:
        songs = genius.search_song(song, artist)
    except TypeError:
        songs = None

    if songs is None:
        await lel.edit(f"Song **{artist} - {song}** not found!")
        return
    if len(songs.lyrics) > 4096:
        await lel.edit("`Lyrics is too big, view the file to see it.`")
        with open("lyrics.txt", "w+") as f:
            f.write(f"Search query: \n{artist} - {song}\n\n{songs.lyrics}")
        await client.send_document(
            message.chat.id,
            "lyrics.txt",
            reply_to_msg_id=message.message_id,
        )
        os.remove("mjlyrics.txt")
    else:
        await lel.edit(
            f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```"
        )
    return
