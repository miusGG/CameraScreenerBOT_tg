from aiogram import Router
from aiogram.types import Message
from aiogram import F
from texts import hello_text, help_text
from tgbot.config import load_config

import logging

from tgbot.keyboards.inline import menu_keyboard
from pathlib import Path

cfg =load_config("cfg.json")
folder_photo = cfg.tg_bot.path_photo

all_text_router = Router()

async def menu_enject(message):
    text = hello_text(message.from_user.first_name)
    await message.reply(text, reply_markup=menu_keyboard())
    logging.info("TEST ON START!")


async def help_enject(message):
    t = help_text()
    await message.answer("❓ Help with bot:\n" + t)

@all_text_router.message(F.text == "/clear")
async def clearing(mes: Message):
    await mes.reply("Удаляем все фото...")
    folder = Path(folder_photo)
    for file_path in folder.rglob('*'):
        if file_path.is_file():
            file_path.unlink()
    await mes.reply("Удаление прошло!\nПроверьте, в /menu.")

@all_text_router.message(F.text)
async def menu_text(message: Message):
    if message.text == "m":
        await menu_enject(message)
    elif message.text == "h":
        await help_enject(message)
        pass
    else:
        await message.reply("Wrong command!")

