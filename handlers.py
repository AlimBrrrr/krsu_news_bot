from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import service


router = Router()

@router.message(Command("start"))
async def start(message: Message):
    await message.answer("Hello!")


@router.message(Command("news"))
async def send_news(message: Message):
    list_news = await service.get_news()

    if list_news == []:
        await message.answer("Новых новостей пока нет!")

    else:
        await message.answer(str(list_news))
