#(©)Codexbotz

from pyrogram import Client, filters, enums
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, ChatJoinRequest, CallbackQuery
from bot import Bot
from config import ADMINS, REQ_CHANNEL, OWNER_ID, MESSAGE, INFO
from helper_func import encode, get_message_id, decode
from logging import getLogger
from database.join_reqs import JoinReqs
from database.database import getConfig, updateConfig
from random import randint

@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('batch'))
async def batch(client: Client, message: Message):
    while True:
        try:
            first_message = await client.ask(text = "Forward the First Message from DB Channel (with Quotes)..\n\nor Send the DB Channel Post Link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        f_msg_id = await get_message_id(client, first_message)
        if f_msg_id:
            break
        else:
            await first_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue

    while True:
        try:
            second_message = await client.ask(text = "Forward the Last Message from DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        s_msg_id = await get_message_id(client, second_message)
        if s_msg_id:
            break
        else:
            await second_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is taken from DB Channel", quote = True)
            continue


    string = f"get-{f_msg_id * abs(client.db_channel.id)}-{s_msg_id * abs(client.db_channel.id)}"
    base64_string = await encode(string)
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await second_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)


@Bot.on_message(filters.private & filters.user(ADMINS) & filters.command('genlink'))
async def link_generator(client: Client, message: Message):
    while True:
        try:
            channel_message = await client.ask(text = "Forward Message from the DB Channel (with Quotes)..\nor Send the DB Channel Post link", chat_id = message.from_user.id, filters=(filters.forwarded | (filters.text & ~filters.forwarded)), timeout=60)
        except:
            return
        msg_id = await get_message_id(client, channel_message)
        if msg_id:
            break
        else:
            await channel_message.reply("❌ Error\n\nthis Forwarded Post is not from my DB Channel or this Link is not taken from DB Channel", quote = True)
            continue

    base64_string = await encode(f"get-{msg_id * abs(client.db_channel.id)}")
    link = f"https://t.me/{client.username}?start={base64_string}"
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("🔁 Share URL", url=f'https://telegram.me/share/url?url={link}')]])
    await channel_message.reply_text(f"<b>Here is your link</b>\n\n{link}", quote=True, reply_markup=reply_markup)


db = JoinReqs
logger = getLogger(__name__)

@Client.on_chat_join_request(filters.chat(REQ_CHANNEL if REQ_CHANNEL else "self"))
async def join_reqs(client, join_req: ChatJoinRequest):

    if db().isActive():
        user_id = join_req.from_user.id
        first_name = join_req.from_user.first_name
        username = join_req.from_user.username
        date = join_req.date

        await db().add_user(
            user_id=user_id,
            first_name=first_name,
            username=username,
            date=date
        )


@Client.on_message(filters.command("totalrequests") & filters.private & filters.user((ADMINS)))
async def total_requests(client, message):

    if db().isActive():
        total = await db().get_all_users_count()
        await message.reply_text(
            text=f"Total Requests: {total}",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    if data == "about":
        string= await decode(INFO)
        await query.message.edit_text(
            text = str(string),
            disable_web_page_preview = True,
            reply_markup = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔒 Close", callback_data = "close")
                    ]
                ]
            )
        )
        return True
    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass


@Client.on_message(filters.command("purgerequests") & filters.private & filters.user(ADMINS))
async def purge_requests(client, message):
    
    if db().isActive():
        await db().delete_all_users()
        await message.reply_text(
            text="Purged All Requests.",
            parse_mode=enums.ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )

@Client.on_message(filters.command("wdbot"))
async def yesno(client, message):
    await message.reply_text(text="Yes , IT is .")

@Bot.on_message(filters.command('setreq') & filters.private & filters.user(ADMINS))
async def req_sub_change(client: Bot, msg: Message):
    text=msg.text
    text=text.split()
    confiG = await getConfig()
    if len(text)!=2:
        fsub=confiG['REQ_CHANNEL']
        await msg.reply(f'Current Request Channel: <code>{fsub}</code>')
        return
    if len(text)==2:
        newFsub=text[1]
        confiG['REQ_CHANNEL']=int(newFsub)
        if await updateConfig(confiG):
            await msg.reply("Request Channel Updated")
        else:
            await msg.reply("Something Went Wrong, Contact Developer"+(MESSAGE if randint(1,30)==3 else ""))

@Bot.on_message(filters.private & filters.user(OWNER_ID)&filters.command('newadmins'))
async def admin_lists(client: Bot, msg: Message):
    text=msg.text
    text=text.split(maxsplit=1)
    confiG = await getConfig()
    if len(text)!=2:
        admins=confiG['ADMINS']
        await msg.reply(f'Current admins: <code>{admins}</code>')
        return
    try:
        newFsub=text[1]
        admins=list()
        for x in newFsub.split():
            admins.append(int(x))
        confiG['ADMINS']=admins
        if await updateConfig(confiG):
            await msg.reply(f"Admins List Updated with {admins}")
    except:
        await msg.reply("Something Went Wrong, Contact Developer"+(MESSAGE if randint(1,30)==3 else ""))