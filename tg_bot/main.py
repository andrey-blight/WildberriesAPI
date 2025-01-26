from aiogram import Bot, Dispatcher, types, Router
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters.callback_data import CallbackData
import asyncio
import websockets

# Создаем FSM для управления состояниями
class ProductStates(StatesGroup):
    waiting_for_article = State()

# CallbackData для кнопки
class ProductCallback(CallbackData, prefix="product"):
    action: str

# Инициализация бота и роутера
bot = Bot(token="8194324385:AAFGwgRg_IfZA0lrqWVp5xEgEDhLhdFDmyg")
dp = Dispatcher()
router = Router()  # Используем Router

# Кнопка "Получить данные по товару"
@router.message(Command("start"))
async def start(message: types.Message):
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="Получить данные по товару",
                callback_data=ProductCallback(action="get_data").pack()  # Используем метод pack()
            )]
        ]
    )
    await message.answer("Выберите действие:", reply_markup=keyboard)

# Обработка нажатия кнопки
@router.callback_query(ProductCallback.filter())
async def ask_for_article(callback: types.CallbackQuery, callback_data: ProductCallback, state: FSMContext):
    if callback_data.action == "get_data":  # Проверяем значение action
        await callback.message.answer("Введите артикул товара:")
        await state.set_state(ProductStates.waiting_for_article)
        await callback.answer()

# Ожидание ввода артикула и запрос через WebSocket
@router.message(ProductStates.waiting_for_article)
async def get_product_data(message: types.Message, state: FSMContext):
    article = message.text  # Артикул, введенный пользователем

    # Подключение к WebSocket-серверу
    async with websockets.connect("ws://your_websocket_server_url") as websocket:
        await websocket.send(article)  # Отправляем артикул на сервер
        response = await websocket.recv()  # Получаем данные

    # Отправка данных пользователю
    await message.answer(f"Данные по артикулу {article}:\n{response}")
    await state.clear()  # Сброс состояния

# Запуск бота
async def main():
    dp.include_router(router)  # Подключаем маршруты к диспетчеру
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())