from aiogram.types import Message
from core.keyboards.main_keyboard import get_main_keyboard
from core.utils.parse_call import find_shoes as my_shoes


async def get_start(message: Message):
    await message.answer(f'Привіт, кохана! 😍 \nГотова до шопингу? )',
                         reply_markup=get_main_keyboard())


async def find_shoes(message: Message):
    await message.answer('Шукаємо...')

    shoes_cards = await my_shoes()
    for each_answer in shoes_cards:
        await message.answer(
            each_answer,
            parse_mode='HTML'
        )
