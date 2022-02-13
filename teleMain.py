import os

from telethon import TelegramClient, events
from decouple import config
import logging
from telethon.sessions import StringSession

logging.basicConfig(filename='app.log', format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

print("Starting...")

# Basics
#APP_ID = config("APP_ID", default=None, cast=int)
APP_ID = "19859411"
#API_HASH = config("API_HASH", default=None)
API_HASH = "eb27349b19f7020edb828118b45f647d"
#FROM_ = config("FROM_CHANNEL")
FROM_ = "1249862622"
#TO_ = config("TO_CHANNEL")
TO_ = "1249862622"
#string = os.environ.get('SESSION')
string1 = "incog"

FROM = [int(i) for i in FROM_.split()]
TO = [int(i) for i in TO_.split()]

try:
    #Bot = TelegramClient(StringSession(string), APP_ID, API_HASH)
    Bot = TelegramClient(string1, APP_ID, API_HASH)
    Bot.start()
except Exception as ap: 
    print(f"ERROR - {ap}")
    exit(1) 

#@Bot.on(events.NewMessage(incoming=True, chats=FROM))
@Bot.on(events.NewMessage(incoming=True))
async def send(event):
    print(event)
    logging.info(event.text)
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
                str1 = "Forwarding %s" %event.text
                await Bot.send_message(i, str1, link_preview = False)

        except Exception as e:
            print(e)

print("Bot has started.")
Bot.run_until_disconnected()