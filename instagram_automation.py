import time
from instabot import Bot
from requests.exceptions import HTTPError

bot = Bot()
bot.login(username="",
          password="", use_cookie=True)

try:
    bot.upload_photo(
        r"C:\Users\Vishnu\Downloads\PXL_20240525_221357830.jpg", caption="Testing")
except HTTPError as e:
    if e.response.status_code == 429:
        print("Too many requests. Sleeping for 5 minutes.")
        time.sleep(300)  # Sleep for 5 minutes
        bot.upload_photo(
            r"C:\Users\Vishnu\Downloads\PXL_20240525_221357830.jpg", caption="Testing")
    else:
        raise e
