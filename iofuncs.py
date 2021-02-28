import pandas as pd
from datetime import datetime
from binance.client import Client
from configparser import ConfigParser
import requests
import urllib3
import telebot
from telebot import types
urllib3.disable_warnings()


config_object = ConfigParser()
config_object.read("config.ini")

keys = config_object["KEYS"]
settings = config_object["settings"]
symbol = settings['symbol']

global bot
bot = telebot.TeleBot(keys['TOKEN'])

admin = settings['admin']

client = Client(keys['apis'][0], keys['apis'][1],
                {"verify": False, "timeout": 20})


def save_settings(newset):
    settings = newset
    with open('config.ini', 'w') as conf:
        config_object.write(conf)


with open('config.ini', 'w') as conf:
    config_object.write(conf)


def read_data():
    data = []
    reader = pd.read_csv('data.csv', names=["param", "val"])
    res = reader.param.to_list()
    res2 = reader.val.to_list()
    for i in range(len(res)):
        data.append([res[i], res2[i]])
    return data


def save_data(data):
    df = pd.DataFrame(data)
    df.to_csv('data.csv', header=None, index=False)


def read_users():
    data = []
    reader = pd.read_csv('users.csv', names=["chat_id", "username"])
    res = reader.chat_id.to_list()
    res2 = reader.username.to_list()
    for i in range(len(res)):
        data.append([res[i], res2[i]])
    return data


def check_user_exist(username):
    rd = read_users()
    exist = False
    for i in range(len(rd)):
        if username in rd[i]:
            exist = True
    return exist


def save_user(username):
    if check_user_exist(username) == False:
        rd = read_users()
        rd.append(username)
        df = pd.DataFrame(rd)
        df.to_csv('users.csv', header=None, index=False)


def del_user(username):
    rd = read_users()
    for i in rd:
        if i[1] == username:
            rd.remove(i)
            break
    df = pd.DataFrame(rd)
    df.to_csv('users.csv', header=None, index=False)


def get_stockdata():
    try:
        if settings['candle'] == '1MINUTE':
            kline = Client.KLINE_INTERVAL_1MINUTE
        if settings['candle'] == '5MINUTE':
            kline = Client.KLINE_INTERVAL_5MINUTE
        if settings['candle'] == '15MINUTE':
            kline = Client.KLINE_INTERVAL_15MINUTE
        if settings['candle'] == '1HOUR':
            kline = Client.KLINE_INTERVAL_1HOUR
        data = client.get_historical_klines(
            symbol, kline,  settings['period'] + " ago UTC")
        df = pd.DataFrame(data)
        df.to_csv('stockdata.csv', header=None, index=False)
        return data
    except:
        print('Binance connection damage')
