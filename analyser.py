from iofuncs import *
from threading import Thread
import time
from chart import chart_gen


class Analyser(Thread):
    def __init__(self):
        Thread.__init__(self)
        self.run()

    def run(self):
        while True:
            old_data = read_data()
            stockdata = get_stockdata()
            self.stockdata = stockdata
            l = int(len(stockdata)-1)
            self.l = l
            h = self.highest_change(5, 'raise')
            f = self.highest_change(5, 'fall')
            vol_raise = self.compare(h, h-1, 5)
            data = [
                ['Время', self.time_fmt(stockdata[h][0])],
                ['Разница объема (%)',
                 vol_raise],
                # ['Количество валюты', float(stockdata[h][5]) -
                #  float(stockdata[h-1][5])],
                # ['Объем до', stockdata[h-1][5]],
                # ['Объем после', stockdata[h][5]],
                # ['Разница объемов торогов на текущий момент (%)', self.compare(
                #  l, l-1, 5)],
                # ['Объем сейчас', stockdata[l][5]],
                # ['Объем на прошлой свечи', stockdata[l-1][5]],
                ['Разница цены (%)', self.compare(
                 l, l-1, 4)],
                ['Последняя цена', stockdata[l][4]],
                # ['Highest volume fall %', self.compare(f, f-1, 5)],
                # ['Amount fallen', float(stockdata[f][5]) +
                #  float(stockdata[f-1][5])],
                # ['Time_f', self.time_fmt(stockdata[f][0])],
                # ['F_Volume_a', stockdata[f-1][5]],
                # ['F_Volume_b', stockdata[f][5]],
                # ['Количество сделок на текущую свечу', stockdata[l-1][8]],
                ['Свеча', settings['candle']],
                ['Период', settings['period']]
            ]
            save_data(data)

            if old_data[0][1] != data[0][1]:
                if vol_raise > 500:
                    self.trade_signal()
            print('...Analyser...')
            time.sleep(5)

    def time_fmt(self, timestamp):
        for i in range(len(self.stockdata)):
            time = str(timestamp)[:-3]
            date_time = datetime.fromtimestamp(int(time))
            return str(date_time)

    def compare(self, a, b, key):
        avl = float(self.stockdata[a][key])
        bvl = float(self.stockdata[b][key])
        pdif = ((avl / bvl) * 100) - 100
        return round(pdif, 2)

    def highest_change(self, key, course='raise', period='1MINUTE'):
        d = []
        l = self.l
        for i in range(1, l):
            if course == 'raise':
                comp = self.compare(i, i-1, key)
                if float(comp) > 0:
                    d.append([i, comp])
            if course == 'fall':
                comp = self.compare(i, i-1, key)
                if float(comp) < 0:
                    d.append([i, comp])
        n = 0
        nind = 0
        if course == 'raise':
            for i in range(len(d)):
                if float(d[i][1]) > n:
                    n = d[i][1]
                    nind = d[i][0]
        if course == 'fall':
            for i in range(len(d)):
                if float(d[i][1]) < n:
                    n = d[i][1]
                    nind = d[i][0]
        return nind

    def trade_signal(self):
        print('Trade signal start')
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        mrk = types.InlineKeyboardButton(text="check")
        markup.add(mrk)
        data = read_data()
        rd = read_users()
        # img = open('chart.png', 'rb')
        string = data[0][1] + ' МСК \n' + 'Обнаружен повышенный объем! \n'
        string += 'Краткосрочный рост объема составил ' + \
            data[1][1] + ' % \n Отправьте check для подробностей'
        for i in range(len(rd)):
            bot.send_message(rd[i][0], string, reply_markup=markup)
            # bot.send_photo(rd[i][0], img, caption=string,
            #                reply_markup=markup)
            print('Signal sent')

# if __name__ == '__main__':
    # rd = read_users()
    # img = open('chart.jpg', 'rb')
    # for i in range(len(rd)):
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     mrk = types.InlineKeyboardButton(text="Check")
    #     markup.add(mrk)

    #     # bot.send_photo(523359893, img, caption='sdsd', reply_markup=markup)
    #     bot.send_photo(rd[i][0], img, caption='test',
    #                    reply_markup=markup)

    # markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    # mrk = types.InlineKeyboardButton(text="Check")
    # markup.add(mrk)
    # data = read_data()
    # rd = read_users()
    # img = open('chart.jpg', 'rb')
    # string = data[0][1] + ' МСК \n' + 'Обнаружен повышенный объем! \n'
    # string += 'Краткосрочный рост объема составил ' + \
    #     data[1][1] + ' % \n'
    # for i in range(len(rd)):
    #     try:
    #         bot.send_photo(rd[i][0], img, caption=string,
    #                        reply_markup=markup)
    #         print('Signal sent')
    #     except:
    #         print('Trouble in sending to ' + str(rd[i][0]))
