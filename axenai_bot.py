import asyncio
import logging
import os
import certifi
os.environ["SSL_CERT_FILE"] = certifi.where()
os.environ["REQUESTS_CA_BUNDLE"] = certifi.where()

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Message

TOKEN = "8324429340:AAGFGcRx_tBi9g5Tn6_4q4pH3GyIwOJ5tOo"
ADMIN_CHAT_ID = 808135642

logging.basicConfig(level=logging.INFO)

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())


class Survey(StatesGroup):
    name_age = State()
    experience = State()
    works = State()
    hours = State()
    why_axenai = State()


QUESTIONS = {
    Survey.name_age: "Как тебя зовут и сколько тебе лет?",
    Survey.experience: "Есть ли опыт с Claude Code, вайб-кодингом или разработкой сайтов через ИИ? Если да — расскажи коротко.",
    Survey.works: "Покажи любую свою работу — ссылка или опиши что делал.",
    Survey.hours: "Сколько часов в день готов уделять работе?",
    Survey.why_axenai: "Почему хочешь работать в AxenAI?",
}


@dp.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(
        "Привет! Я бот для приёма заявок в команду AxenAI.\n"
        "Отвечу на несколько вопросов — это займёт пару минут.\n\n"
        + QUESTIONS[Survey.name_age]
    )
    await state.set_state(Survey.name_age)


@dp.message(Survey.name_age)
async def answer_name_age(message: Message, state: FSMContext):
    await state.update_data(name_age=message.text)
    await message.answer(QUESTIONS[Survey.experience])
    await state.set_state(Survey.experience)


@dp.message(Survey.experience)
async def answer_experience(message: Message, state: FSMContext):
    await state.update_data(experience=message.text)
    await message.answer(QUESTIONS[Survey.works])
    await state.set_state(Survey.works)


@dp.message(Survey.works)
async def answer_works(message: Message, state: FSMContext):
    await state.update_data(works=message.text)
    await message.answer(QUESTIONS[Survey.hours])
    await state.set_state(Survey.hours)


@dp.message(Survey.hours)
async def answer_hours(message: Message, state: FSMContext):
    await state.update_data(hours=message.text)
    await message.answer(QUESTIONS[Survey.why_axenai])
    await state.set_state(Survey.why_axenai)


@dp.message(Survey.why_axenai)
async def answer_why_axenai(message: Message, state: FSMContext):
    await state.update_data(why_axenai=message.text)
    data = await state.get_data()
    await state.clear()

    username = f"@{message.from_user.username}" if message.from_user.username else f"id:{message.from_user.id}"

    report = (
        "Новая заявка:\n\n"
        f"Имя и возраст: {data['name_age']}\n"
        f"Опыт: {data['experience']}\n"
        f"Работы: {data['works']}\n"
        f"Часов в день: {data['hours']}\n"
        f"Почему AxenAI: {data['why_axenai']}\n"
        f"Username: {username}"
    )

    await bot.send_message(chat_id=ADMIN_CHAT_ID, text=report)
    await message.answer("Отлично! Твои ответы отправлены. С тобой свяжутся в ближайшее время.")


async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
