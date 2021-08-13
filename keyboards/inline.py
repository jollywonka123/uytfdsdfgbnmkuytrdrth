from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import chat, chanel
from .callback_datas import ref_callback, accept_callback, service_callback, okey_callback

rules = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🧾Правила', callback_data='rules')
    ]
])

zayavka = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🧾Подать заявку', callback_data='zayavka')
    ]
])

accept_rules = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='✅Принять правила', callback_data='accept_rules')
    ]
])

ref = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🤝Друзья', callback_data=ref_callback.new(who='Друзья')),
    ],
    [
        InlineKeyboardButton(text='📃Реклама', callback_data=ref_callback.new(who='Реклама'))
    ],
    [
        InlineKeyboardButton(text='📺LOLZTEAM', callback_data=ref_callback.new(who='LOLZTEAM'))
    ]
])

send_zayavka = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='📮Отправить заявку', callback_data='send zayavka'),
        InlineKeyboardButton(text='🗑Заполнить заново', callback_data='zayavka')
    ]
])

accepted = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='💎Чат воркеров', url=chat),
        InlineKeyboardButton(text='💸Выплаты', url=chanel)
    ],
    [
        InlineKeyboardButton(text='🧰Меню воркера', callback_data='menu_work')
    ]
])

service = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🚗BBC', callback_data=service_callback.new(what='БлаБлаКар'))
    ],
    [
        InlineKeyboardButton(text='👟Vinted', callback_data=service_callback.new(what='Vinted'))
    ]
])

okey = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='✅Да', callback_data=okey_callback.new(act='Да')),
        InlineKeyboardButton(text='❌Нет', callback_data=okey_callback.new(act='Нет'))
    ]
])

inform = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='💎Чат воркеров', url=chat),
        InlineKeyboardButton(text='💸Выплаты', url=chanel)
    ]
])

choose_service = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🏛Grailed', callback_data='grailed')
    ]
])

cheta = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='🏴А󠁧󠁢󠁥󠁮󠁧󠁿нглия', callback_data='uk'),
        InlineKeyboardButton(text='🇧🇪Бельгия', callback_data='be')
    ]
])

pay_pal = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='✅Да', callback_data=okey_callback.new(act='Да')),
        InlineKeyboardButton(text='❌Нет', callback_data=okey_callback.new(act='Нет'))
    ]
])
