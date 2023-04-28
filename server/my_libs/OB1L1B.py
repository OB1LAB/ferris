import os
import json
import requests
from datetime import datetime, timedelta
from my_libs.config import Config


# Определение типа лога
def log_type(log, player, date):
    if player.player_name not in log[1]:
        return False
    length = len(log)
    if length == 3:
        action = log[2]
        if action == 'зашёл':
            if not player.online_status:
                player.online_status = True
                player.join_time = to_log_unixtime(f'{date}{log[0]}')
        elif action == 'вышел':
            if player.online_status:
                player.online_status = False
                player.online_time += to_log_unixtime(f'{date}{log[0]}') - player.join_time
                if player.vanish_status:
                    player.vanish_status = False
                    player.vanish_time += to_log_unixtime(f'{date}{log[0]}') - player.vanish_join_time
    elif length > 5 and log[2] == 'issued':
        command = log[5].lower()
        if command in Config.private_chat_commands and length > 7 or command == '/r' and length > 6:
            player.private_msg += 1
        elif command == '/warn' and length > 6:
            player.warns += 1
        elif command in Config.mute_commands and length > 6:
            player.mutes += 1
        elif command == '/kick' and length > 6:
            player.kicks += 1
        elif command in Config.ban_commands and length > 6:
            player.bans += 1
        elif command == '/vanish':
            if not player.vanish_status:
                player.vanish_status = True
                player.vanish_join_time = to_log_unixtime(f'{date}{log[0]}')
            else:
                player.vanish_status = False
                player.vanish_time += to_log_unixtime(f'{date}{log[0]}') - player.vanish_join_time
    elif length > 1:
        if log[1] == '[L]':
            player.local_msg += 1
        elif log[1] == '[G]':
            player.global_msg += 1
    return True


# Для первого лога, чтобы определить статусы онлайна/Ваниша
def log_type_first_date(log, player):
    if player.player_name not in log[1]:
        return
    length = len(log)
    if length == 3:
        action = log[2]
        if action == 'зашёл':
            if not player.online_status:
                player.online_status = True
        elif action == 'вышел':
            if player.online_status:
                player.online_status = False
                if player.vanish_status:
                    player.vanish_status = False



def output_time(time):
    hours = int(time / 3600)
    time = time - hours * 3600
    minutes = int(time / 60)
    seconds = int(time - minutes * 60)
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


# Количество дней между двумя строковами датами
def range_days(date_1, date_2):
    difference_days = (to_datetime(date_2) - to_datetime(date_1)).days
    return range(difference_days + 1)  # +1, т.к range работает до строго меньше указанного числа


# Преобразование строковой даты в datetime
def to_datetime(date: str) -> datetime:  
    return datetime.strptime(date, '%d-%m-%Y')


# Преобразование строковой даты в datetime
def to_log_unixtime(date: str) -> datetime:  
    return datetime.strptime(date, '%d-%m-%Y[%H:%M:%S]').timestamp()


# Возвращает диапазон дат в формате datetime между двумя строками датами
def date_range_str(date_1, date_2):
    dates = []
    for day in range_days(date_1, date_2):
        date_datetime = to_datetime(date_1) + timedelta(days=day)
        date_string = date_datetime.strftime('%d-%m-%Y')
        dates.append(date_string)
    return dates


# Проверка, есть ли лог перед первой датой в логах
def is_before_date(dates, logs_path):
    date = (to_datetime(dates[0]) - timedelta(days=1)).strftime('%d-%m-%Y')
    if f'{date}.txt' in os.listdir(logs_path):
        return date


# Получение младшего мод.состава с сайта Скилла
def get_staff():  
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


# Чтение файла
def read_file(path, encoding=None):
    with open(path, 'r', encoding=encoding) as file:
        return file.read()


# Получение конфига
def get_config():  
    return json.loads(read_file(f'{Config.program_path}/config.json', 'utf-8'))


# Сохранение конфига
def save_config(data):  
    with open(f'{Config.program_path}/config.json', 'w', encoding='utf-8') as file:
        file.write(json.dumps(data))
