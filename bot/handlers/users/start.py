import logging
from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart

from loader import dp, db


@dp.message_handler(CommandStart())
async def botstart(message: types.Message):
    alreadyuser = await db.user_exists(message.from_user.id)
    print(alreadyuser)

    await message.answer(("Hello") + f", {message.from_user.fullname}!")
