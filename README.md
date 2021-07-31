<h1> ❝𝐓𝐡𝐞 𝐌𝐨𝐬𝐭 𝐏𝐨𝐰𝐞𝐫𝐟𝐮𝐥𝐥 𝐆𝐫𝐨𝐮𝐩 𝐌𝐚𝐧𝐚𝐠𝐞𝐦𝐞𝐧𝐭 𝐁𝐨𝐭❞ </h1>




<center>[![Mr.Joker LOGOG](https://telegra.ph/file/6525d89de5b72003d80fa.png)](https://t.me/Mrjokerlk_bot)</center>

<h1 align ="center"> 𝍖𝍖𝍖𐒄Ɽ.ʝⰙƘƸⱤ𝍖𝍖𝍖</h1>
<h1 align = "center">Yo,🤡♂️I'm Alive..I'm a super bot 🔥...🚴‍♂️Speed 1 THz..Memory 1 Zettabyte.🕺</center></h1>

<p><h3 align = "justify">A modular telegram Python bot running on python3 with an sqlalchemy database.</br></br></h3>
  
<h3 align = "justify">Originally a simple group management bot with multiple admin features, it has evolved into becoming a basis for modular bots aiming to provide simple plugin expansion via a simple drag and drop.</h3></p>









## Deploy
[![Deploy To Heroku](https://www.herokucdn.com/deploy/button.svg)](https://dashboard.heroku.com/new?template=https://github.com/kjeymax/MR-JOKER_BOT)

[![Deploy To Railway](https://railway.app/button.svg)](https://railway.app)

[![Deploy to Qovery](https://img.shields.io/badge/Deploy-Qovery-6EC0D9.svg)](https://qovery.com)

[![Contact me](https://img.shields.io/badge/Telegram-Contact%20Me-informational)](https://t.me/kavinduaj)



## Starting the bot

<h3 align = "justify">Once you've setup your database and your configuration (see below) is complete, simply run:</h3>

```

python3 -m mrjoker

```

## Configuration 

<h3 align = "justify">Create a new <u>config.py</u> or rename <u>sample_config.py</u> to <u>config.py</u> file in same dir and import, then extend this class.</h3>

- `TOKEN`                  : Your [bot Token](https://t.me/BotFather), As a string
- `API_ID & API_HASH`      : Get API_ID & API_HASH from my.telegram.org, used for telethon based modules.
- `SQLALCHEMY_DATABASE_URI`: Your database URL
-  `OWNER_ID`              : An integer of consisting of your [owner ID](https://t.memy_id_bot)
-   `OWNER_USERNAME`       : Your username (without the @)
-   `SUPPORT_CHAT`         : Your Telegram support group chat username
-   `EVENT_LOGS`           : Event logs channel to note down important bot level events, recommend to make this public. ex: `-100:123`
-   `JOIN_LOGGER`          : A channel where bot will print who added it to what group, useful during debugging or spam handling.
-   `CASH_API_KEY`         :Required for currency converter. [Get yours from](https://www.alphavantage.co/support/#api-key)
-   `TIME_API_KEY`         : Required for timezone information. [Get yours from](https://timezonedb.com/api)
-   `DEV_USERS`            : ID of users who are Devs of your bot (can use /py etc.). If you are a noob and would come and bother Mr.Joker support then keep the current ID's here at they are and add yours. 
-   `sw_api`               : Spamwatch API Token, Get one from [@SpamWatchBot](https://t.me/SpamWatchBot)
-   `STRICT_GBAN`          : Enforce gbans across new groups as well as old groups. When a gbanned user talks, he will be banned.
-   `DRAGONS`              : A space separated list of user IDs who you want to assign as sudo users
-   `DEMONS`               : A space separated list of user IDs who you wanna assign as support users(gban perms only)
-   `TIGERS`               : A space separated list of user IDs who you wanna assign as tiger users.
-   `WOLVES`               : A space separated list of user IDs who you want to assign as whitelisted - can't be banned with your bot.
-   `ENV`                  : Setting this to ANYTHING will enable environment variables. Leave it as it is
-   `WEBHOOK`              : Setting this to ANYTHING will enable webhooks. If you dont know how this works leave it as it is
-   `PORT`                 : Port to use for your webhooks. Better leave this as it is on heroku
-   `URL`                  : The Heroku App URL :-  `https://<appname>.herokuapp.com`
-   `No_LOAD`              : Dont load these modules cause they shit, space separation
-   `BL_CHATS`             : List of chats you want blacklisted.
-   `ALLOW_EXCL`           : Set this to True if you want ! to be a command prefix along with /. Recommended is True
-   `DEL_CMDS`             : Set this to True if you want to delete command messages from users who don't have the perms to run that command.
-   `AI_API_KEY`           : Make your bot talk using Intellivoid's chatbot API, [Get your key from](https://coffeehouse.intellivoid.net/)
-   `BAN_STICKER`          : ID of the sticker you want to use when banning people
-   `WALL_API`             : Required for wallpaper. [Get your's from](https://wall.alphacoders.com/)  
 

