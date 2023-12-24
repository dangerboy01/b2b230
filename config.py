#(©)CodeXBotz




import os
import logging
from logging.handlers import RotatingFileHandler
from dotenv import load_dotenv
from pymongo import MongoClient
load_dotenv('wd.env', override=True)
mode=0

MESSAGE='@wDbots'
INFO=''
#Bot token @Botfather
TG_BOT_TOKEN = os.environ.get("TG_BOT_TOKEN", "")
if  not TG_BOT_TOKEN:
    logging.error('BOT TOKEN NOT FOUND !!')
    exit(1)
bot_id = int(TG_BOT_TOKEN.split(':', 1)[0])

#Your API ID from my.telegram.org
APP_ID = int(os.environ.get("APP_ID", ""))
if not APP_ID:
    logging.error('APP ID NOT FOUND !!')
    exit(1)
#Your API Hash from my.telegram.org
API_HASH = os.environ.get("API_HASH", "")
if not API_HASH:
    logging.error('API HASH NOT FOUND !!')
    exit(1)
#Your db channel Id
CHANNEL_ID = int(os.environ.get("CHANNEL_ID", ""))

#OWNER ID
OWNER_ID = int(os.environ.get("OWNER_ID", ""))
if not OWNER_ID:
    logging.error('Owner ID NOT FOUND !!')
    exit(1)


#Database 
DB_URI = os.environ.get("DATABASE_URL", "")
if not DB_URI:
    logging.error("DB url NOt set @!")
    exit(1)
DB_NAME = os.environ.get("DATABASE_NAME", "wdbots")
JOIN_REQS_DB=DB_URI

#save
conn = MongoClient(DB_URI)
db = conn.wDbots
if confiG := db.config.find_one({'_id': bot_id}):  #retrun config dict (all env vars)
    print("Getting Values from DB")
    del confiG['_id']
    for key, value in confiG.items():
        os.environ[key] = str(value)
else:
    mode=1
conn.close()

#force sub channel id, if you want enable force sub
REQ_CHANNEL = os.environ.get("REQ_CHANNEL",'')
try:
 REQ_CHANNEL = int(REQ_CHANNEL)
except:
 REQ_CHANNEL= False

if mode==1:
 ADMINS=os.environ.get('ADMINS','1')
else:
    ADMINS=confiG['ADMINS']    
if isinstance(ADMINS,str) and mode:
    try:
        admin=ADMINS.split()
        ADMINS=[OWNER_ID]
        for x in admin:
            ADMINS.append(int(x))
    except ValueError:
            raise Exception("Your Admins list does not contain valid integers.")
            ADMINS=[1]

TG_BOT_WORKERS = int(os.environ.get("TG_BOT_WORKERS", "6"))

#start message
START_MSG = os.environ.get("STARTo_MESSAGE", "SGVsbG8ge2ZpcnN0fQoKSSBhbSBhIEZpbGUgU3RvcmUgYm90Lg")

#Force sub message 
FORCE_MSG = os.environ.get("FORCE_SUB_MESSAGE", "Hello {first}\n\n<b>You need to join in my Channel/Group to use me\n\nKindly Please join Channel</b>")

#set your Custom Caption here, Keep None for Disable Custom Caption
CUSTOM_CAPTION = os.environ.get("CUSTOM_CAPTION", None)

#set True if you want to prevent users from forwarding files from bot
PROTECT_CONTENT = True if os.environ.get('PROTECT_CONTENT', "False") == "True" else False

#Set true if you want Disable your Channel Posts Share button
DISABLE_CHANNEL_BUTTON = os.environ.get("DISABLE_CHANNEL_BUTTON", None) == 'True'

BOT_STATS_TEXT = "<b>BOT UPTIME</b>\n{uptime}"
USER_REPLY_TEXT = "❌Don't send me messages directly I'm only File Share bot!"

PORT = int(os.environ.get("PORT",0))
LOG_FILE_NAME = "filesharingbotBYwDbots.txt"

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_NAME,
            maxBytes=50000000,
            backupCount=10
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)

if mode:
    print("Saving values in DB")
    confiG={
        'REQ_CHANNEL':REQ_CHANNEL,
        'ADMINS':ADMINS,
        'Creater':"@whiteDevilBots"
    }
    conn = MongoClient(DB_URI)
    db = conn.wDbots
    db.config.update_one({'_id': bot_id}, {'$set': confiG}, upsert=True)
    conn.close()
