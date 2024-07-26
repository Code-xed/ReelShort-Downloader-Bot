from pyrogram import Client

@Client.on_message()
async def other(_, message):
	await message.reply("Please use /download url to download")