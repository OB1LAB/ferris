import os
import json
import ctypes
import requests
from my_libs.config import Config
from datetime import datetime, timedelta


class Player(ctypes.Structure):  # Класс игрока для языка си
    _fields_ = [
        ('local_msg', ctypes.c_int),
        ('global_msg', ctypes.c_int),
        ('private_msg', ctypes.c_int),
        ('warns', ctypes.c_int),
        ('kicks', ctypes.c_int),
        ('mutes', ctypes.c_int),
        ('bans', ctypes.c_int),
        ('online_time', ctypes.c_int),
        ('vanish_time', ctypes.c_int),
        ('join_time', ctypes.c_long),
        ('exit_time', ctypes.c_long),
        ('vanish_join_time', ctypes.c_int),
        ('vanish_exit_time', ctypes.c_int),
        ('nickName', ctypes.POINTER(ctypes.c_char) * 16),
        ('online_status', ctypes.c_bool),
        ('vanish_status', ctypes.c_bool)
    ]


def to_c_array_string(array: list):
    """
        :param array: Питоновский массив
        :return: Массив, который сможет понять язык си
    """
    byte_array = [i.encode() for i in array]
    return (ctypes.c_char_p * (len(byte_array) + 1))(*byte_array)


def output_time(time: int) -> str:
    """
        :param time: Секунды
        :return: Преобразование секунд в строков фремя форматом "Час-минута-секунда"
    """
    hours = int(time / 3600)
    time = time - hours * 3600
    minutes = int(time / 60)
    seconds = time - minutes * 60
    if hours < 10:
        output = f'0{hours}'
    else:
        output = str(hours)
    if minutes < 10:
        output += f':0{minutes}'
    else:
        output += f':{minutes}'
    if seconds < 10:
        output += f':0{seconds}'
    else:
        output += f':{seconds}'
    return output


def range_days(date_1: str, date_2: str) -> range:
    """
        :param date_1: Первая дата в виде строки
        :param date_2: Вторая дата в виде строки
        :return: Количество дней между датами
    """
    difference_days = (to_datetime(date_2) - to_datetime(date_1)).days
    return range(difference_days + 1)  # +1, т.к range работает до строго меньше указанного числа


def to_datetime(date: str) -> datetime:  # Преобразование строковой даты в datetime
    return datetime.strptime(date, '%d-%m-%Y')


def date_range_str(date_1: str, date_2: str) -> list[str]:
    """
        :param date_1: Первая дата в виде строки
        :param date_2: Вторая дата в виде строки
        :return: Массив разницы дат (В виде строк). В формате: день-месяц-Год
    """
    dates = []
    for day in range_days(date_1, date_2):
        date_datetime = to_datetime(date_1) + timedelta(days=day)
        date_string = date_datetime.strftime('%d-%m-%Y')
        dates.append(date_string)
    return dates


def if_before_date(dates: list[str], logs_path: str):
    """
        :param dates: Массив строковых дат
        :param logs_path: Путь до логов
        :return: Проверка на наличие лога днём раннее с последующим его добавлением в массив дат
    """
    date = (to_datetime(dates[0]) - timedelta(days=1)).strftime('%d-%m-%Y')
    if f"{date}.txt" in os.listdir(logs_path):
        dates.insert(0, date)
        return True, dates
    return False, dates


def get_staff() -> dict:  # Получение младшего мод.состава с сайта Скилла
    staff = {}
    for server in Config.server_names_convert:
        staff[Config.server_names_convert[server]] = []
    r = requests.get(Config.staff_url).json()
    for i in r:
        if i['title'] in Config.server_names_convert:
            for j in i['moders']:
                if j['group'] in Config.junior_staff:
                    staff[Config.server_names_convert[i['title']]].append({
                        'Player': j['name'],
                        'Group': j['group']
                    })
    return staff


def read_file(path, encoding=None):
    file = open(path, 'r', encoding=encoding)
    data = file.read()
    file.close()
    return data


def get_config() -> dict:  # Получение конфига
    return json.loads(read_file(r"C:\Users\OB1CHAM\Desktop\OB1LAB\python\ferris\server\config.json", 'utf-8'))


def save_config(data):  # Сохранение конфига
    with open(r"C:\Users\OB1CHAM\Desktop\OB1LAB\python\ferris\server\config.json", 'w', encoding='utf-8') as file:
        file.write(json.dumps(data))
