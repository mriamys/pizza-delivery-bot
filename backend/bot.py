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
    # Замінюємо index.html на admin.html для кнопки адмінки
    admin_url = WEBAPP_URL.replace('index.html', 'admin.html')
    if 'admin.html' not in admin_url:
        admin_url += '/admin.html' if not admin_url.endswith('/') else 'admin.html'

    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🍕 Замовити піцу", web_app=WebAppInfo(url=WEBAPP_URL))],
            [KeyboardButton(text="⚙️ Адмін-панель", web_app=WebAppInfo(url=admin_url))]
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
        "Натисни кнопку нижче, щоб відкрити меню і зробити замовлення, або переглянути статистику.",
        reply_markup=get_main_keyboard()
    )

# Обробка даних з Web App
@dp.message(F.web_app_data)
async def web_app_data_handler(message: Message):
    # Дані приходять у форматі JSON
    data = json.loads(message.web_app_data.data)
    
    action = data.get('action')
    if action == 'update_status':
        order_id = data.get('order_id')
        status = data.get('status')
        db.update_order_status(order_id, status)
        db.export_to_json()
        await message.answer(f"✅ Статус замовлення #{order_id} успішно змінено на '{status}'!")
        return

    items = data.get('items', '')
    total = data.get('total', 0)
    
    # Записуємо замовлення в базу та оновлюємо JSON для адмінки
    db.add_order(message.from_user.id, items, total)
    db.export_to_json()
    
    await message.answer(
        f"✅ Ваше замовлення успішно прийнято!\n\n"
        f"📋 Склад: {items}\n"
        f"💰 Сума: {total} грн\n\n"
        f"Дякуємо, що обрали нас!"
    )

async def main():
    print("Бот запущений!")
    db.init_db()  # Створюємо таблиці, якщо їх ще немає
    db.export_to_json() # Генеруємо початковий файл статистики
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
