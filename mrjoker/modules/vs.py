import asyncio
import io
import json
import os
import time
import aiohttp
import lyricsgenius
import requests
import wget

from pyrogram import filters
from pyrogram.types import Message
from tswift import Song
from pytube import YouTube
from youtubesearchpython import SearchVideos

from mrjoker import LOGGER, pbot
from mrjoker.utils.ut import get_arg
from telethon.tl.types import DocumentAttributeAudio
from youtube_dl import YoutubeDL
from youtube_dl.utils import (
    ContentTooShortError,
    DownloadError,
    ExtractorError,
    GeoRestrictedError,
    MaxDownloadsReached,
    PostProcessingError,
    UnavailableVideoError,
    XAttrMetadataError,
)

from mrjoker.conf import get_str_key
from mrjoker.pyro.pluginshelper import get_text
from mrjoker.events import register
from mrjoker.utils import progress

#-----------------------------------------------------------------------Video------------------------------------------------------------------

GENIUS = get_str_key("GENIUS_API_TOKEN", None)

try:
    from youtubesearchpython import SearchVideos

except:
    os.system("pip install pip install youtube-search-python")
    from youtubesearchpython import SearchVideos


@register(pattern="^/video (.*)")
async def download_video(v_url):
    lazy = v_url
    sender = await lazy.get_sender()
    me = await lazy.client.get_me()
    if not sender.id == me.id:
        rkp = await lazy.reply("`processing...`")
    else:
        rkp = await lazy.edit("`processing...`")
    url = v_url.pattern_match.group(1)
    if not url:
        return await rkp.edit("`Error \nusage video <song name>`")
    search = SearchVideos(url, offset=1, mode="json", max_results=1)
    test = search.result()
    p = json.loads(test)
    q = p.get("search_result")
    try:
        url = q[0]["link"]
    except:
        return await rkp.edit("`failed to find`")
    type = "audio"
    await rkp.edit("`Preparing to download...`")
    if type == "audio":
        opts = {
            "format": "best",
            "addmetadata": True,
            "key": "FFmpegMetadata",
            "prefer_ffmpeg": True,
            "geo_bypass": True,
            "nocheckcertificate": True,
            "postprocessors": [
                {"key": "FFmpegVideoConvertor", "preferedformat": "mp4"}
            ],
            "outtmpl": "%(id)s.mp4",
            "logtostderr": False,
            "quiet": True,
        }
        song = False
        video = True
    try:
        await rkp.edit("`Fetching data, please wait..`")
        with YoutubeDL(opts) as rip:
            rip_data = rip.extract_info(url)
    except DownloadError as DE:
        await rkp.edit(f"`{str(DE)}`")
        return
    except ContentTooShortError:
        await rkp.edit("`The download content was too short.`")
        return
    except GeoRestrictedError:
        await rkp.edit(
            "`Video is not available from your geographic location due to geographic restrictions imposed by a website.`"
        )
        return
    except MaxDownloadsReached:
        await rkp.edit("`Max-downloads limit has been reached.`")
        return
    except PostProcessingError:
        await rkp.edit("`There was an error during post processing.`")
        return
    except UnavailableVideoError:
        await rkp.edit("`Media is not available in the requested format.`")
        return
    except XAttrMetadataError as XAME:
        await rkp.edit(f"`{XAME.code}: {XAME.msg}\n{XAME.reason}`")
        return
    except ExtractorError:
        await rkp.edit("`There was an error during info extraction.`")
        return
    except Exception as e:
        await rkp.edit(f"{str(type(e)): {str(e)}}")
        return
    c_time = time.time()
    if song:
        await rkp.edit(
            f"`Preparing to upload Video `\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp3",
            supports_streaming=True,
            attributes=[
                DocumentAttributeAudio(
                    duration=int(rip_data["duration"]),
                    title=str(rip_data["title"]),
                    performer=str(rip_data["uploader"]),
                )
            ],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, v_url, c_time, "Uploading..", f"{rip_data['title']}.mp3")
            ),
        )
        os.remove(f"{rip_data['id']}.mp3")
        await v_url.delete()
    elif video:
        await rkp.edit(
            f"`Preparing to upload video song :`\
        \n**{rip_data['title']}**\
        \nby *{rip_data['uploader']}*"
        )
        await v_url.client.send_file(
            v_url.chat_id,
            f"{rip_data['id']}.mp4",
            supports_streaming=True,
            caption=rip_data["title"],
            progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                progress(d, t, v_url, c_time, "Uploading..", f"{rip_data['title']}.mp4")
            ),
        )
        os.remove(f"{rip_data['id']}.mp4")
        await rkp.delete()

#-----------------------------------------------------------Song---------------------------------------------------------------



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
        await message.reply("Enter a song name. Check /help")
        return ""
    status = await message.reply("Processing...")
    video_link = yt_search(args)
    if not video_link:
        await status.edit("Song not found😪.")
        return ""
    yt = YouTube(video_link)
    audio = yt.streams.filter(only_audio=True).first()
    try:
        download = audio.download(filename=f"{str(user_id)}")
    except Exception as ex:
        await status.edit("Failed to download song")
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
    
 #--------------------------------------------------------------------------------Lyric------------------------------------------------------------  
    
@pbot.on_message(filters.command(["lyric", "lyrics"]))
async def _(client, message):
    lel = await message.reply("Searching For Lyrics.....")
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
            "eg: `.glyrics HR jothi pala - Super Bass`"
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
        os.remove("lyrics.txt")
    else:
        await lel.edit(
            f"**Search query**: \n`{artist} - {song}`\n\n```{songs.lyrics}```"
        )
    return
    


__help__ = """
 *You can either enter just the song name or both the artist and song
  name. *

🔹 `/song` <songname artist(optional)>*:* uploads the song in it's best quality available
🔹 `/video` <songname artist(optional)>*:* uploads the video song in it's best quality available
🔹 `/lyrics` <song>*:* returns the lyrics of that song.
🔹 `/glyric` <artist name - song name>

"""

__mod_name__ = "Music"

