from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import Message
from tgbot.config import load_config

import json

from texts import hello_text, reg_done_text

import logging

user_router = Router()
cfg =load_config("cfg.json")
password = cfg.tg_bot.password


@user_router.message(CommandStart())
async def user_start_com(message: Message):
    user_id = message.from_user.id
    text = hello_text(message.from_user.first_name)
    await message.reply(text)
    logging.info(f"New active from {user_id}")

@user_router.message(F.text == password)
async def passed(mes: Message):
    user_id = mes.from_user.id
    with open("cfg.json", "r+", encoding="utf-8") as f:
        data = json.load(f)
        data["main"]["ADMINS"].append(user_id)
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()
    dt = reg_done_text()
    await mes.reply(dt)


@user_router.message(F.text != password)
async def non_passed(mes: Message):
    await mes.reply("Wrong password! Try again...")



