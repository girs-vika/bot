Алексей Сенокосов, [22.04.2023 04:28]
import telebot
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

bot = telebot.TeleBot(token="5854034045:AAFZiBf_PL1cpWAc728VPG3x0yOsqkFKfuc")
# словарь для хранения логинов пользователей
# logins = {"Alex","111"}
logins = {}
sklad = {"шоколад":  "2000",
         "мармелад" :"2000",
         "зефир":"2000"}
logistik= {"Прибыло на склад": ["шоколад","22.04.2023","СОАО Коммунарка,г. Минск, 220033, ул. Аранская, 18",'Global',1000],
         "Убыло со склада" :["зефир","22.04.2023","Global","220026, г. Минск, пер.Бехтерева, д.8, ком.315",1000],
         "зефир":"2000"}
@bot.message_handler(commands=['start'])
def handle_start(message):
    button = InlineKeyboardButton(text='Вход', callback_data='enter')
    keyboard = InlineKeyboardMarkup().add(button)
    bot.send_message(chat_id=message.chat.id, text='Нажмите на кнопку, чтобы войти:', reply_markup=keyboard)
@bot.callback_query_handler(func=lambda call: True)
def handle_button_press(call):
    if call.data == 'enter':
        # заменяем сообщение с кнопкой на сообщение с новой кнопкой
        login_button = InlineKeyboardButton(text='Введи login', callback_data='login')
        keyboard = InlineKeyboardMarkup().add(login_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите логин:',
                              reply_markup=keyboard)
    elif call.data == 'password':
        password_button = InlineKeyboardButton(text='Введи password', callback_data='password')
        keyboard = InlineKeyboardMarkup().add(password_button)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Введите password:',
                              reply_markup=keyboard)
    elif call.data == 'warehouse':
        text = "Данные на складе:\n"
        for product, quantity in sklad.items():
            text += f"{product}: {quantity}\n"
        bot.send_message(chat_id=call.message.chat.id, text=text)
    elif call.data == 'logistics':
        button1 = InlineKeyboardButton(text='Прибыло на склад', callback_data='arrival')
        button2 = InlineKeyboardButton(text='Убыло со склада', callback_data='departure')
        button3 = InlineKeyboardButton(text='Данные на складе', callback_data='warehouse')
        keyboard = InlineKeyboardMarkup().add(button1, button2,button3)
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text='Выберите действие:',
                              reply_markup=keyboard)
    elif call.data == 'arrival':
        text = f"{logistik['Прибыло на склад'][0]} прибыло на склад {logistik['Прибыло на склад'][2]} от {logistik['Прибыло на склад'][3]}. Количество: {logistik['Прибыло на склад'][4]}"
        bot.send_message(chat_id=call.message.chat.id, text=text)
    elif call.data == 'departure':
        text = f"{logistik['Убыло со склада'][0]} убыло со склада {logistik['Убыло со склада'][3]} в {logistik['Убыло со склада'][2]}. Количество: {logistik['Убыло со склада'][4]}"
        bot.send_message(chat_id=call.message.chat.id, text=text)

Алексей Сенокосов, [22.04.2023 04:28]
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    if chat_id in logins:
        # сохраняем пароль и отправляем сообщение об успешном входе
        password = message.text
        login = logins[chat_id]
        del logins[chat_id]
        success_message = f'Вы вошли в систему!\nЛогин: {login}\nПароль: {password}'
        # удаляем сообщение пользователя
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton("склад", callback_data="warehouse"),
                   InlineKeyboardButton("логистика", callback_data="logistics"))
        bot.send_message(chat_id=chat_id, text=success_message, reply_markup=markup)
        # удаляем сообщение пользователя
    else:
        # сохраняем логин и запрашиваем пароль
        logins[chat_id] = message.text
        password_button = InlineKeyboardButton(text='Введи password', callback_data='password')
        keyboard = InlineKeyboardMarkup().add(password_button)
        bot.send_message(chat_id=chat_id, text='Введите пароль:', reply_markup=keyboard)
        # удаляем сообщение пользователя
        bot.delete_message(chat_id=chat_id, message_id=message.message_id)

bot.polling()