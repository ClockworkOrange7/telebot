import telebot
from config import TOKEN, available_currency
from extensions import CryptoConverter, APIException

bot = telebot.TeleBot(TOKEN)




@bot.message_handler(commands=['start', 'help'])
def welcome_or_help(message):
    '''Метод приветствия. отрабатывает на команды /start и /help '''
    text = ('Добрый день!\nВас приветствует бот,\
    который расскажет Вам о стоимости той или иной валюты, а для этого необходимо сделать следующее:\nотправить сообщение типа - <имя валюты, цену которой необходимо узнать> <имя валюты,\
    в которой надо узнать цену первой валюты> <количество первой валюты>.\n Увидеть список всех доступных валют: /values')

    bot.send_message(message.chat.id, text)
    pass

@bot.message_handler(commands=['values'])
def currency(message):
    '''Метод показывающий доступные валюты для конвертации по команде /values'''
    text = 'Доступные валюты:'

    bot.send_message(message.chat.id, text +'\n'+'\n'.join(available_currency.keys()))


@bot.message_handler(content_types=['text'])
def req_curr_conv(message):
    '''метод, благодаря которому выводится на экран ответ от бота, будь то конвертация валют или вывод причины ошибки'''
    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise APIException('Неправильное количество параметров')

        qoute, base, amount = [val_.lower() for val_ in values]

        text_ = CryptoConverter.get_price(qoute, base, float(amount))
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message,f'не удалось обработать команду\n{e}')
    else:
        bot.send_message(message.chat.id, f'{qoute} в количестве {amount} = {float(text_['conversion_rate'])*float(amount)} {base}')

bot.polling(non_stop=True)