import asyncio
import json
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

import db

# Завантажуємо змінні середовища
load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://mriamys.site/webapp/index.html")

# Ініціалізація бази даних
db.init_db()

# Налаштування логування (згідно стандартів)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Створює головну клавіатуру з кнопками."""
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(
                    text="🍕 Замовити піцу", web_app=WebAppInfo(url=WEBAPP_URL)
                )
            ],
            [KeyboardButton(text="🛠 Адмін-панель")],
        ],
        resize_keyboard=True,
    )
    return keyboard


@dp.message(Command("start"))
async def cmd_start(message: types.Message) -> None:
    """Обробник команди /start."""
    await message.answer(
        "Вітаємо у нашій піцерії! 🍕\nНатисніть кнопку нижче, щоб зробити замовлення.",
        reply_markup=get_main_keyboard(),
    )


@dp.message(F.text == "🛠 Адмін-панель")
async def btn_admin(message: types.Message) -> None:
    """Обробник кнопки 'Адмін-панель'."""
    orders = db.get_orders()
    if not orders:
        await message.answer("Замовлень поки немає.")
        return

    text = "📋 **Останні 10 замовлень:**\n\n"
    for order in orders:
        order_id, username, items, total_price, status = order
        text += f"ID: {order_id} | Клієнт: {username}\nЗамовлення: {items}\nСума: {total_price} грн | Статус: {status}\n---\n"

    await message.answer(text, parse_mode="Markdown")


@dp.message(F.web_app_data)
async def web_app_handler(message: types.Message) -> None:
    """Обробник даних від Web App."""
    try:
        data = json.loads(message.web_app_data.data)
        items = data.get("items", "Невідомо")
        total = data.get("total", 0)

        username = message.from_user.username or message.from_user.first_name

        # Зберігаємо у базу
        db.add_order(message.from_user.id, username, items, total)

        await message.answer(
            f"✅ Дякуємо за замовлення, {username}!\nВи замовили: {items}\nСума до сплати: {total} грн.",
            reply_markup=get_main_keyboard(),
        )
        logger.info(f"Нове замовлення від {username}: {items} на суму {total}")

    except Exception as e:
        logger.error(f"Помилка обробки замовлення: {e}")
        await message.answer("Сталася помилка при обробці вашого замовлення.")


async def main() -> None:
    logger.info("Запуск бота...")
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
