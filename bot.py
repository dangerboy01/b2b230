#(©)Codexbotz

from aiohttp import web
from plugins import web_server
from os import path as ospath,remove as osremove
import pyromod.listen
from pyrogram import Client
from pyrogram.enums import ParseMode
import sys
from datetime import datetime

from random import randint

from config import API_HASH, APP_ID, LOGGER, TG_BOT_TOKEN, TG_BOT_WORKERS, CHANNEL_ID, PORT

WD_PROTECTION = 'Yeah Baby'

class Bot(Client):
    def __init__(self):
        super().__init__(
            name="Bot",
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "plugins"
            },
            workers=TG_BOT_WORKERS,
            bot_token=TG_BOT_TOKEN
        )
        self.LOGGER = LOGGER
    
    
    async def start(self):
        await super().start()
        usr_bot_me = await self.get_me()
        self.uptime = datetime.now()
	
        try:
            db_channel = await self.get_chat(CHANNEL_ID)
            self.db_channel = db_channel
            test = await self.send_message(chat_id = db_channel.id, text = "Test Message - @wDbots")
            await test.delete()
        except Exception as e:
            self.LOGGER(__name__).warning(e)
            self.LOGGER(__name__).warning(f"Make Sure bot is Admin in DB Channel, and Double check the CHANNEL_ID Value, Current Value {CHANNEL_ID}")
            self.LOGGER(__name__).info("\nBot Stopped. Join https://t.me/whiteDevilBots for support")
            sys.exit()
        self.set_parse_mode(ParseMode.HTML)
        self.LOGGER(__name__).info(f"Bot Running..!\n\nCreated by \nhttps://t.me/whiteDevilBots")
        self.LOGGER(__name__).info(f""" \n\n       
           _____  _           _       
          |  __ \| |         | |      
 __      _| |  | | |__   ___ | |_ ___ 
 \ \ /\ / / |  | | '_ \ / _ \| __/ __|
  \ V  V /| |__| | |_) | (_) | |_\__ \\
   \_/\_/ |_____/|_.__/ \___/ \__|___/
                                      
                                          """)
        self.username = usr_bot_me.username
        #web-response
        if PORT:
            app = web.AppRunner(await web_server())
            await app.setup()
            bind_address = "0.0.0.0"
            await web.TCPSite(app, bind_address, PORT).start()
        if ospath.isfile(".restartmsg"):
                    with open(".restartmsg") as f:
                        chat_id, msg_id = map(int, f)
                    msg = f"Bot Restarted Successfully❗\n"+('by @wDbots' if randint(1,30)==3 else "")
                    await self.edit_message_text(chat_id, msg_id, msg)
                    osremove(".restartmsg")
    async def stop(self, *args):
        await super().stop()
        self.LOGGER(__name__).info("Bot stopped.")
