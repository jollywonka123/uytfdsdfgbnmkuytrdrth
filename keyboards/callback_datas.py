from aiogram.utils.callback_data import CallbackData

ref_callback = CallbackData("ref", "who")
accept_callback = CallbackData("accs", "action", "id")
service_callback = CallbackData("service", 'what')
okey_callback = CallbackData("okey", "act")
paypal_callback = CallbackData("paypal", "act")
iban_callback = CallbackData("iban", "act")
