from peewee import Model, CharField, IntegerField, SqliteDatabase
from telebot.types import Message



database_object = SqliteDatabase('history.db')

class History(Model):
    history = CharField()
    user_id_history = IntegerField(unique=True)

    class Meta:
        database = database_object


def history_bot_func(message: Message,  action: str):
    """
    Функция, Обновляющая и выводящая историю запросов пользователя
    :param message: экземпляр беседы
    :param action: какая именно функция была задействована (это необходимо для обновления истории)
    :return: Обновлённая история запросов пользователя
    """
    user_id = message.from_user.id


    if database_object.is_closed():
        database_object.connect()
    database_object.create_tables([History])


    user, user_in_system = History.get_or_create(user_id_history=user_id, defaults={'history': 'У вас появилась история запросов;\n'})

    if action == 'start':
        user.history = user.history + 'Вы зашли в бота;\n'
        user.save()

    if action == 'help_bot':
        user.history = user.history + 'Вы запросили перечень функций;\n'
        user.save()

    if action == 'history':
        user.history = user.history + 'Вы запросили историю ваших запросов;\n'
        user.save()

    if action == 'rubles_to_dollars':
        user.history = user.history + 'Вы конвертировали рубли в доллары;\n'
        user.save()

    if action == 'dollars_to_rubles':
        user.history = user.history + 'Вы конвертировали доллары в рубли;\n'
        user.save()

    if action == 'unintelligible text':
        user.history = user.history + 'Вы ввели сообщение вместо команды;\n'
        user.save()

    if action == 'city':
        user.history = user.history + 'Вы узнали свой город;\n'
        user.save()

    return user.history



