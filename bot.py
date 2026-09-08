import asyncio
import os
import json
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
from dotenv import load_dotenv
import db

# Завантажуємо змінні з .env файлу
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')
WEBAPP_URL = os.getenv('WEBAPP_URL')

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Ініціалізація клавіатури з Web App
def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍕 Меню (Web App)", web_app=WebAppInfo(url=WEBAPP_URL))],
            [KeyboardButton(text="📊 Статистика (Адмін)")]
        ],
        resize_keyboard=True
    )
    return keyboard

@dp.message(CommandStart())
async def cmd_start(message: Message):
    # Зберігаємо користувача в БД
    db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name)
    await message.answer(
        "Привіт! Я бот-піцерія 🍕\n"
        "Натисни кнопку нижче, щоб відкрити меню і зробити замовлення.",
        reply_markup=get_main_keyboard()
    )

# Обробка даних з Web App
@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    # Дані приходять у форматі JSON
    data = json.loads(message.web_app_data.data)
    items = data.get('items', '')
    total = data.get('total', 0)
    
    # Записуємо замовлення в базу
    db.add_order(message.from_user.id, items, total)
    
    await message.answer(
        f"✅ Ваше замовлення успішно прийнято!\n\n"
        f"📋 Склад: {items}\n"
        f"💰 Сума: {total} грн\n\n"
        f"Дякуємо, що обрали нас!"
    )

# Проста адмінка для показу статистики
@dp.message(F.text == "📊 Статистика (Адмін)")
async def admin_stats(message: Message):
    total_orders, total_revenue = db.get_stats()
    await message.answer(
        f"📈 Статистика піцерії:\n\n"
        f"📦 Всього замовлень: {total_orders}\n"
        f"💵 Загальна виручка: {total_revenue} грн"
    )

async def main():
    print("Бот запущений!")
    db.init_db()  # Створюємо таблиці, якщо їх ще немає
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
