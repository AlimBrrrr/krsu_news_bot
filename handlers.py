from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandObject
from aiogram.enums import ParseMode
import html

import service
import subscribers


router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message):
    subscribers.add_subscriber(message.chat.id)
    await message.answer("Привет! Это парсер новостей сайта КРСУ. Нажимая на /start, ты подписываешься на новости. Как только новость появится на сайте, бот сразу сообщит об этом!\n- /subscribe подписка на бота\n- /stop отписка от новостей\n- /latest {число} показывает количество последних новостей, которые хочешь увидеть")


@router.message(Command("subscribe"))
async def cmd_start(message: Message):
    subscription = subscribers.add_subscriber(message.chat.id)
    if subscription:
        await message.answer("Ты успешно подписался на новостной бот")
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
    list_news = await service.check_news()

    if list_news == []:
        await message.answer("Новых новостей пока нет!")

    else:
        await message.answer(format_news(list_news), parse_mode = "HTML")


@router.message(Command(commands=["latest"]))
async def send_latest(message: Message, command: CommandObject):
    arg = command.args

    if not arg:
        await message.answer("Пожалуйста, после команды /latest напишите количество новостей (1-10)")
        return

    try:
        count = int(arg)
        if service.get_latest(count) == 0:
            await message.answer("Новостей пока нет!")
            return

    except ValueError:
        await message.answer("При вызове /latest ввели не число! Введите число")
        return

    if count < 1 or count > 10:
        await message.answer("Пожалуйста, введите число от 1 до 10!")
        return

    number_of_news = len(service.get_latest(count))

    if count > number_of_news:
        await message.answer(format_news(service.get_latest(number_of_news)), parse_mode = "HTML")
        return

    await message.answer(format_news(service.get_latest(count)), parse_mode = "HTML")

    
def format_news(item: list[dict]) -> str:
    msg = ""
    for card in item:
        title, link, date = card["title"], card["link"], card["date"]
        title = html.escape(title, quote = True)
        link = html.escape(link, quote = True)
        date = html.escape(date, quote = True)
        msg += (f'<b> - {title}</b>\n{date}, <a href="{link}">Ссылка</a>\n\n')

    return msg

