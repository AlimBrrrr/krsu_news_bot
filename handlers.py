from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

import service
import subscribers


router = Router()

@router.message(Command("start"))
async def cmd_start(message: Message):
    subscription = subscribers.add_subscriber(message.chat.id)
    if subscription:
        await message.answer("Привет! Ты подписался на парсер новостей сайта КРСУ")
    else:
        await message.answer("Ты уже подписан!")


@router.message(Command("stop"))
async def cmd_stop(message: Message):
    unsubscription = subscribers.remove_subscriber(message.chat.id)
    if unsubscription:
        await message.answer("Жаль, что ты отписался ;(")
    else:
        await message.answer("Отказано! Ты и так не был подписан!")


@router.message(Command("news"))
async def send_news(message: Message):
    list_news = await service.get_news()

    if list_news == []:
        await message.answer("Новых новостей пока нет!")

    else:
        await message.answer(str(list_news))
