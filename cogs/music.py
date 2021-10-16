import os
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
        return
    
    reply_message.edit(f"`Uploading {title}.`")

    try:
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            info_dict = ydl.extract_info(link, download=False)
            audio = ydl.prepare_filename(info_dict)
            reply_message.edit(f"`Uploading {title}..`")
            ydl.process_info(info_dict)
        caption = f"🎶 <b>Title:</b> <a href='{link}'>{title}</a>\n⌚ <b>Duration:</b> <code>{duration}</code>\n📻 <b>Uploaded By:</b> <a href='https://t.me/chotu_music_bot'>Chotu Music Bot 👶🤘</a>"
        secmul = 1
        dur = 0
        dur_arr = duration.split(":")

        reply_message.edit(f"`Uploading {title}...`")
        for i in range(len(dur_arr) - 1, -1, -1):
            dur += int(dur_arr[i]) * secmul
            secmul *= 60

        reply_message.edit(f"`Uploading {title}....`")
        message.reply_audio(audio, caption=caption, parse_mode='HTML', quote=False, title=title, duration=dur, thumb=thumbnail_name)
        reply_message.delete()
    except Exception as e:
        reply_message.edit("**If you're reading this, make a issue on this <a href='https://github.com/Pragmatic-Programmers/chotu-telegram/issues'>Github Repo</a>**")
        message.reply(f"Paste this in the issue:\n`Error: {e}\nSong Name: {title}\nLink: {link}\nDuration: {duration}\nAny other comment from your side:`")
    
    os.remove(audio)
    os.remove(thumbnail_name)
