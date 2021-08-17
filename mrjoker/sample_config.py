# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
import json
import os


def get_user_list(config, key):
    with open("{}/mrjoker/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


# Create a new config.py or rename this to config.py file in same dir and import, then extend this class.
class Config(object):
    LOGGER = True
    # REQUIRED
    # Login to https://my.telegram.org and fill in these slots with the details given by it

    API_ID = 1234568 # integer value, dont use ""
    API_HASH = ""
    TOKEN = ""  # This var used to be API_KEY but it is now TOKEN, adjust accordingly.
    BOT_USERNAME = ""
    OWNER_ID = 1131653685   # If you dont know, run the bot and do /id in your private chat with it, also an integer
    OWNER_USERNAME = "kavinduaj"
    ARQ_API_URL = ""
    ARQ_API_KEY = ""
    SUDO_USERS = 1131653685
    SUPPORT_USERS = 1131653685
    WHITELIST_USERS = 1131653685
    SUPPORT_CHAT = "lkhitech"  # Your own group for support, do not add the @
    JOIN_LOGGER = (
        -1001329348574
    )  # Prints any new group the bot is added to, prints just the name and ID.
    EVENT_LOGS = (
        -1001329348574
    )  # Prints information like gbans, sudo promotes, AI enabled disable states that may help in debugging and shit

    # RECOMMENDED
    SQLALCHEMY_DATABASE_URI = ""  
    REDIS_URI = ""
    LOAD = []
    NO_LOAD = ["rss", "cleaner", "connection", "math"]
    WEBHOOK = False
    INFOPIC = True
    URL = None
    SPAMWATCH_API = ""  # go to support.spamwat.ch to get key
    SPAMWATCH_SUPPORT_CHAT = "@SpamWatchSupport"
    OPENWEATHERMAP_ID = ""
 
    # OPTIONAL
    ##List of id's -  (not usernames) for users which have sudo access to the bot.
    DRAGONS = "1131653685"
    ##List of id's - (not usernames) for developers who will have the same perms as the owner
    DEV_USERS = "1131653685"
    ##List of id's (not usernames) for users which are allowed to gban, but can also be banned.
    DEMONS = "1131653685"
    # List of id's (not usernames) for users which WONT be banned/kicked by the bot.
    TIGERS = "1131653685"
    WOLVES = "1131653685"
    DONATION_LINK = None  # EG, paypal
    CERT_PATH = None
    PORT = 5000
    DEL_CMDS = True  # Delete commands that users dont have access to, like delete /ban if a non admin uses it.
    STRICT_GBAN = True
    WORKERS = (
        8  # Number of subthreads to use. Set as number of threads your processor uses
    )
    BAN_STICKER = ""  # banhammer marie sticker id, the bot will send this sticker before banning or kicking a user in chat.
    ALLOW_EXCL = True  # Allow ! commands as well as / (Leave this to true so that blacklist can work)
    CASH_API_KEY = (
        "G"  # Get your API key from https://www.alphavantage.co/support/#api-key
    )
    TIME_API_KEY = "xyz"  # Get your API key from https://timezonedb.com/api
    WALL_API = (
        "xyz"  # For wallpapers, get one from https://wall.alphacoders.com/api.php
    )
    AI_API_KEY = "xyz"  # For chatbot, get one from https://coffeehouse.intellivoid.net/dashboard
    BL_CHATS = []  # List of groups that you want blacklisted.
    SPAMMERS = None
    YOUTUBE_API_KEY=""
    INFOPIC =""
    TEMP_DOWNLOAD_DIRECTORY = "./"
    REM_BG_API_KEY = ""
    MONGO_DB_URI = ""


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True

