import asyncio
import json

import websockets
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters.command import Command
from aiogram.types import Message
from aiogram.utils.keyboard import InlineKeyboardBuilder

bot = Bot(token="8194324385:AAFGwgRg_IfZA0lrqWVp5xEgEDhLhdFDmyg")
WEB_SOCKET = "ws://localhost:8000/ws"
dp = Dispatcher()

wait_artikul = False
user_tasks = {}


@dp.message(Command("start"))
async def cmd_random(message: types.Message):
    builder = InlineKeyboardBuilder()
    builder.add(types.InlineKeyboardButton(
        text="Ввести артикул",
        callback_data="fill")
    )
    await message.answer(
        "Введите артикул с wb",
        reply_markup=builder.as_markup()
    )


@dp.callback_query(F.data == "fill")
async def send_random_value(callback: types.CallbackQuery):
    global wait_artikul
    wait_artikul = True
    await callback.message.answer("Введите артикул")


@dp.message(F.text)
async def connect(message: Message):
    global wait_artikul
    if wait_artikul:
        user_id = message.chat.id

        task = asyncio.create_task(handle_websocket(user_id, int(message.text)))
        if user_id not in user_tasks:
            user_tasks[user_id] = []
        user_tasks[user_id].append(task)

        await message.reply("Подключение к WebSocket установлено. Ожидайте сообщений.")
    else:
        await message.answer(f"Начните со старта\n\n")


async def handle_websocket(user_id, artikul):
    async with websockets.connect(WEB_SOCKET) as websocket:
        await websocket.send(json.dumps({"action": "subscribe",
                                         "artikul": artikul}))

        try:
            while True:
                try:
                    data = await websocket.recv()
                    json_data = json.loads(data)

                    text = (f"Артикул: {json_data['artikul']}\n"
                            f"Название: {json_data['name']}\n"
                            f"Цена: {json_data['price']}\n"
                            f"Рейтинг: {json_data['rating']}\n"
                            f"Кол-во: {json_data['count']}\n")

                    await bot.send_message(chat_id=user_id, text=text)
                except websockets.ConnectionClosed as e:
                    print(f"Соединение закрыто для пользователя {user_id}: {e}")
                    break
        except Exception as e:
            print(f"Ошибка соединения для пользователя {user_id}: {e}")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
