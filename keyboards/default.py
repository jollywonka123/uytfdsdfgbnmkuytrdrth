from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

admin_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='👀Рассмотреть заявки')
        ],
        [
            KeyboardButton(text='📢Сделать рассылку')
        ],
        [
            KeyboardButton(text='💸Новое поступление'),
            KeyboardButton(text='💹Повысить ставку')
        ],
        [
            KeyboardButton(text='🎯Управление счетами')
        ]
    ],
    resize_keyboard=True
)

worker_panel = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🖼Отрисовка')
        ],
        [
            KeyboardButton(text='🧿PayPal'),
            KeyboardButton(text='💳Счет')
        ],
        [
            KeyboardButton(text='💼Профиль'),
            KeyboardButton('🗂Информация')
        ]
    ],
    resize_keyboard=True
)

upr_sch = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='🧱Добавить счет'),
            KeyboardButton(text='💣Удалить счет')
        ],
        [
            KeyboardButton(text='🧱Добавить PayPal'),
            KeyboardButton(text='💣Удалить PayPal')
        ],

    ],
    resize_keyboard=True
)