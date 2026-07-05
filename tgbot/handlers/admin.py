from idlelib.outwin import file_line_pats

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.filters.callback_data import CallbackData
from aiogram.types import Message
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile
from attr import dataclass

from tgbot.config import load_config
from pathlib import Path

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


import os

from tgbot.screener.sc_class import WebcamSaver

from texts import menu_text, help_text

import logging

from tgbot.keyboards.inline import menu_keyboard
from tgbot.filters.admin import AdminFilter

admin_router = Router()
admin_router.message.filter(AdminFilter())
cfg =load_config("cfg.json")
folder_photo = cfg.tg_bot.path_photo
cam = WebcamSaver(output_dir=folder_photo)

class PhotoCanDelete(CallbackData, prefix="del_img"):
    photo_path: str

def delete_photo_button(filename: str) -> InlineKeyboardMarkup:
    cb_data = PhotoCanDelete(photo_path=filename).pack()

    btn = InlineKeyboardButton(text="🗑 Delete", callback_data=cb_data)
    return InlineKeyboardMarkup(inline_keyboard=[[btn]])

def get_files(list_return=False):
    files = [f for f in os.listdir(folder_photo) if os.path.isfile(os.path.join(folder_photo, f))]
    files_text = "\n".join(files)
    if list_return:
        return files
    return files_text

@admin_router.message(CommandStart())
async def user_start_com(message: Message):
    text = menu_text()
    await message.reply(text, reply_markup=menu_keyboard())
    logging.info("TEST ON START!")

@admin_router.message(F.text == "/menu")
async def user_start_text(message: Message):
    await user_start_com(message)

@admin_router.message(F.text == "/clear")
async def clearing(mes: Message):
    await mes.reply("Deleted photos...")
    folder = Path(folder_photo)
    for file_path in folder.rglob('*'):
        if file_path.is_file():
            file_path.unlink()
    await mes.reply("Deleted done!\nLook in /menu.")

@admin_router.message(F.text)
async def texter(mes:Message):
    files = get_files(True)
    text = mes.text
    if text in ["m", "menu", '/menu']:
        await user_start_com(mes)
    elif text in ["shot", 'screenshot', 's', 'photo', "screen", "smile"]:
        screenshot_path = cam.take_screenshot()

        if screenshot_path:
            await mes.answer("📸 Screenshot done! Logging send! Look:")
            photo_file = FSInputFile(screenshot_path)
            reply_markup = delete_photo_button(filename=screenshot_path)
            await mes.answer_photo(photo=photo_file, caption=f"Webcam screenshot path: {screenshot_path}",
                                                reply_markup=reply_markup)
        else:
            await mes.answer("❌ Error: Failed to take a screenshot.")
    elif text in ["l", "/list", "list"]:
        files_text = get_files()
        await mes.answer("📁 Screenshots list:\n" + files_text)
    elif text in ['c', 'clear']:
        await clearing(mes)
    elif text in ['path', 'p']:
        await mes.answer(f"Path for your photos:\n{folder_photo}")
    elif text in ["/help", "h", "help", "info", "sos"]:
        t = help_text()
        await mes.answer("❓ Help with bot:\n" + t)
    elif (text in files) or ((text + '.jpg') in files):
        if ".jpg" in text:
            full_path = folder_photo + "/" + text
        else:
            full_path = folder_photo + "/" + text +'.jpg'
        photo_file = FSInputFile(full_path)
        await mes.answer_photo(photo=photo_file, caption=f"Webcam screenshot search!")
    else:
        await mes.reply("Unknown command :(")

@admin_router.callback_query(F.data == "screen")
async def process_screenshot_press(callback: CallbackQuery):
    await callback.answer("Smile face!!!")

    screenshot_path = cam.take_screenshot()

    if screenshot_path:
        await callback.message.answer("📸 Screenshot done! Logging send! Look:")
        photo_file = FSInputFile(screenshot_path)
        reply_markup = delete_photo_button(filename=screenshot_path)
        await callback.message.answer_photo(photo=photo_file, caption=f"Webcam screenshot path: {screenshot_path}",
                                            reply_markup=reply_markup)
    else:
        await callback.message.answer("❌ Error: Failed to take a screenshot.")


@admin_router.callback_query(F.data == "cfg")
async def process_config_press(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("⚙️ Settings:\nComing soon... Wait it on GitHub!")


@admin_router.callback_query(F.data == "list")
async def process_list_press(callback: CallbackQuery):
    await callback.answer()
    files_text = get_files()
    await callback.message.answer("📁 Screenshots list:\n"+files_text)


@admin_router.callback_query(F.data == "h")
async def process_help_press(callback: CallbackQuery):
    await callback.answer()
    t  =help_text()
    await callback.message.answer("❓ Help with bot:\n" + t)

@admin_router.callback_query(PhotoCanDelete.filter())
async def deleter(callback: CallbackQuery, callback_data: PhotoCanDelete):
    await callback.answer("Deleting...")
    file_path = callback_data.photo_path
    os.remove(file_path)
    await callback.message.answer("Delete done!")


