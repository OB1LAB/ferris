from ctypes import *
from my_libs.OB1L1B import to_c_array_string, Player, output_time, date_range_str, if_before_date, get_config


def get_activity(first_date, second_date, players):
    activity, len_days = {}, 1
    sorted_players_activity = []
    logs_path = get_config()['logs_path']
    days = date_range_str(first_date, second_date)
    len_days = len(days)
    before_day, days = if_before_date(days, logs_path)
    c_players = to_c_array_string(players)
    c_days = to_c_array_string(days)
    activity_data = c_lib.getActivity(c_players, c_days, logs_path.encode(), before_day)
    for i in range(len(c_players)-1):
        activity[cast(activity_data[i].nickName[0], c_char_p).value.decode()] = {
            'local_msg': activity_data[i].local_msg,
            'global_msg': activity_data[i].global_msg,
            'private_msg': activity_data[i].private_msg,
            'warns': activity_data[i].warns,
            'kicks': activity_data[i].kicks,
            'mutes': activity_data[i].mutes,
            'bans': activity_data[i].bans,
            'online_time': output_time(activity_data[i].online_time),
            'vanish_time': output_time(activity_data[i].vanish_time),
            'avg_online_time': output_time(int(activity_data[i].online_time/len_days)),
            'avg_vanish_time': output_time(int(activity_data[i].vanish_time/len_days)),
        }
    for player in players:
        sorted_players_activity.append({
            'Player': player,
            'local_msg': activity[player]['local_msg'],
            'global_msg': activity[player]['global_msg'],
            'private_msg': activity[player]['private_msg'],
            'warns': activity[player]['warns'],
            'kicks': activity[player]['kicks'],
            'mutes': activity[player]['mutes'],
            'bans': activity[player]['bans'],
            'AVG': f'{activity[player]["avg_online_time"]}<br/>{activity[player]["avg_vanish_time"]}',
            'Total': f'{activity[player]["online_time"]}<br/>{activity[player]["vanish_time"]}'
        })
    return sorted_players_activity


c_lib = CDLL('my_libs/main.dll', winmode=0x8)
c_lib.getActivity.restype = POINTER(Player)
c_lib.getActivity.argtypes = [POINTER(c_char_p), POINTER(c_char_p), c_char_p, c_bool]
