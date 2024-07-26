from pyrogram import Client, filters


@Client.on_message(filters.command(["start"]))
async def start(_, message):
	await message.reply("Send Me ReelsShort Link to Download:")
		
