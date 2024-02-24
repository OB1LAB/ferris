import os
from app import socketio
from my_libs.OB1L1B import output_time, date_range_str, is_before_date, \
    log_activity, to_log_unixtime, log_type_first_date
from my_libs.config import Config


# Класс игрока
class Player:
    def __init__(self, player_name, group):
        self.player_name = player_name
        self.local_msg = 0
        self.global_msg = 0
        self.private_msg = 0
        self.warns = 0
        self.kicks = 0
        self.mutes = 0
        self.bans = 0
        self.online_time = 0
        self.vanish_time = 0
        self.join_time = None
        self.vanish_join_time = None
        self.online_status = False
        self.vanish_status = False
        self.group = group

    def get_result(self, count_days):
        avg_online_time, total_online_time = output_time(self.online_time / count_days), output_time(self.online_time)
        avg_vanish_time, total_vanish_time = output_time(self.vanish_time / count_days), output_time(self.vanish_time)
        avg_online_without_vanish_time, total_online_without_vanish_time = output_time(
            (self.online_time / count_days) - self.vanish_time / count_days
        ), output_time(self.online_time - self.vanish_time)
        return {
            'Player': self.player_name,
            'local_msg': self.local_msg,
            'global_msg': self.global_msg,
            'private_msg': self.private_msg,
            'warns': self.warns,
            'kicks': self.kicks,
            'mutes': self.mutes,
            'bans': self.bans,
            'AVG': f'{avg_online_time}',
            'AVG_vanish': avg_vanish_time,
            'Total': f'{total_online_time}',
            'Total_vanish': total_vanish_time,
            'AVG_without_vanish': avg_online_without_vanish_time,
            'Total_without_vanish': total_online_without_vanish_time,
            'Group': self.group
        }


# Получение игровой активности
def get_activity(first_date, second_date, players_data, server):
    activity, players, last_line = {}, [], ''
    for player in players_data:
        activity[player['Player']] = Player(player['Player'], player['Group'])
        players.append(player['Player'])
    logs_path = f'{Config.logs_path}/{server}/chat_public'
    local_logs = os.listdir(logs_path)
    days = date_range_str(first_date, second_date)
    count_days = len(days)
    date = is_before_date(days, logs_path)
    not_found_logs = []
    if date:
        if f'{date}.txt' not in local_logs:
            not_found_logs.append(date)
        else:
            with open(f'{logs_path}/{date}.txt', encoding='utf-8') as file:
                for line in file:
                    for player in players:
                        if (player in line or 'Сервер' in line) and log_type_first_date(line.split(), activity[player]):
                            break
        for player in players:
            if activity[player].online_status:
                activity[player].join_time = to_log_unixtime(f'{days[0]}{"[00:00:00]"}')
            if activity[player].vanish_status:
                activity[player].vanish_join_time = to_log_unixtime(f'{days[0]}{"[00:00:00]"}')
    for date in days:
        if f'{date}.txt' not in local_logs:
            not_found_logs.append(date)
            continue
        if date == days[-1]:
            with open(f'{logs_path}/{date}.txt', encoding='utf-8') as file:
                for line in file:
                    for player in players:
                        if (player in line or 'Сервер' in line) and log_activity(line.split(), activity[player], date):
                            break
                    last_line = line
        else:
            with open(f'{logs_path}/{date}.txt', encoding='utf-8') as file:
                for line in file:
                    for player in players:
                        if (player in line or 'Сервер' in line) and log_activity(line.split(), activity[player], date):
                            break
    if not_found_logs:
        socketio.emit('error', f'Не найдены логи с {not_found_logs[0]} по {not_found_logs[-1]}')
    for player in players:
        if activity[player].online_status:
            activity[player].online_time += to_log_unixtime(f'{days[-1]}{last_line.split()[0]}') - activity[player].join_time
        if activity[player].vanish_status:
            activity[player].vanish_time += to_log_unixtime(f'{days[-1]}{last_line.split()[0]}') - activity[player].vanish_join_time
    return [activity[player].get_result(count_days) for player in players]
