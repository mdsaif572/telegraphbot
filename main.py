import os
from telegraph import upload_file
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

Bot = Client(
    "Telegraph Uploader Bot",
    bot_token=os.environ.get("BOT_TOKEN"),
    api_id=int(os.environ.get("API_ID")),
    api_hash=os.environ.get("API_HASH")
)

DOWNLOAD_LOCATION = os.environ.get("DOWNLOAD_LOCATION", "./DOWNLOADS/")


START_CAPTION = """*ʜᴇʏ* {}, 🥀
*๏ ᴛʜɪs ɪs* {} !

➻ ꜱᴇɴᴅ ᴀɴʏ ʙᴇʟᴏᴡ 5ᴍʙ ᴘʜᴏᴛᴏ/ᴠɪᴅᴇᴏ ᴛᴏ ɢᴇᴛ ᴛᴇʟᴇɢʀᴀᴘʜ ʟɪɴᴋ 

──────────────────
๏ ᴛʜᴀɴᴋꜱ ʙʏ 💞 @ᴘʀɪᴠᴀᴛᴇꜱ_ʀᴏʙᴏᴛ"""

START_BUTTONS = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton('✨ 𝚄𝙿𝙳𝙰𝚃𝙴𝚂 𝙲𝙷𝙰𝙽𝙽𝙴𝙻', url='https://telegram.me/Privates_RoBot')
        ]
    ]
)

@Bot.on_callback_query()
async def cb_data(bot, update):
    if update.data == "home":
        await update.message.edit_text(
            text=START_TEXT.format(update.from_user.mention),
            disable_web_page_preview=True,
            reply_markup=START_BUTTONS
        )
    else:
        await update.message.delete()

@Bot.on_message(filters.private & filters.command(["start"]))
async def start(bot, update):
    # Send the start photo with caption
    await bot.send_photo(
        chat_id=update.chat.id,
        photo="https://graph.org/file/50319ca29329595238b54.jpg",  # Replace with the URL of your start photo
        caption=START_TEXT.format(update.from_user.mention) + "\n\n" + START_CAPTION,
        reply_markup=START_BUTTONS
    )

@Bot.on_message(filters.private & filters.media)
async def getmedia(bot, update):
    medianame = DOWNLOAD_LOCATION + str(update.from_user.id)
    try:
        message = await update.reply_text(
            text="`ᴘʀᴏᴄᴇꜱꜱɪɴɢ...`",
            quote=True,
            disable_web_page_preview=True
        )
        await bot.download_media(
            message=update,
            file_name=medianame
        )
        response = upload_file(medianame)
        try:
            os.remove(medianame)
        except:
            pass
    except Exception as error:
        text=f"Error :- <code>{error}</code>"
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton('More Help', callback_data='help')]]
        )
        await message.edit_text(
            text=text,
            disable_web_page_preview=True,
            reply_markup=reply_markup
        )
        return
    text=f"**Link :-** `https://telegra.ph{response[0]}`\n\n**Join :-** @Privates_RoBot"
    reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton(text="ᴏᴘᴇɴ ʟɪɴᴋ 🛡️", url=f"https://telegra.ph{response[0]}"),
                InlineKeyboardButton(text="ꜱʜᴇʀᴇ ʟɪɴᴋ 🗡️", url=f"https://telegram.me/share/url?url=https://telegra.ph{response[0]}")
            ]
        ]
    )
    await message.edit_text(
        text=text,
        disable_web_page_preview=True,
        reply_markup=reply_markup
    )

Bot.run()
            
