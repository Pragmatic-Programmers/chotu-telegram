import re
import youtube_dl
import requests
import time
from youtube_search import YoutubeSearch
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


# /start command
@Client.on_message(filters.command('start') & filters.private)
async def start(client, message):
    await message.reply_animation(
        animation="https://tenor.com/view/baby-music-listening-to-music-happy-baby-gif-22195024",
        caption=f"<b>Hello {message.from_user.mention}!\nI am Chotu 👶🎧\n\nSend me a song name of your choice along /song command\n& I will upload it here for you 🎧🤘</b>",
        
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Contribute 👩‍💻", url="https://github.com/Pragmatic-Programmers/chotu-telegram"),
                    InlineKeyboardButton("Buy us a coffee ☕", url="http://pragmaticprogrammer.in")
                ],
                [
                    InlineKeyboardButton("Join Community", url="http://pragmaticprogrammer.in"),
                    InlineKeyboardButton("Message Developer", url="https://telegram.dog/h4x0r47")
                ]
            ]
        ),
    reply_to_message_id=message.message_id
    )


# /song command
@Client.on_message(filters.command(['song']))
def song(client, message):
    query = ""
    for i in message.command[1:]:
        query += ' ' + str(i)
    
    reply_message = message.reply('`Hold on! fetching music details.`')
    ydl_options = {"format": "bestaudio[ext=m4a]"}

    try:
        results = []
        count = 0
        
        while len(results) == 0 and count < 6:
            if count > 0:
                time.sleep(1)
            results = YoutubeSearch(query, max_results=1).to_dict()
            #print(results)
            count += 1
        
        try:
            link = f"https://youtube.com{results[0]['url_suffix']}"
            title = results[0]["title"]
            thumbnail = results[0]["thumbnails"][0]
            duration = results[0]["duration"]
            views = results[0]["views"]

            thumbnail_name = f"{title}{message.message_id}.jpg"
            thumb = requests.get(thumbnail, allow_redirects=True)
            open(thumbnail_name, 'wb').write(thumb.content)

        except Exception as e:
            print(e)
            reply_message.edit("No Match Found 😒")
            return
    except Exception as e:
        print(e)
        reply_message.edit("**Use Command: ** `/song name-of-song`")
