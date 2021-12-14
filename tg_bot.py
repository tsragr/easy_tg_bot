from main import get_data_playlists, get_playlist_videos
import logging
import json
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import Text
from aiogram.utils.markdown import hbold, hlink
from dotenv import load_dotenv
import os

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')
logging.basicConfig(level=logging.INFO)

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot)
YOUTUBE_LINK = os.getenv('YOUTUBE_LINK')
TWITCH_LINK = os.getenv('TWITCH_LINK')


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    start_buttons = ["🤖 youtube's playlists", ]
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*start_buttons)
    await message.answer('Hello)', reply_markup=keyboard)


@dp.message_handler(commands=['youtube', 'twitch'])
async def youtube_twitch(message: types.Message):
    if message.get_command() == '/youtube':
        await message.answer(YOUTUBE_LINK)
    elif message.get_command() == '/twitch':
        await message.answer(TWITCH_LINK)


@dp.message_handler(Text(equals="🤖 youtube's playlists"))
async def get_playlists(message: types.Message):
    await message.answer('Please waiting....')
    get_data_playlists()

    with open('playlists_data.json', 'r') as file:
        data = json.load(file)

    buttons = []
    for item in data:
        buttons.append(f"{item.get('playlist_title')}")

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*buttons)
    await message.answer('Playlists', reply_markup=keyboard)


@dp.message_handler()
async def get_videos(message: types.Message):
    with open('playlists_data.json', 'r') as file:
        data = json.load(file)

    for item in data:
        if message.text == item.get('playlist_title'):
            get_playlist_videos(item.get('playlist_id'))
            break

    with open('playlist_videos.json', 'r') as file:
        data_videos = json.load(file)

    for item_video in data_videos:
        card = f"{hlink(item_video.get('video_title'), item_video.get('video_url'))} \n" \
               f"{item_video.get('video_image')} \n" \
               f"{item_video.get('video_description')}"

        await message.answer(card)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
