import os
from app import socketio
from my_libs.OB1L1B import date_range_str
from my_libs.config import Config


def add_date_line(line, date):
    if line.startswith('['):
        log = line.split()
        return f"[{date} {log[0].split('[')[1]} {' '.join(log[1:])}"
    else:
        return f'{date} {line}'


def global_find(first_date, second_date, find_data, server):
    find_logs = []
    not_found_logs = []
    dates = date_range_str(first_date, second_date)
    if find_data['selectedTypeFind'] == "chatPublic":
        logs_path = f'{Config.logs_path}/{server}/chat_public'
        local_logs = os.listdir(logs_path)
        white_list = find_data['chatPublic']['whiteList'].lower().replace(', ', ',').splitlines()
        black_list = find_data['chatPublic']['blackList'].lower().replace(', ', ',').splitlines()
        is_white_list = len(white_list) > 0
        is_black_list = len(black_list) > 0
        for date in dates:
            if f'{date}.txt' not in local_logs:
                not_found_logs.append(date)
                continue
            with open(f'{logs_path}/{date}.txt', encoding='utf-8') as file:
                for line in file:
                    black_line_status = False
                    if is_black_list:
                        for black_line in black_list:
                            is_black_line = True
                            black_words = black_line.split(',')
                            for word in black_words:
                                if word not in line.lower():
                                    is_black_line = False
                                    break
                            if is_black_line:
                                black_line_status = True
                                break
                    if black_line_status:
                        continue
                    if is_white_list:
                        for white_words in white_list:
                            words = white_words.split(',')
                            is_white = True
                            for word in words:
                                if word not in line.lower():
                                    is_white = False
                                    break
                            if is_white:
                                find_logs.append(add_date_line(line, date))
                                break
                    else:
                        find_logs.append(add_date_line(line, date))
    elif find_data['selectedTypeFind'] == "chatPrivate":
        logs_path = f'{Config.logs_path}/{server}/chat_private'
        local_logs = os.listdir(logs_path)
        white_list = find_data['chatPrivate']['whiteList'].lower().replace(', ', ',').splitlines()
        black_list = find_data['chatPrivate']['blackList'].lower().replace(', ', ',').splitlines()
        is_white_list = len(white_list) > 0
        is_black_list = len(black_list) > 0
        for date in dates:
            date_private = date.split('-')
            date_private = f'{date_private[2]}-{date_private[1]}-{date_private[0]}'
            offset = 1
            while True:
                offset_date = f'{date_private}-{offset}.log'
                if offset_date not in local_logs:
                    if offset == 1:
                        not_found_logs.append(date_private)
                    break
                with open(f'{logs_path}/{offset_date}', encoding='utf-8') as file:
                    for line in file:
                        black_line_status = False
                        if is_black_list:
                            for black_line in black_list:
                                is_black_line = True
                                black_words = black_line.split(',')
                                for word in black_words:
                                    if word not in line.lower():
                                        is_black_line = False
                                        break
                                if is_black_line:
                                    black_line_status = True
                                    break
                        if black_line_status:
                            continue
                        if is_white_list:
                            for white_words in white_list:
                                words = white_words.split(',')
                                is_white = True
                                for word in words:
                                    if word not in line.lower():
                                        is_white = False
                                        break
                                if is_white:
                                    find_logs.append(add_date_line(line, date))
                                    break
                        else:
                            find_logs.append(add_date_line(line, date))
                offset += 1
    elif find_data['selectedTypeFind'] == "dropPrivate":
        logs_path = f'{Config.logs_path}/{server}/drop_private'
        local_logs = os.listdir(logs_path)
        white_list = find_data['dropPrivate']['whiteList'].lower().replace(', ', ',').splitlines()
        black_list = find_data['dropPrivate']['blackList'].lower().replace(', ', ',').splitlines()
        worlds = find_data['dropPrivate']['worlds']
        is_white_list = len(white_list) > 0
        is_black_list = len(black_list) > 0
        is_worlds = len(worlds) > 0
        x, z, x1, z1, x2, z2, radius = None, None, None, None, None, None, None
        is_square, is_radius = None, None
        if find_data['dropPrivate']['type'] == 'square':
            if (find_data['dropPrivate']['pos1']['x'] and find_data['dropPrivate']['pos1']['z']
                    and find_data['dropPrivate']['pos2']['x'] and find_data['dropPrivate']['pos2']['z']):
                is_square = True
                x1, z1 = int(find_data['dropPrivate']['pos1']
                             ['x']), int(find_data['dropPrivate']['pos1']['z'])
                x2, z2 = int(find_data['dropPrivate']['pos2']
                             ['x']), int(find_data['dropPrivate']['pos2']['z'])
        elif find_data['dropPrivate']['type'] == 'radius':
            if (find_data['dropPrivate']['pos']['x'] and find_data['dropPrivate']['pos']['z'] and find_data['dropPrivate']['radius']):
                is_radius = True
                x, z = int(find_data['dropPrivate']['pos']['x']), int(
                    find_data['dropPrivate']['pos']['z'])
                radius = int(find_data['dropPrivate']['radius'])
        for date in dates:
            date = date.replace('-', '.')
            if f'{date}.log' not in local_logs:
                not_found_logs.append(date)
                continue
            with open(f'{logs_path}/{date}.log', encoding='utf-8') as file:
                for line in file:
                    world = line.split('Мир: ')[1].split()[0]
                    x_line = int(line.split('x=')[1].split(',')[0])
                    z_line = int(line.split('z=')[1].split(']')[0])
                    if is_worlds and world not in worlds:
                        continue
                    if is_square and not (x1 <= x_line <= x2 and z1 <= z_line <= z2):
                        continue
                    if is_radius and not (x-radius <= x_line <= x+radius and z-radius <= z_line <= z+radius):
                        continue
                    black_line_status = False
                    if is_black_list:
                        for black_line in black_list:
                            is_black_line = True
                            black_words = black_line.split(',')
                            for word in black_words:
                                if word not in line.lower():
                                    is_black_line = False
                                    break
                            if is_black_line:
                                black_line_status = True
                                break
                    if black_line_status:
                        continue
                    if is_white_list:
                        for white_words in white_list:
                            words = white_words.split(',')
                            is_white = True
                            for word in words:
                                if word not in line.lower():
                                    is_white = False
                                    break
                            if is_white:
                                find_logs.append(add_date_line(line, date))
                                break
                    else:
                        find_logs.append(add_date_line(line, date))
    if not_found_logs:
        socketio.emit('error', f'Не найдены логи с {not_found_logs[0]} по {not_found_logs[-1]}')
    return find_logs
