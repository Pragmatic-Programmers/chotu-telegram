import youtube_dl
from youtube_search import YoutubeSearch
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup


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

