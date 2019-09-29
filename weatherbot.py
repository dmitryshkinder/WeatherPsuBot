import config
import telebot
import time

from pyowm import OWM
from pyowm.exceptions import api_response_error

API_key = 'b91aa6d9ecf6f03d71a3116551fff5fd'
owm = OWM(API_key, language = 'ru')

bot = telebot.TeleBot(config.telebot_token)

question_msg = 'Привет, друг!\n' + 'В каком городе ты живёшь?'

@bot.message_handler(commands=['start', 'weather'])
def send_welcome(message):
      bot.send_message(message.chat.id, question_msg)

@bot.message_handler(content_types = ['text'])
def send_echo(message):

    try: 
        observation = owm.weather_at_place(message.text)
        w = observation.get_weather()
        temp = w.get_temperature('celsius')['temp']

        answer = 'В городе ' + message.text + ' сейчас ' + w.get_detailed_status() + '\n' 
        answer += 'Температура сейчас в районе ' + str(temp)

        bot.send_message(message.chat.id, answer)
    except api_response_error.NotFoundError:
        bot.send_message(message.chat.id, "Такого города не существует")
        time.sleep(10)


bot.polling(none_stop=True)

