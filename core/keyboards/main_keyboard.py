from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


def get_main_keyboard() -> ReplyKeyboardMarkup:
    main_keyboard = ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(
                    text='Знайти шузи'
                ),
                # KeyboardButton(
                #     text='Налаштувати пошук'
                # )
            ]
        ],
        resize_keyboard=True, one_time_keyboard=True
    )
    return main_keyboard
