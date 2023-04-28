from my_libs.OB1L1B import output_time, date_range_str, is_before_date, log_type, get_config


# Класс игрока
class Player:
    def __init__(self, player_name):
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
    
    def get_result(self, count_days):
        avg_online_time, total_online_time = output_time(self.online_time/count_days), output_time(self.online_time)
        avg_vanish_time, total_vanish_time = output_time(self.vanish_time/count_days), output_time(self.vanish_time)
        return {
            'Player': self.player_name,
            'local_msg': self.local_msg,
            'global_msg': self.global_msg,
            'private_msg': self.private_msg,
            'warns': self.warns,
            'kicks': self.kicks,
            'mutes': self.mutes,
            'bans': self.bans,
            'AVG': f'{avg_online_time}<br/>{avg_vanish_time}',
            'Total': f'{total_online_time}<br/>{total_vanish_time}'
        }
        


# Получение игровой активности
def get_activity(first_date, second_date, players):
    activity = {}
    first_date, second_date = '01-03-2023', '07-03-2023'
    for player in players:
        activity[player] = Player(player)
    logs_path = get_config()['logs_path']
    days = date_range_str(first_date, second_date)
    count_days = len(days)
    date = is_before_date(days, logs_path)
    if date:
        with open(f'{logs_path}/{date}.txt') as file:
                for line in file:
                    for player in players:
                        if player in line and log_type(line.split(), activity[player], date):
                            break
    for date in days:
        with open(f'{logs_path}/{date}.txt') as file:
            for line in file:
                for player in players:
                    if player in line and log_type(line.split(), activity[player], date):
                        break
    return [activity[player].get_result(count_days) for player in players]
