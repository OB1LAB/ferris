import os
import sys
import requests
import subprocess
from app import socketio
from flask_restful import Resource, reqparse
from my_libs.config import Config
from my_libs.OB1L1B import date_range_str
from datetime import datetime
from threading import Thread


def download_logs(server, date, logs_path):
    logs_content = requests.get(
        f'https://ob1lab.ru/api/logs?server={server}&date={date}').text
    with open(f'{logs_path}/{date}.txt', 'w', encoding='utf-8') as file:
        file.write(logs_content)


def dates_sort(dates):
    dates = [datetime.strptime(date, '%d-%m-%Y.txt') for date in dates]
    dates.sort()
    return [date.strftime('%d-%m-%Y') for date in dates]


class LogsApi(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('server', type=str, location='args')

    def get(self):
        info = requests.get(
            'https://ob1lab.ru/api/info').json()['local_servers_dates']
        server = self.reqparse.parse_args()['server']
        logs_path = f'{Config.logs_path}/{server}/chat_public'
        local_dates = dates_sort(os.listdir(logs_path))
        server_dates = date_range_str(
            info[server]['first'], info[server]['last'])
        threads_download, complete_download = [], []
        if local_dates:
            threads_download.append(
                Thread(target=download_logs, args=(server, local_dates[-1], logs_path)))
            threads_download[-1].start()
        for date in server_dates:
            if date not in local_dates:
                threads_download.append(
                    Thread(target=download_logs, args=(server, date, logs_path)))
                threads_download[-1].start()
        percent = 0
        while percent < 100:
            for thread_download in threads_download:
                if not thread_download.is_alive() and thread_download.getName() not in complete_download:
                    complete_download.append(thread_download.getName())
                    percent = int(
                        (len(complete_download)/len(threads_download))*100)
                    socketio.emit('percent', percent)
                    if percent == 100:
                        break
        return ''

    def post(self):
        directory_path = Config.logs_path
        if sys.platform == 'win32':
            subprocess.Popen(['start', directory_path], shell=True)
        elif sys.platform == 'darwin':
            subprocess.Popen(['open', directory_path])
        else:
            try:
                subprocess.Popen(['xdg-open', directory_path])
            except OSError:
                print('Не удалось открыть директорию.')
        return ''
