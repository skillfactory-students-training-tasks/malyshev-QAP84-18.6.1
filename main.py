import telebot
from config import TOKEN, keys
from extensions import api, ConvertException

bot = telebot.TeleBot(TOKEN)



@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, ("Привет, я помогу тебе узнать курс валюты. \n Пиши /help и я расскажу как я устроен"))


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, ("Я могу конвертировать одну валюту в другую, команда /values покажет тебе их список.\n\n"
                                       "Отправь мне сообщение в виде: <имя валюты цену которой хочешь узнать> <имя валюты в которой надо узнать цену первой валюты> <количество первой валюты> и я подскажу тебе значение. "))





@bot.message_handler(commands=['values'])
def values(message):
    r = api.get_values()
    for i in r.keys():
        bot.send_message(message.chat.id, str(i))

@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        message.text = message.text.lower()
        message.text = message.text.replace(',', '.')
        values = message.text.split(' ')
        quote, base, amount = values
        if len(values) > 3:
            raise ConvertException('Неправильный ввод данных')
        if len(values) < 3:
            raise ConvertException('Неправильный ввод данных')

        if float(amount) < 0:
            raise ConvertException('Количество не может быть отрицательным!')
        try:
            quote in keys[quote]
        except KeyError:
            raise ConvertException(f'Я не знаю валюту {quote}')
        try:
            base in keys[base]
        except KeyError:
            raise ConvertException(f'Я не знаю валюту {base}')

        if quote == base:
            raise ConvertException(f'{quote} в {base} это и есть {quote}')

    except ConvertException as e:
        bot.reply_to(message, f'Ошибка: {e}')
    except ValueError:
        bot.reply_to(message, f'Неправильный ввод данных')

    else:
        text = api.get_price(base, quote, amount)
        bot.send_message(message.chat.id, text)









bot.polling(none_stop=True)
