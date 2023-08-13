from dotenv import load_dotenv
from cron import fetch_new_proxties
from Context import Context
from TelegramAPI import TelegramAPI

def main():
    load_dotenv()    
    context = Context()
    telegramAPI = TelegramAPI()
    fetch_new_proxties.start(context, telegramAPI)        


if __name__ == "__main__":
    main()
