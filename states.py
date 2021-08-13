from aiogram.dispatcher.filters.state import StatesGroup, State


class Join_team(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()
    Q5 = State()

class Make_r(StatesGroup):
    Q1 = State()

class New_payment(StatesGroup):
    Q1 = State()
    Q2 = State()
    Q3 = State()
    Q4 = State()

class Increase(StatesGroup):
    Q1 = State()
    Q2 = State()

class Paint(StatesGroup):
    Q1 = State()
    Q2 = State()

class Dob_schet(StatesGroup):
    Q1 = State()
    Q2 = State()

class Dob_paypal(StatesGroup):
    Q1 = State()
    Q2 = State()

class Del_schet(StatesGroup):
    Q1 = State()

class Del_paypal(StatesGroup):
    Q1 = State()