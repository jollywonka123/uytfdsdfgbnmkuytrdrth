import requests
from main import bot, dp, sql1, db1, sql2, db2, sql3, db3
from config import admins, chanel_id
from aiogram.dispatcher.filters import Command
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from keyboards.inline import rules, zayavka, accept_rules, ref, send_zayavka, accepted, service, okey, inform, choose_service, cheta
from keyboards.callback_datas import ref_callback, paypal_callback
from aiogram.dispatcher import FSMContext
from states import Join_team, Make_r, New_payment, Increase, Paint, Dob_schet, Dob_paypal, Del_schet, Del_paypal
from keyboards.default import admin_panel, worker_panel, upr_sch
from keyboards.callback_datas import accept_callback, service_callback, okey_callback, iban_callback
from PIL import Image, ImageDraw, ImageFont

async def on_startup(dp):
    for i in admins:
        await bot.send_message(chat_id=i, text='<b>Бот запущен</b>')

@dp.message_handler(Command('start'))
async def command_start(message: Message):
    sql1.execute(f"SELECT chatid FROM users WHERE chatid = '{message.chat.id}'")
    if sql1.fetchone() is None:
        sql1.execute(f"INSERT INTO users VALUES(?,?,?,?,?)", (message.chat.id, message.from_user.username, 0, 0, 50))
        db1.commit()
    for k in sql1.execute(f'SELECT status FROM users WHERE chatid = "{message.chat.id}"'):
        if k[0] == 0:
            await message.answer(text=f'<b>Привет, {message.chat.first_name}! Перед подачей заявки ознакомься с правилами проекта</b>',reply_markup=rules)
        elif k[0] == 1:
            await message.answer(text='<b>Для подачи заявки нажите на кнопку ниже</b>', reply_markup=zayavka)

        elif k[0] == 2:
            await message.answer(text='<b>🔊Вы уже подали заявку, ожидайте.</b>')
        elif k[0] == 3:
            await message.answer(text='<b>❗Воспользуйтесь меню ниже.</b>', reply_markup=worker_panel)
        else:
            await message.answer(text='<b>🚫Ваша заявка отклонена, вы больше не сможете пользоваться ботом.</b>')

@dp.callback_query_handler(text='rules')
async def ok_rules(call: CallbackQuery):
    await call.answer(cache_time=1)
    db1.commit()
    await call.message.edit_text(text='<b>• Воркеры, не проявляющие активности в течение 14 дней, будут исключены</b>\n'
                                      '<b>• В конференции запрещен любой NSFW-контент, спам, реклама, попрошайничество, любая коммерция</b>\n'
                                      '<b>• Выяснения отношений и оскорбления в беседе также не приветствуются и будут присекаться, для этого есть ЛС</b>\n'
                                      '<b>• ТС может отказать в выплате, если воркер не состоит в чате тимы.</b>', reply_markup=accept_rules)

@dp.callback_query_handler(text='accept_rules')
async def prinat_rules(call: CallbackQuery):
    sql1.execute(f"UPDATE users SET status = 1 WHERE chatid = {call.message.chat.id}")
    db1.commit()
    await call.answer(text='✅ОК')
    await call.message.edit_text(text='<b>Для подачи заявки нажите на кнопку ниже</b>', reply_markup=zayavka)

@dp.callback_query_handler(text='zayavka', state=[None, Join_team.Q5])
async def get_zayavka(call: CallbackQuery):
    await call.message.edit_text(text='<b>💭Откуда вы о нас узнали?</b>', reply_markup=ref)
    await Join_team.Q1.set()

@dp.callback_query_handler(ref_callback.filter(), state=Join_team.Q1)
async def lolz_profile(call: CallbackQuery, callback_data: dict, state: FSMContext):
    who = callback_data.get('who')
    await state.update_data(who=who)
    await call.message.edit_text(text='<b>💭Отправьте ссылку на ваш профиль в LOLZTEAM</b>')
    await Join_team.Q2.set()

@dp.message_handler(state=Join_team.Q2)
async def time_work(message: Message, state=FSMContext):
    await state.update_data(lolzteam=message.text)
    await message.answer(text='<b>💭Сколько часов в день вы готовы уделять работе?</b>')
    await Join_team.Q3.set()

@dp.message_handler(state=Join_team.Q3)
async def opit_work(message: Message, state=FSMContext):
    await state.update_data(time=message.text)
    await message.answer(text='<b>💭Каков ваш опыт в сфере скама? Расскажите поподробней.</b>')
    await Join_team.Q4.set()

@dp.message_handler(state=Join_team.Q4)
async def join_end(message: Message, state=FSMContext):
    data = await state.get_data()
    who = data.get('who')
    lolzteam = data.get('lolzteam')
    time = data.get('time')
    await state.update_data(opit=message.text)
    await message.answer(text=f'<b>📢Откуда узнали: {who}</b>\n'
                              f'<b>📺Профиль LOLZTEAM: {lolzteam}</b>\n'
                              f'<b>⌚Сколько часов готов уделять: {time}</b>\n'
                              f'<b>⚡Опыт: {message.text}</b>', reply_markup=send_zayavka)
    await Join_team.Q5.set()

@dp.callback_query_handler(text='send zayavka', state=Join_team.Q5)
async def send_z(call: CallbackQuery, state=FSMContext):
    await call.message.edit_text(text='<b>🎉Ваша заявка успешно отправлена. В ближайшее время её рассмотрят.</b>')
    data = await state.get_data()
    who = data.get('who')
    lolzteam = data.get('lolzteam')
    time = data.get('time')
    opit = data.get('opit')
    sql1.execute(f"UPDATE users SET status = 2 WHERE chatid = {call.message.chat.id}")
    db1.commit()
    sql2.execute(f"SELECT chatid FROM zayavka WHERE chatid = '{call.message.chat.id}'")
    if sql2.fetchone() is None:
        sql2.execute(f"INSERT INTO zayavka VALUES(?,?,?,?,?,?)", (call.message.chat.id, call.message.chat.username, who, lolzteam, time, opit))
        db2.commit()
    else:
        sql2.execute(f"DELETE FROM zayavka WHERE chatid = {call.message.chat.id}")
        sql2.execute(f"INSERT INTO zayavka VALUES(?,?,?,?,?,?)", (call.message.chat.id, call.message.chat.username, who, lolzteam, time, opit))
        db2.commit()
    for i in admins:
        await bot.send_message(chat_id=i, text='<b>🔔Новая заявка!</b>')
    await state.finish()

@dp.message_handler(Command('admin'))
async def adm_panel(message:Message):
    if message.chat.id in admins:
        await message.answer(text='<b>❗Воспользуйтесь меню ниже.</b>', reply_markup=admin_panel)
    else:
        await message.answer(text='У вас нет прав.')

@dp.message_handler(text='👀Рассмотреть заявки')
async def view_zayavki(message: Message):
    if message.chat.id in admins:
        sql2.execute(f"SELECT * FROM zayavka")
        if sql2.fetchone() is None:
            await message.answer(text='<b>💤Новых заявок пока нет.</b>')

        else:
            for i in sql2.execute("SELECT * FROM zayavka"):
                accept_zayavka = InlineKeyboardMarkup(inline_keyboard=[
                    [
                        InlineKeyboardButton(text='✔Принять заявку', callback_data=accept_callback.new(action=f'accept', id=f'{i[0]}')),
                        InlineKeyboardButton(text='🗑Отклонить заявку', callback_data=accept_callback.new(action=f'dont_accept',id=f'{i[0]}'))
                    ]
                ])
                await message.answer(text=f'<b>ID: {i[0]}</b>\n'
                                          f'<b>USERNAME: @{i[1]}</b>\n'
                                          f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                          f'<b>📢Откуда узнал: {i[2]}</b>\n'
                                          f'<b>📺Профиль LOLZTEAM: {i[3]}</b>\n'
                                          f'<b>⌚Сколько часов готов уделять: {i[4]}</b>\n'
                                          f'<b>⚡Опыт: {i[5]}</b>', reply_markup=accept_zayavka)

@dp.callback_query_handler(accept_callback.filter())
async def viewing_zayavki(call: CallbackQuery, callback_data: dict):
    id = callback_data.get('id')
    action = callback_data.get('action')
    if action == 'accept':
        sql1.execute(f"UPDATE users SET status = 3 WHERE chatid = {id}")
        db1.commit()
        sql2.execute(f"DELETE FROM zayavka WHERE chatid = {id}")
        db2.commit()
        await call.message.edit_text(text='<b>🔔Вы успешно приняли в команду нового воркера.</b>')
        await bot.send_message(chat_id=id, text='<b>⚡Ваша заявка принята.⚡</b>', reply_markup=accepted)
    else:
        sql2.execute(f"DELETE FROM zayavka WHERE chatid = {id}")
        db2.commit()
        sql1.execute(f"UPDATE users SET status = 4 WHERE chatid = {id}")
        db1.commit()
        await call.message.edit_text(text='<b>🔔Вы успешно отклонили заявку.</b>')
        await bot.send_message(chat_id=id, text='<b>😞Ваша заявка отклонена</b>')

@dp.callback_query_handler(text='menu_work')
async def show_work_menu(call: CallbackQuery):
    await call.message.answer(text='<b>❗Воспользуйтесь меню ниже.</b>', reply_markup=worker_panel)

@dp.message_handler(text='💳Счет')
async def schett(message: Message):
    for k in sql1.execute(f'SELECT status FROM users WHERE chatid = "{message.chat.id}"'):
        if k[0] == 3:
            schet_2 = InlineKeyboardMarkup(row_width=1)
            for i in sql3.execute('SELECT info FROM pay WHERE service = "iban"'):
                schet_2.insert(InlineKeyboardButton(text=f'{i[0]}', callback_data=iban_callback.new(act=f'{i[0]}')))
            await message.answer(text='💳Счет', reply_markup=schet_2)

@dp.callback_query_handler(iban_callback.filter())
async def show_schet(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    act = callback_data.get('act')
    for i in sql3.execute(f'SELECT payment_details FROM pay WHERE info = "{act}"'):
        await call.message.edit_text(text=f'{i[0]}')

@dp.message_handler(text='🧿PayPal')
async def paypal(message: Message):
    for k in sql1.execute(f'SELECT status FROM users WHERE chatid = "{message.chat.id}"'):
        if k[0] == 3:
            pay_pal = InlineKeyboardMarkup(row_width=1)
            for i in sql3.execute('SELECT info FROM pay WHERE service = "paypal"'):
                pay_pal.insert(InlineKeyboardButton(text=f'{i[0]}', callback_data=paypal_callback.new(act=f'{i[0]}')))
            await message.answer(text='🧿PayPal', reply_markup=pay_pal)

@dp.callback_query_handler(paypal_callback.filter())
async def show_paypal(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=1)
    act = callback_data.get('act')
    for i in sql3.execute(f'SELECT payment_details FROM pay WHERE info = "{act}"'):
        await call.message.edit_text(text=f'{i[0]}')

@dp.message_handler(text='💼Профиль')
async def profile_info(message: Message):
    for k in sql1.execute(f'SELECT status FROM users WHERE chatid = "{message.chat.id}"'):
        if k[0] == 3:
            for i in sql1.execute(f'SELECT * FROM users WHERE chatid = "{message.chat.id}"'):
                await message.answer(text=f'<b>🌵ID: {message.chat.id}</b>\n'
                                          f'<b>🧊USERNAME: @{message.chat.username}</b>\n'
                                          f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                          f'<b>💰Залетов на сумму: {i[3]}€</b>\n'
                                          f'<b>🔗Ваш процент: {i[4]}%</b>')

@dp.message_handler(text='📢Сделать рассылку', state=None)
async def rassilka(message: Message):
    if message.chat.id in admins:
        await message.answer(text='💻Отправьте текст, который вы желаете разослать по всем пользователям бота')
        await Make_r.Q1.set()

@dp.message_handler(state=Make_r.Q1)
async def mk_r(message: Message, state=FSMContext):
    await state.finish()
    await message.answer(text='<b>📌Во время рассылки желательно никак не взаимодействовать с ботом</b>')
    error = 0
    for i in sql1.execute("SELECT chatid FROM users"):
        try:
            await bot.send_message(chat_id=i[0], text=message.text)
        except:
            error += 1
    await message.answer(text=f'<b>📌Рассылка завершилсь. Количество ошибок: {error}</b>')

@dp.message_handler(text='💸Новое поступление', state=None)
async def new_payment(message: Message):
    if message.chat.id in admins:
        await message.answer(text='<b>📦Выберите сервис</b>', reply_markup=service)
        await New_payment.Q1.set()

@dp.callback_query_handler(service_callback.filter() ,state=New_payment.Q1)
async def choice_service(call: CallbackQuery, callback_data: dict, state=FSMContext):
    what = callback_data.get('what')
    await state.update_data(what=what)
    await call.answer(f'✅Выбран сервис: {what}')
    await call.message.edit_text(text='<b>📝Введите сумму залёта в евро.</b>')
    await New_payment.Q2.set()

@dp.message_handler(state=New_payment.Q2)
async def sum_zalet(message: Message, state=FSMContext):
    await message.answer(text='<b>📝Введите ID воркера, который завез CASH.</b>')
    await state.update_data(summ=message.text)
    await New_payment.Q3.set()

@dp.message_handler(state=New_payment.Q3)
async def user_worker(message: Message, state=FSMContext):
    data = await state.get_data()
    what = data.get('what')
    summ = data.get('summ')
    await state.update_data(id=message.text)
    for i in sql1.execute(f'SELECT username FROM users WHERE chatid = "{message.text}"'):
        await message.answer(text=f'<b>📞Всё верно?</b>\n'
                                  f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                  f'<b>⚙️Сервис: {what}</b>\n'
                                  f'<b>💵Сумма залёта: {summ}€</b>\n'
                                  f'<b>🛠Воркер: {i[0]}</b>', reply_markup=okey)
    await New_payment.Q4.set()

@dp.callback_query_handler(okey_callback.filter(), state=New_payment.Q4)
async def post_chanel(call: CallbackQuery, callback_data: dict, state=FSMContext):
    await call.answer(cache_time=2)
    action = callback_data.get('act')
    if action == 'Да':
        data = await state.get_data()
        what = data.get('what')
        summ = int(data.get('summ'))
        id = data.get('id')
        await state.finish()
        try:
            for i in sql1.execute(f"SELECT * FROM users WHERE chatid = '{id}'"):
                total = int('{:.0f}'.format((summ/100)*float(i[4])))
                print(total)
                sql1.execute(f'UPDATE users SET zalet = zalet + "{total}"')
                await bot.send_message(chat_id=chanel_id, text=f'<b>🏷Новый залёт!</b>\n'
                                                               f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                                               f'<b>⚙️Сервис: {what}</b>\n'
                                                               f'<b>💵Сумма залёта: {summ}€</b>\n'
                                                               f'<b>🎚Процентная ставка: {i[4]}%</b>\n'
                                                               f'<b>🛠Воркер: {i[1]}</b>\n'
                                                               f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                                               f'<b>💳Ожидается к выплате: {total}€</b>')
                await call.message.edit_text(text='👍Пост успешно опубликован в канале с выплатами')
        except:
            await call.message.answer(text='Ошибка')


    else:
        await call.message.answer(text='🚫Отменено')
        await state.finish()


@dp.message_handler(text='💹Повысить ставку', state=None)
async def increase_percent(message: Message):
    if message.chat.id in admins:
        await message.answer(text='💬Введите ID воркера, которому надо повысить процентную ставку.')
        await Increase.Q1.set()

@dp.message_handler(state=Increase.Q1)
async def how_percent(message: Message, state=FSMContext):
    await state.update_data(id=message.text)
    try:
        for i in sql1.execute(f"SELECT * FROM users WHERE chatid = '{message.text}'"):
            await message.answer(text=f'🌵ID: {message.text}\n'
                                      f'🧊USERNAME: {i[1]}\n'
                                      f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                      f'🧮Процентная ставка: {i[4]}%')
    except:
        await message.answer(text='🚫Ошибка')
        await state.finish()
    await message.answer(text='🏷На сколько % вы хотите повысить ставку воркера?')
    await Increase.Q2.set()

@dp.message_handler(state=Increase.Q2)
async def some_up(message: Message, state=FSMContext):
    data = await state.get_data()
    id = int(data.get('id'))
    how = int(message.text)
    sql1.execute(f"UPDATE users SET percent = percent + {how} WHERE chatid = '{id}'")
    db1.commit()
    for i in sql1.execute(f"SELECT * FROM users WHERE chatid = '{id}'"):
        await message.answer(text=f'🛎Ставка воркера успешно повышена на {message.text}%. Текущая ставка {i[4]}%')
        await bot.send_message(chat_id=id, text=f'🎉Выша ставка повышена на {message.text}%\nТекущая ставка: {i[4]}%')
    await state.finish()

@dp.message_handler(text='🗂Информация')
async def info(message: Message):
    for k in sql1.execute(f'SELECT status FROM users WHERE chatid = "{message.chat.id}"'):
        if k[0] == 3:
            await message.answer(text=f'📂INFORMATION\n'
                                      f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                      f'👑ТСы: @registerq, @povishe\n'
                                      f'➖➖➖➖➖➖➖➖➖➖➖\n'
                                      f'📚Мануал по VINTED (PayPal): <a href="https://telegra.ph/Manual-po-rabote-VINTED-07-07-2">ССЫЛКА</a>\n'
                                      f'📚Мануал по VINTED (IBAN): <a href="https://telegra.ph/Manual-po-rabote-VINTED-07-07-3">ССЫЛКА</a>\n'
                                      f'📚Мануал по созданию DHL трекера: <a href="https://telegra.ph/Sozdaem-DHL-trek-nomer-onlajn-besplatno-07-08">ССЫЛКА</a>\n'
                                      f'📚Мануал по BLaBlaCar: <a href="https://telegra.ph/BlaBlaCar-Scam-EU-PAYPAL-10-07-07">ССЫЛКА</a>\n', reply_markup=inform, disable_web_page_preview=True)

@dp.message_handler(text='🖼Отрисовка')
async def otrisovka(message: Message):
    for k in sql1.execute(f'SELECT status FROM users WHERE chatid = "{message.chat.id}"'):
        if k[0] == 3:
            await message.answer(text='🔎Выберите сервис.', reply_markup=choose_service)

@dp.callback_query_handler(text='grailed', state=None)
async def grailed(call: CallbackQuery):
    await call.message.edit_text(text='Введите ссылку на изображение из этого бота -> @tlgurbot')
    await Paint.Q1.set()

@dp.message_handler(state=Paint.Q1)
async def get_link(message: Message, state=FSMContext):
    if message.text[:17] == 'https://tlgur.com':
        await state.update_data(link=message.text)
        await message.answer(text='💬Введите данные для отрисовки в формате:\n'
                                  '➖➖➖➖➖➖➖➖➖➖➖\n'
                                  'Бренд\n'
                                  'Название товара\n'
                                  'Размер\n'
                                  'Имя и Фамилия\n'
                                  'Улица, дом\n'
                                  'Город, штат, индекс\n'
                                  'Шорткод страны\n'
                                  'Цена товара целым числом в $')
        await Paint.Q2.set()
    else:
        await message.answer(text='🚫Некорректная ссылка')
        await state.finish()

@dp.message_handler(state=Paint.Q2)
async def get_info(message: Message, state=FSMContext):
    await message.answer(text='👨‍🎨Начинаю рисовать.')
    try:
        data = await state.get_data()
        link = data.get('link')
        await state.finish()
        response = requests.get(link, stream=True).raw
        img = Image.open(response)
        check = Image.open("images/grailed.png")
        num = img.height / 100
        num1 = int('{:d}'.format(int(img.height / num)))
        num2 = int('{:d}'.format(int(img.width / num)))
        img.thumbnail((num2, num1))
        font1 = ImageFont.truetype("fonts\ARLRDBD.TTF", size=15)
        font2 = ImageFont.truetype("fonts\arial.ttf", size=15)
        font3 = ImageFont.truetype("fonts\ARLRDBD.TTF", size=20)
        text_color = (0, 0, 0)
        idraw = ImageDraw.Draw(check)
        level = 1
        for i in message.text.split('\n'):
            if level == 1:
                check.paste(img, (62, 411))
                idraw.text((281, 428), i, text_color, font1)
                idraw.text((281, 476), '"RepReceipt" (GS)', text_color, font2)
            elif level == 2:
                idraw.text((281, 453), i, text_color, font2)
            elif level == 3:
                idraw.text((281, 500), i, text_color, font2)
            elif level == 4:
                idraw.text((499, 428), i, text_color, font1)
            elif level == 5:
                idraw.text((499, 453), i, text_color, font2)
            elif level == 6:
                idraw.text((499, 476), i, text_color, font2)
            elif level == 7:
                idraw.text((499, 500), i, text_color, font2)
            elif level == 8:
                idraw.text((384, 619), f'{i}.00$', text_color, font3)
            level += 1
        check.save('images/ready_img.png')
        with open('images/ready_img.png', 'rb') as photo:
            await message.answer_photo(photo=photo)
    except:
        await message.answer(text='😐Ошибка')
        await state.finish()

@dp.message_handler(text='🎯Управление счетами')
async def upr_schet(message: Message):
    if message.chat.id in admins:
        await message.answer(text='💬Выберите действие', reply_markup=upr_sch)

@dp.message_handler(text='🧱Добавить счет')
async def dob_schet(message: Message):
    if message.chat.id in admins:
        await message.answer(text='💬Введите реквизиты')
        await Dob_schet.Q1.set()

@dp.message_handler(state=Dob_schet.Q1)
async def dob_schet(message: Message, state=FSMContext):
    await state.update_data(recs=message.text)
    await message.answer(text='💬Введите информацию, которая будет отображаться на кнопке')
    await Dob_schet.Q2.set()

@dp.message_handler(state=Dob_schet.Q2)
async def dob_schet2(message: Message, state=FSMContext):
    data = await state.get_data()
    recs = data.get('recs')
    info = message.text
    await state.finish()
    sql3.execute(f"INSERT INTO pay VALUES(?,?,?)", ('iban', recs, info))
    db3.commit()
    await message.answer(text='✅Счет успешно добавлен')

@dp.message_handler(text='🧱Добавить PayPal')
async def dob_paypal(message: Message):
    if message.chat.id in admins:
        await message.answer(text='💬Введите реквизиты')
        await Dob_paypal.Q1.set()

@dp.message_handler(state=Dob_paypal.Q1)
async def dob_paypall(message: Message, state=FSMContext):
    await state.update_data(recs=message.text)
    await message.answer(text='💬Введите информацию, которая будет отображаться на кнопке')
    await Dob_paypal.Q2.set()

@dp.message_handler(state=Dob_paypal.Q2)
async def dob_paypal2(message: Message, state=FSMContext):
    data = await state.get_data()
    recs = data.get('recs')
    info = message.text
    await state.finish()
    sql3.execute(f"INSERT INTO pay VALUES(?,?,?)", ('paypal', recs, info))
    db3.commit()
    await message.answer(text='✅PayPal успешно добавлен')

@dp.message_handler(text='💣Удалить счет')
async def dob_schet(message: Message):
    if message.chat.id in admins:
        schet_2 = InlineKeyboardMarkup(row_width=1)
        for i in sql3.execute('SELECT info FROM pay WHERE service = "iban"'):
            schet_2.insert(InlineKeyboardButton(text=f'{i[0]}', callback_data=iban_callback.new(act=f'{i[0]}')))
        await message.answer(text='💬Выберите счет, который нужно удалить', reply_markup=schet_2)
        await Del_schet.Q1.set()

@dp.callback_query_handler(iban_callback.filter(), state=Del_schet.Q1)
async def delete_iban(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    act = callback_data.get('act')
    sql3.execute(f"DELETE FROM pay WHERE info = '{act}'")
    db3.commit()
    await call.message.edit_text(text='🥰Счет успешно удален')

@dp.message_handler(text='💣Удалить PayPal')
async def delet_paypal(message: Message):
    if message.chat.id in admins:
        pay_pal = InlineKeyboardMarkup(row_width=1)
        for i in sql3.execute('SELECT info FROM pay WHERE service = "paypal"'):
            pay_pal.insert(InlineKeyboardButton(text=f'{i[0]}', callback_data=paypal_callback.new(act=f'{i[0]}')))
        await message.answer(text='💬Выберите счет, который нужно удалить', reply_markup=pay_pal)
        await Del_paypal.Q1.set()

@dp.callback_query_handler(paypal_callback.filter(), state=Del_paypal.Q1)
async def delete_iban(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await state.finish()
    act = callback_data.get('act')
    sql3.execute(f"DELETE FROM pay WHERE info = '{act}'")
    db3.commit()
    await call.message.edit_text(text='🥰PayPal успешно удален')
