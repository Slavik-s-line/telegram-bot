import telebot
from telebot import types
import requests
from bs4 import BeautifulSoup as BS

bot = telebot.TeleBot('1653644021:AAEuuD2PtYXo1YwTVDDgrOotXWE2lDQMxn4')

@bot.message_handler(commands=['start'])
def welcome(message):

    # keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Цитатка")
    item2 = types.KeyboardButton("Поговори со мной")
    item3 = types.KeyboardButton("Погода в Киеве")
    markup.add(item1, item2, item3)

    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!".format(
                         message.from_user, bot.get_me()),
                     parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def lalala(message):
    if message.chat.type == 'private':
        if message.text == "Цитатка":
            bot.send_message(message.chat.id,
                             "Никто не может грустить, когда у него есть воздушный шарик!\n"".\n"
                                              "Алан Александр Милн")
        elif message.text == 'Поговори со мной':

            markup = types.InlineKeyboardMarkup(row_width=2)
            item1 = types.InlineKeyboardButton("Хорошо", callback_data='good')
            item2 = types.InlineKeyboardButton("Не очень", callback_data='bad')

            markup.add(item1, item2)

            bot.send_message(message.chat.id, 'Как ты, бродяга?', reply_markup=markup)

        elif message.text == 'Погода в Киеве':
            r = requests.get('https://sinoptik.ua/погода-киев')
            html = BS(r.content, 'html.parser')
            for el in html.select('#content'):
                t_min = el.select('.temperature .min')[0].text
                t_max = el.select('.temperature .max')[0].text
                text = el.select('.wDescription .description')[0].text
            bot.send_message(message.chat.id, "Привет, погода на сегодня:\n" +
                             t_min + ', ' + t_max + '\n' + text)
        else:
            bot.send_message(message.chat.id, 'Я не знаю что ответить 😢')


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        if call.message:
            if call.data == 'good':
                bot.send_message(call.message.chat.id, 'Вот и отличненько 😊')
            elif call.data == 'bad':
                bot.send_message(call.message.chat.id, 'Бывает 😢')

            # show alert
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False,
                                      text="ЭТО ТЕСТОВОЕ УВЕДОМЛЕНИЕ!!11")

    except Exception as e:
        print(repr(e))


# RUN
bot.polling(none_stop=True)
