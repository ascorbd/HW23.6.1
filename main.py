import telebot
from config import keys, TOKEN
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help_message(message: telebot.types.Message):
    text = ('Чтобы начать работу, введите команду в следующем формате: \n <имя валюты> \n <в какую валюту перевести> \n <количество переводимой валюты>')
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты: '
    for key in keys.keys():
        text = '\n'.join((text, key, ))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split()
        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {quote} в {base} =  {total_base} {base}'
        bot.send_message(message.chat.id, text)


bot.polling()