from pytgbot import Bot
import logging
logging.basicConfig(level=logging.DEBUG)

API_KEY='6548756897:AAFuUVTDRc4bPLG44jOhYwcMAOlFLU-GJ4Y'
CHAT='@myproxy786'
bot = Bot(API_KEY)

# res = bot.send_message(CHAT, "Example Text FROM BOT!")
# res = bot.edit_message_text("Example Text EDIT FROM BOT!", CHAT, 25)
bot.delete_message(CHAT,25)
# print(res.message_id)
