from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject

import service
import subscribers


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    subscribers.add_subscriber(message.chat.id)
    await message.answer("Привет! Это парсер новостей сайта КРСУ. Как только новость появится на сайте, бот сразу сообщит об этом!\n- /stop отписка от новостей\n- /latest {число} показывает количество последних новостей, которые хочешь увидеть")


@router.message(Command("stop"))
async def cmd_stop(message: Message):
    unsubscription = subscribers.remove_subscriber(message.chat.id)
    if unsubscription:
        await message.answer("Жаль, что ты отписался ;(")
    else:
        await message.answer("Отказано! Ты и так не был подписан!")


@router.message(Command(commands=["latest"]))
async def send_latest(message: Message, command: CommandObject):
    arg = command.args

    if not arg:
        await message.answer("Пожалуйста, после команды /latest напишите количество новостей (1-10)")
        return

    try:
        count = int(arg)
        number_of_news = len(service.get_latest(count))

        if number_of_news == 0:
            await message.answer("Новостей пока нет!")
            return

        if count < 1 or count > 10:
            await message.answer("Пожалуйста, введите число от 1 до 10!")
            return

        if count > number_of_news:
            await message.answer((f"Нашлось только {number_of_news} новостей:\n", service.format_news(service.get_latest(number_of_news))), parse_mode = "HTML")
            return

    except ValueError:
        await message.answer("При вызове /latest ввели не число! Введите число")
        return

    await message.answer(service.format_news(service.get_latest(count)), parse_mode = "HTML")


@router.message(Command(commands = ["show_subscribers"]))
async def show_subscribers(message: Message):
    await message.answer(str(subscribers.get_subscribers()))

