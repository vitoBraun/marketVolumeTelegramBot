from threading import Thread
from iofuncs import *
from chart import chart_gen


def sm(ms, text, nomarkup=False):
    if nomarkup == True:
        bot.send_message(ms.chat.id, text)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mrk = types.InlineKeyboardButton(text="check")
        markup.add(mrk)
        bot.send_message(ms.chat.id, text, reply_markup=markup)


class ChatbotClass(Thread):
    def __init__(self):
        Thread.__init__(self)

        @bot.message_handler(content_types=['text'])
        def start(message):
            username = message.chat.username

            if message.chat.username == None:
                sm(message, 'У вас нет имени пользователя Telegram, добавьте его в настройках', nomarkup=True)
            else:
                if check_user_exist(username) == False:
                    if message.text == 'ABC':
                        save_user([message.chat.id, message.chat.username])
                        sm(message, 'Добро пожаловать!')
                    else:
                        sm(message, '!%under maintainance', nomarkup=True)
                else:
                    if message.text == '/start':
                        try:
                            sm(message, 'Мистер Робот активирован и пристально наблюдает за рынком 👀. Ждем новостей... 💫 ')
                        except:
                            pass
                    if message.text == 'check':
                        data = read_data()
                        string = ''
                        for i in data:
                            string += str(i[0]) + ': ' + str(i[1]) + '\n'
                        img = open('chart.png', 'rb')
                        bot.send_photo(message.chat.id, img, caption=string)
                    if message.text == 'stop':
                        del_user(message.chat.username)
                        sm(message, 'Вы удалены', nomarkup=True)
                    if message.text[0] == '_' and username == admin:
                        command = message.text.replace('_', '')
                        command = command.split(' ')
                        if len(command) == 3:
                            settings[command[0]] = str(
                                command[1] + ' ' + command[2])
                        else:
                            settings[command[0]] = command[1]
                        save_settings(settings)
                        sm(message, str(dict(
                            config_object['settings'])))
                    if message.text == 'settings' and username == admin:
                        sm(message, str(dict(
                            config_object['settings'])))
                    if message.text == 'users' and username == admin:
                        data = read_users()
                        string = ''
                        for i in data:
                            string += str(i[0]) + ' ' + str(i[1]) + '\n'
                        sm(message, string)
                    if message.text.split()[0] == 'delete' and username == admin:
                        del_user(message.text.split()[1])
                        sm(message, 'User ' +
                           message.text.split()[1] + ' удален')
                    if message.text == 'chart':
                        chart_gen()
                        sm(message, 'Чарт обновлен')

                    if message.text == 'commands' and username == admin:
                        commands = '''
                        Комманды: 
                        users - Список пользователей
                        settings - Текущие настройки
                        chart - Обновить картинку с графиком
                        delete <username> - Удалить юзера
                        stop - Удалить самого себя из списка пользователей бота
                        _period [n] [minutes/hours/days] - установить период на график
                        _candle [n]HOUR/MINUTE - установить длинну свечки
                        msg <чат id> <сообщение> - отправить сообщение пользователю от имени бота'''

                        sm(message, commands)
                    if message.text.split()[0] == 'msg' and username == admin:
                        try:
                            bot.send_message(message.text.split()[
                                             1], message.text.split()[2])
                        except:
                            sm(message,
                               'Некорректная команда. должно быть: <чат id> <сообщение>')
            print('...ChatBot...')
