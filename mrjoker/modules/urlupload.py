import os
import asyncio
import time
import datetime
import aiohttp
import traceback

from telethon import events
from mrjoker.utils.plh import humanbytes, time_formatter
from mrjoker import telethn as bot
from mrjoker.utils.plh import humanbytes, progress

TEMP_DOWNLOAD_DIRECTORY = "./"

async def download_file(url, file_name, message, start_time, bot):
    async with aiohttp.ClientSession() as session:
        time.time()
        await download_coroutine(session, url, file_name, message, start_time, bot)
    return file_name


async def download_coroutine(session, url, file_name, event, start, bot):

    CHUNK_SIZE = 1024 * 6  # 2341
    downloaded = 0
    display_message = ""
    async with session.get(url) as response:
        total_length = int(response.headers["Content-Length"])
        content_type = response.headers["Content-Type"]
        if "text" in content_type and total_length < 500:
            return await response.release()
        await event.edit(
            """**Initiating Download**
**URL:** {}
**File Name:** {}
**File Size:** {}
**© @mrjokerpro_bot**""".format(
                url,
                os.path.basename(file_name).replace("%20", " "),
                humanbytes(total_length),
            ),
            parse_mode="md",
        )
        with open(file_name, "wb") as f_handle:
            while True:
                chunk = await response.content.read(CHUNK_SIZE)
                if not chunk:
                    break
                f_handle.write(chunk)
                downloaded += CHUNK_SIZE
                now = time.time()
                diff = now - start
                if round(diff % 10.00) == 0:  # downloaded == total_length:
                    percentage = downloaded * 100 / total_length
                    speed = downloaded / diff
                    elapsed_time = round(diff) * 1000
                    time_to_completion = (
                        round((total_length - downloaded) / speed) * 1000
                    )
                    estimated_total_time = elapsed_time + time_to_completion
                    try:
                        total_length = max(total_length, downloaded)
                        current_message = """Downloading : {}%
URL: {}
File Name: {}
File Size: {}
Downloaded: {}
ETA: {}""".format(
                            "%.2f" % (percentage),
                            url,
                            file_name.split("/")[-1],
                            humanbytes(total_length),
                            humanbytes(downloaded),
                            time_formatter(estimated_total_time),
                        )
                        if current_message not in [display_message, "empty"]:
                            print(current_message)
                            await event.edit(current_message, parse_mode="html")

                            display_message = current_message
                    except Exception as e:
                        print("Error", e)
                        # logger.info(str(e))
        return await response.release()
      
      
#-------------------------------------------------------------------------transfersh----------------------------------------------------------

def get_date_in_two_weeks():
    """
    get maximum date of storage for file
    :return: date in two weeks
    """
    today = datetime.datetime.today()
    date_in_two_weeks = today + datetime.timedelta(days=14)
    return date_in_two_weeks.date()


async def send_to_transfersh_async(file):

    size = os.path.getsize(file)
    size_of_file = humanbytes(size)
    final_date = get_date_in_two_weeks()
    file_name = os.path.basename(file)

    print("\nUploading file: {} (size of the file: {})".format(file_name, size_of_file))
    url = "https://transfer.sh/"

    with open(file, "rb") as f:
        async with aiohttp.ClientSession() as session, session.post(url, data={str(file): f}) as response:
            download_link = await response.text()

    print(
        "Link to download file(will be saved till {}):\n{}".format(
            final_date, download_link
        )
    )
    return download_link, final_date, size_of_file


async def send_to_tmp_async(file):
    url = "https://tmp.ninja/api.php?d=upload-tool"

    with open(file, "rb") as f:
        async with aiohttp.ClientSession() as session, session.post(url, data={"file": f}) as response:
            download_link = await response.text()

    return download_link


@bot.on(events.NewMessage(pattern="/transfersh"))
async def tsh(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("Downloading...")
        try:
            file_path = await url.download_media(
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, ilk, start, "Downloading...")
                )
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            await event.respond(f"**Downloading Failed**\n\n**Error:** {e}")

        await ilk.delete()

        try:
            orta = await event.respond("**Uploading to TransferSh...**")
            download_link, final_date, size = await send_to_transfersh_async(file_path)

            str(time.time() - start)
            await orta.edit(
                f"File Successfully Uploaded to TransferSh.\n\nLink 👉 {download_link}\n*Expired Date* 👉 {final_date}\n\nUploaded by **MR.JOKER ROBOT**"
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            await event.respond(f"Uploading Failed\n\n**Error:** {e}")

    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="/tmpninja"))
async def tmp(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("*Downloading...*")
        try:
            file_path = await url.download_media(
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, ilk, start, "*Downloading...*")
                )
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            await event.respond(f"*Downloading Failed*\n\n**Error:** {e}")

        await ilk.delete()

        try:
            orta = await event.respond("*Uploading to TmpNinja...*")
            download_link = await send_to_tmp_async(file_path)

            str(time.time() - start)
            await orta.edit(
                f"*File Successfully Uploaded to TmpNinja.*\n\n*Link* 👉 {download_link}\n\n*Uploaded by* *MR.JOKER ROBOT*"
            )
        except Exception as e:
            traceback.print_exc()
            print(e)
            await event.respond(f"*Uploading Failed*\n\n**Error:** {e}")

    raise events.StopPropagation


@bot.on(events.NewMessage(pattern="/up"))
async def up(event):
    if event.reply_to_msg_id:
        start = time.time()
        url = await event.get_reply_message()
        ilk = await event.respond("*Downloading...*")

        try:
            filename = os.path.join(TEMP_DOWNLOAD_DIRECTORY, os.path.basename(url.text))
            await download_file(url.text, filename, ilk, start, bot)
        except Exception as e:
            print(e)
            await event.respond(f"Downloading Failed\n\n**Error:** {e}")

        await ilk.delete()

        try:
            orta = await event.respond("Uploading to Telegram...")

            dosya = await bot.upload_file(
                filename,
                progress_callback=lambda d, t: asyncio.get_event_loop().create_task(
                    progress(d, t, orta, start, "Uploading to Telegram...")
                ),
            )

            str(time.time() - start)
            await bot.send_file(
                event.chat.id,
                dosya,
                force_document=True,
                caption="Uploaded By **MR.JOKER ROBOT**",
            )
        except Exception as e:
            traceback.print_exc()

            print(e)
            await event.respond(f"Uploading Failed\n\n**Error:** {e}")

        await orta.delete()

    raise events.StopPropagation


def main():
    if not os.path.isdir(TEMP_DOWNLOAD_DIRECTORY):
        os.mkdir(TEMP_DOWNLOAD_DIRECTORY)



__mod_name__ = "URL Upload"

__help__ = """
Here is the help for the Upload module:
╔Link To File:
╚ `/up` *:*  reply to a direct download link to upload it to telegram as files
 
╔File To Link:
╚ `/transfersh`*:* reply to a telegram file to upload it on transfersh and get direct download link
 """     
