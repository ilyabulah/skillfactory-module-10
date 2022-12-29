import telebot
from config import TOKEN, keys
from extensions import APIException, СurrencyConverter

bot = telebot.TeleBot(TOKEN)

# Обрабатываются все сообщения содержащие команды '/start' or '/help'.
@bot.message_handler(commands=['start', 'help'])
def handle_start_help(message: telebot.types.Message):
    text = '''
    Чтобы начать работу введите команду боту в следующем формате:\n
<имя валюты> <в какую валюту перевести> <количество переводимой валюты>\n
Чтобы увидеть список всех доступных валют введите команду: /values'''
    bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def handle_values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
    try:
        values = message.text.lower().split(' ')

        if len(values) != 3:
            raise APIException('Слишком много параметров')

        quote, base, amount = values
        total_base = СurrencyConverter.get_price(quote, base,amount)

    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')

    else:
        response_text = f'Цена {amount}  {quote} в {base} = {total_base} {keys[base]}'
        bot.send_message(message.chat.id, response_text)


bot.polling(none_stop=True) #бот должен стараться не прекращать работу при возникновении каких-либо ошибок