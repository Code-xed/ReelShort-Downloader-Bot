from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from plugins.ReelShort import getEpisodeList, downloadVideo
import os

# Function to extract the book_id from a single URL
def extract_book_id(url):
    base_url = "https://stardust-h5.stardustgod.com/reelshort/shareBookPage?book_id="
    title_param = "&title="
    return url[len(base_url):url.index(title_param)]
    '''
    if url.startswith(base_url) and title_param in url:
        
    return False
    '''

@Client.on_message(filters.command("download"))
async def handle_url(_, message):
    url = message.command[1]
    book_id = extract_book_id(url)
    if not book_id:
        await message.reply("Invalid URL. Please check and try again.")
        return
    
    status_message = await message.reply("Fetching episodes...")
    
    episodes = getEpisodeList(book_id)
    if not episodes:
        await status_message.edit_text("Invalid link. Please check and try again.")
    else:
        inline_buttons = [InlineKeyboardButton("Trailer", callback_data=f"{episodes[0]}-0")]
        inline_buttons.extend(InlineKeyboardButton(f"Episode {i}", callback_data=f"{episodes[i]}-{i}") for i in range(1, len(episodes)))
        
        # Group buttons into rows (3 buttons per row)
        rows = [inline_buttons[i:i + 3] for i in range(0, len(inline_buttons), 3)]
        # Create InlineKeyboardMarkup
        ikb = InlineKeyboardMarkup(rows)
        await status_message.edit_text("Choose an episode 👇:", reply_markup=ikb)
        
@Client.on_callback_query()
async def handle_callback(_, callback_query):
    # Extract data from the callback query
    episode, index = callback_query.data.split("-")
    
    # Remove the inline keyboard by updating the message
    await callback_query.message.edit_text("Processing your request...", reply_markup=None)
    
    file = downloadVideo(episode, f"episode_{index}.ts")
    await callback_query.message.reply_video(video=file, caption=f"Here is the video for Episode {index}")
    if os.path.exists(file):
    	os.remove(file)