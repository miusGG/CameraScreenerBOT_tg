from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def get_reply_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    builder.button(text="Привет 👋")
    builder.add(
        KeyboardButton(text="Меню 🍔"),
        KeyboardButton(text="Настройки ⚙️")
    )
    # Метод .row() добавляет кнопки в новый ряд
    builder.row(
        KeyboardButton(text="Поделиться контактом", request_contact=True), # Запрос контакта
        KeyboardButton(text="Поделиться локацией", request_location=True) # Запрос локации
    )

    # Возвращаем готовую клавиатуру, при необходимости меняем ее поведение
    return builder.as_markup(
        resize_keyboard=True,     # Уменьшает размер клавиатуры
        one_time_keyboard=False,  # Скрывает клавиатуру после нажатия (False = не скрывает)
        is_persistent=True,       # Клавиатура остается видимой после отправки сообщения
        input_field_placeholder="Выберите действие..." # Подсказка в поле ввода
    )