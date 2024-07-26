from pyrogram import Client
from Config import api_id, api_hash, bot_token


plugins = dict(root="plugins")

if __name__ == "__main__":
    Client(bot_token=bot_token, api_id=api_id, api_hash=api_hash, plugins=plugins, in_memory=True).run()
