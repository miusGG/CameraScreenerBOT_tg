from aiogram import Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile
from tgbot.config import load_config
from pathlib import Path

import os

from tgbot.screener.sc_class import WebcamSaver

from texts import hello_text, help_text

import logging

from tgbot.keyboards.inline import menu_keyboard

user_router = Router()
cfg =load_config("cfg.json")
folder_photo = cfg.tg_bot.path_photo
cam = WebcamSaver(output_dir=folder_photo)


@user_router.message(CommandStart())
async def user_start_com(message: Message):
    text = hello_text(message.from_user.first_name)
    await message.reply(text, reply_markup=menu_keyboard())
    logging.info("TEST ON START!")

@user_router.message(F.text == "/menu")
async def user_start_text(message: Message):
    text = hello_text(message.from_user.first_name)
    await message.reply(text, reply_markup=menu_keyboard())
    logging.info("TEST ON START!")

@user_router.message(F.text == "/clear")
async def clearing(mes: Message):
    await mes.reply("Удаляем все фото...")
    folder = Path(folder_photo)
    for file_path in folder.rglob('*'):
        if file_path.is_file():
            file_path.unlink()
    await mes.reply("Удаление прошло!\nПроверьте, в /menu.")

@user_router.callback_query(F.data == "screen")
async def process_screenshot_press(callback: CallbackQuery):
    await callback.answer("Smile face!!!")

    screenshot_path = cam.take_screenshot()

    if screenshot_path:
        await callback.message.answer("📸 Screenshot done! Logging send! Look:")
        photo_file = FSInputFile(screenshot_path)
        await callback.message.answer_photo(photo=photo_file, caption=f"Webcam screenshot path: {screenshot_path}")
    else:
        await callback.message.answer("❌ Error: Failed to take a screenshot.")


@user_router.callback_query(F.data == "cfg")
async def process_config_press(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("⚙️ Settings:\nComing soon... Wait it on GitHub!")


@user_router.callback_query(F.data == "list")
async def process_list_press(callback: CallbackQuery):
    await callback.answer()
    folder_path = "tgbot/screener/screenshot"
    files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    files_text = "\n".join(files)
    await callback.message.answer("📁 Screenshots list:\n"+files_text)


@user_router.callback_query(F.data == "h")
async def process_help_press(callback: CallbackQuery):
    await callback.answer()
    t  =help_text()
    await callback.message.answer("❓ Help with bot:\n" + t)



