# import asyncio
# import aiojobs

from dotenv import load_dotenv
from cron import fetch_new_proxties
from Context import Context
from utils.TelegramAPI import TelegramAPI
from utils.BotAPI import BotAPI


def main():
    load_dotenv()
    context = Context()
    telegramAPI = TelegramAPI()
    # fetch_new_proxties.start(context, telegramAPI)
    # print('here')
    # telegramAPI.idle()

    # botAPI = BotAPI('@myproxy786')
    # result = botAPI.send_message("Test message 786 - Pin")
    # message_id = result.message_id
    # result = botAPI.pin_chat_message(message_id, False)
    # message_id = botAPI.edit_message_text("Test2 message 786", message_id)


if __name__ == "__main__":
    main()
