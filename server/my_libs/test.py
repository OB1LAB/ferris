# from ctypes import *
# from my_libs.OB1L1B import to_c_array_string, Player, output_time, date_range_str, if_before_date, get_config
#
#
# activity = {}
# first_date, second_date = '26-02-2023', '05-03-2023'
# players = ['stepanrt_ss', 'salex94']
# c_lib = CDLL('main.dll', winmode=0x8)
# c_lib.getActivity.restype = POINTER(Player)
# c_lib.getActivity.argtypes = [POINTER(c_char_p), POINTER(c_char_p), c_char_p, c_bool]
# logs_path = get_config()['logs_path']
# days = date_range_str(first_date, second_date)
# players = to_c_array_string(players)
# c_days = to_c_array_string(days)
# before_day = if_before_date(first_date, logs_path)
# test = c_lib.getActivity(players, c_days, logs_path.encode(), before_day)
# for i in range(len(players)-1):
#     activity[cast(test[i].nickName[0], c_char_p).value.decode()] = {
#         'local_msg': test[i].local_msg,
#         'global_msg': test[i].global_msg,
#         'private_msg': test[i].private_msg,
#         'warn': test[i].warns,
#         'kicks': test[i].kicks,
#         'mutes': test[i].mutes,
#         'bans': test[i].bans,
#         'online_time': output_time(test[i].online_time),
#         'vanish_time': output_time(test[i].vanish_time),
#     }
# print(activity['salex94']['online_time'], activity['salex94']['vanish_time'])
import os

from logs import get_log_data, in_brackets, contains_log
from OB1L1B import read_file
from my_libs.config import Config

data = read_file(rf"{os.getenv('APPDATA')}\{Config.minecraft_logs_file}").splitlines()
for line in data:
    if line:
        log = get_log_data(line)
        if log['type'] == 'Other':
            print(log)
            if in_brackets(line):
                print(in_brackets(line)[0], contains_log(in_brackets(line)[0],
                                                            ['main/DEBUG', 'main/INFO', 'main/TRACE', 'main/WARN,'
                                                             'main/ERROR']))
