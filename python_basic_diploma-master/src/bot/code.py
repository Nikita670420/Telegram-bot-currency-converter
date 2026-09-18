import telebot
import os


from src.bot.commands.help import help_bot
from src.bot.commands.dollar_exchange_rate import dollar_exchange_rate
from src.bot.commands.history import history_bot_func
from src.bot.commands.city_by_ip import city_by_ip


from telebot.types import Message
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(token)
waiting_for_rubles = {}
number = {}

@bot.message_handler(commands=['start'])
def start_bot(message: Message) -> int:
    """
    Это функция, которая приветствует пользователя при запуске программы.
    Так же эта функция позволяет пользователю узнать набор команд для работы, для этого она вызывает функцию help.
    :param message: Объект сообщения, которое принимает функция start_bot (то есть это сообщение пользователя)
    """
    bot.reply_to(message, 'Здравствуйте! Это конвертор валют.')
    user_id = message.chat.id
    number[user_id] = 0
    help_bot(message, bot)
    history_bot_func(message, 'start')
    return user_id


global_user_id = start_bot


@bot.message_handler(commands=['help'])
def func_help_bot(message: Message) -> None:
    """
    Это функция, которая возвращает список команд.
    :param message: Объект сообщения, которое принимает функция start_bot (то есть это сообщение пользователя)
    """
    help_bot(message, bot)
    history_bot_func(message, 'help_bot')


@bot.message_handler(commands=['history'])
def func_history_bot(message: Message) -> None:
    """
    Выводит историю запросов пользователя.
    :param message: Объект сообщения, которое принимает функция (то есть это сообщение пользователя)
    """
    history = history_bot_func(message, 'history')
    bot.reply_to(message, f'Вот история ваших запросов:\n---------------------------\n{history}')


@bot.message_handler(commands=['rubles_to_dollars'])
def converting_rubles_to_dollars(message: Message) -> None:
    """
    Функция запускающая конвертацию рублей в доллары.
    1) функция запрашивает число у пользователя (сколько рублей пользователь хочет конвертировать)
    2) функция вызывает функцию, которая используя пользовательское сообщение с числом, конвертирует рубли в доллары.
    :param message: Сообщение пользователя (объект сообщения)
    """
    number[global_user_id] = 1
    chat_id = message.chat.id
    waiting_for_rubles[chat_id] = True  # Ждём число
    bot.reply_to(message, 'Напишите, сколько рублей вы хотите перевести в доллары.')
    history_bot_func(message, 'rubles_to_dollars')


@bot.message_handler(func=lambda message: waiting_for_rubles.get(message.chat.id, False) and number[global_user_id] == 1)
def calculator(message: Message) -> None:
    """
    Функция конвертирует число из сообщения пользователя в доллары по актуальному курсу.
    Актуальность курса гарантируется постоянными запросами API Центрального Банка Российской Федерации при активации функции.
    :param message: Сообщение пользователя (объект сообщения)
    """
    try:
        chat_id = message.chat.id
        rub = float(message.text.replace(',', '.'))
        rate = dollar_exchange_rate()
        result = round(rub / rate, 2)
        bot.reply_to(message, f'На эти деньги можно купить {result} долларов')
        waiting_for_rubles[chat_id] = False
    except ValueError:
        bot.reply_to(message, 'Введите число!')
    except ZeroDivisionError:
        bot.reply_to(message, f'Извините, произошла ошибка, сервер не отвечает. \n Попробуйте ещё раз.')



@bot.message_handler(commands=['dollars_to_rubles'])
def converting_dollars_to_rubles(message: Message) -> None:
    """
    Функция запускает конвертирование.
    1) запрашивает число у пользователя
    2) активирует функцию которая используя сообщение пользователя конвертирует доллары в рубли
    :param message: Пользовательское сообщение (объект сообщения)
    """
    number[global_user_id] = 2
    chat_id = message.chat.id
    waiting_for_rubles[chat_id] = True  # вновь ждём число
    bot.reply_to(message, 'Напишите, сколько долларов вы хотите перевести в рубли.')
    history_bot_func(message, 'dollars_to_rubles')


@bot.message_handler(func=lambda message: waiting_for_rubles.get(message.chat.id, False) and number[global_user_id] == 2)
def calculater_2(message) -> None:
    """
    Функция конвертирует число из сообщения пользователя в рубли по актуальному курсу.
    Актуальность курса гарантируется постоянными запросами API Центрального Банка Российской Федерации при активации функции.
    :param message: Сообщение пользователя (объект сообщения)
    """
    try:
        chat_id = message.chat.id
        rub = float(message.text.replace(',', '.'))
        rate = dollar_exchange_rate()
        result = round(rub * rate, 2)
        bot.reply_to(message, f'На эти деньги можно купить {result} рублей')
        waiting_for_rubles[chat_id] = False
    except ValueError:
        bot.reply_to(message, 'Введите число!')
    except ZeroDivisionError:
        bot.reply_to(message, f'Извините, произошла ошибка, сервер не отвечает. \n Попробуйте ещё раз.')




@bot.message_handler(commands=['my_city'])
def my_city(message: Message) -> None:
    """
    Это функция, что выводит пользователю его город (город из которого идёт запрос)
    :param message: объект сообщения (сообщение пользователя)
    """
    city = city_by_ip()
    bot.reply_to(message, f'Запрос исходит из города {city}')
    history_bot_func(message, 'city')


@bot.message_handler(func=lambda message: message.text not in ['/start', '/help', '/history', '/rubles_to_dollars', '/dollars_to_rubles'])
def processing_non_commands(message: Message) -> None:
    """
    Функция отвечает на все остальные сообщения пользователя (которые не являются командами)
    :param message: Сообщение пользователя (объект сообщения)
    """
    bot.reply_to(message, f'Извините, но я общаюсь командами. \nВыберите одну из доступных команд.')
    help_bot(message, bot)
    history_bot_func(message, 'unintelligible text')


def run_bot() -> None:
    """
    Эта функция необходима для перевода кода в файл main.py.
    В этой функции будет несколько функция (функция run_bot - это функция в которой функции).
    Каждая из этих функций будет отвечать за свою часть программы.
    """

    bot.infinity_polling()  # Это запуск всех модулей.