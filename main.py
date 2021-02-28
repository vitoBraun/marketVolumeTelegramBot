
from threading import Thread
from iofuncs import *
from chatbot import ChatbotClass
from analyser import Analyser
from chart import *


def main():

    anl = Analyser
    thread1 = Thread(target=anl)
    thread1.start()

    Chatbot = ChatbotClass
    thread2 = Thread(target=Chatbot)
    thread2.start()

    chart_refresh = Chart
    thread3 = Thread(target=chart_refresh)
    thread3.start()


if __name__ == '__main__':
    main()
    bot.polling()
