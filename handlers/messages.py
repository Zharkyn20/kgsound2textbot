# -*- coding: utf-8 -*-
__author__ = 'Nikolay Mamashin (mamashin@gmail.com)'

from loguru import logger
from aiogram import types
from aiogram import F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.types import Message

from bot import telegram_router


@telegram_router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f"Саламатсызбы, {hbold(message.from_user.full_name)}!\n" +
                        "Мен JardamAI. Кандай суроо боюнча келдиңиз?" +
                        "Суроонузду аудио же текст форматында берсеңиз болот.")
