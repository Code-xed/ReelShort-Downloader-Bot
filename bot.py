from pyrogram import Client
import os

API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
plugins = dict(root="plugins")

if __name__ == "__main__":
    Client("bot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=
    API_HASH, plugins=plugins, in_memory=True).run()
