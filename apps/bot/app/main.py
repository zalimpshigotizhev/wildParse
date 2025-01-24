import asyncio
import logging
import sys
import re
from datetime import datetime
from os import getenv

from aiogram import Bot, Dispatcher, html, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from products.dao import find_product_by_artikul

TOKEN = getenv("BOT_TOKEN")
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    await message.answer(f"Пришлите артикул с Wildberries.")


@dp.message(F.text.regexp(r'^\d+$'))
async def echo_handler(message: Message) -> None:
    """
    Перехват любого сообщение в бота.
    Внутри функции проверяется сообщение на тип данных.
    Если это число, то ищется продукт с таким артикулом в БД.
    """
    product = await find_product_by_artikul(int(message.text))
    if not product:
        await message.reply(
            text=f"*Такого артикула в БД нет!*\n"
                 f"Вы можете зарегистрировать его по этому адресу - XXXXXX"
        )
    else:
        at_update: datetime = product[8]
        await message.reply(
            f"*{product[0]}*\n"
            f"*Артикул:* {product[1]}\n"
            f"*Стоимость:* {product[2] // 100} руб.\n"
            f"*Рейтинг:* {product[3]}\n"
            f"*Кол-ство единиц:* {product[4]}\n"
            f"*Последнее обновление* {at_update.strftime("%Y.%m.%d %H:%M")}\n"
        )


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.MARKDOWN))
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
