import os

from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession
import telegram as tt

import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

#logging.basicConfig(filename='app.log', format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)
logging.info("Starting...")

# Basics
APP_ID = config("APP_ID", default=None, cast=int)

API_HASH = config("API_HASH", default=None)

FROM_ = config("FROM_CHANNEL")

TO_ = config("TO_CHANNEL")

bot_token = config("BOT_TOKEN")
chat_id = config("CHAT_ID", cast=int)


string1 = "incog"
logging.info("Forwarding Messages from : %s" % FROM_)
logging.info("Forwarding messages to : %s" % TO_)

logging.info("Using session : %s" % string1)

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]


try:
    Bot = TelegramClient(string1, APP_ID, API_HASH)
    Bot.start()
except Exception as ap: 
    logging.error(f"ERROR - {ap}")
    exit(1) 

def send_message_bot(message_to_send, bot_token, chat_id):
    """ This function will send the message to bot. """
    try:
        bot = tt.Bot(bot_token)
        bot.sendMessage(chat_id=chat_id,text= message_to_send)
        logging.info("Got It")
    except Exception as err:
        logging.error("Error in sending message with bot: %s" % err)
    return True


@Bot.on(events.NewMessage(incoming=True, chats=FROM))
async def send(event):
    for i in TO:
        try:
            if event.poll:
                return
            if event.photo:
                photo = event.media.photo
                await Bot.send_file(i, photo, caption = event.text, link_preview = False)
            elif event.media:
                try:
                    if event.media.webpage:
                        await Bot.send_message(i, event.text, link_preview = False)
                        return
                except:
                    media = event.media.document
                    await Bot.send_file(i, media, caption = event.text, link_preview = False)
                    return
            else:
                logging.info(event.text)
                str1 = "Forwarded _|_: %s" %event.text
                send_message_bot(str1, bot_token, chat_id)
                await Bot.send_message(i, str1, link_preview = False)

        except Exception as e:
            logging.error(e)

logging.info("Bot has started.")
Bot.run_until_disconnected()