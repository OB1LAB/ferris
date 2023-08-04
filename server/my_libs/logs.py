from my_libs.OB1L1B import read_file
from my_libs.coloredLog import colored_line
from my_libs.config import Config


# Поиск совпадение в логе из списка
def contains_log(line, words):
    for word in words:
        if word in line:
            return True
    return False


# Получение информации в скбобках
def in_brackets(line):
    data = []
    left_brackets = line.split('[')[1:]
    if left_brackets:
        for i in left_brackets[1:]:
            data.append(i.split(']')[0])
    return data


# Получение типа лога
def get_log_data(line):
    log = line.split()
    data_log = {
        'content': line,
        'type': 'Other',
        'player': None
    }
    allowed_types = ['mod_chat', 'alisa', 'private_msg', 'afk',
                     'afk_returned', 'local_msg', 'global_msg', 'bd_msg', 'discord_msg']
    data_in_brackets = in_brackets(line)
    if data_in_brackets:
        data_in_brackets = data_in_brackets[0]
    if len(log) > 5 and data_in_brackets and log[5] not in types_chat and contains_log(data_in_brackets,
                                                                                       ['thread/DEBUG', 'thread/WARN', 'thread/ERROR',
                                                                                        'thread/INFO', 'thread/TRACE']):
        if log[4] == '[CHAT]':
            data_log['content'] = f'{log[0]} {" ".join(log[5:])}'
        if log[5] == '[Мод.Чат]':
            data_log['type'] = 'mod_chat'
            data_log['player'] = log[6].split(':')[0]
        elif log[5] == '[Малышка]':
            data_log['type'] = 'alisa'
        elif len(log) > 7 and (log[5] == '[Я' or log[7] == 'Я]'):
            data_log['type'] = 'private_msg'
            if log[5] == '[Я':
                data_log['player'] = log[7].split(']')[0]
            else:
                data_log['player'] = log[5].split('[')[0]
        elif len(log) == 7 and log[6] == 'отошел.':
            data_log['type'] = 'afk'
            data_log['player'] = log[5]
        elif len(log) == 7 and log[6] == 'вернулся.':
            data_log['type'] = 'afk_returned'
            data_log['player'] = log[5]
        else:
            data_log['type'] = 'Thread information'
    elif len(log) > 2 and data_in_brackets and (len(log) < 6 or log[5] not in types_chat) and contains_log(data_in_brackets,
                                                                                                           ['main/DEBUG', 'main/INFO', 'main/TRACE', 'main/WARN,'
                                                                                                            'main/ERROR']):
        data_log['type'] = 'Main information'
    elif len(log) > 2 and data_in_brackets and (len(log) < 6 or log[5] not in types_chat) and contains_log(data_in_brackets, ['DEBUG', 'INFO', 'TRACE', 'WARN']):
        data_log['type'] = 'Other information'
    elif len(log) and log[0] in ['at', 'java.lang.NullPointerException', 'java.io.IOException:']:
        data_log['type'] = 'Error'
    elif len(log) > 5 and log[4] == '[CHAT]':
        data_log['content'] = f'{log[0]} {" ".join(log[5:])}'
        if log[5] == '[L]':
            data_log['type'] = 'local_msg'
            if log[6].endswith(':'):
                data_log['player'] = log[6].split(':')[0]
            elif log[7].endswith(':'):
                data_log['player'] = log[7].split(':')[0]
            else:
                data_log['player'] = log[8].split(':')[0]
        elif log[5] == '[G]':
            data_log['type'] = 'global_msg'
            if log[6].endswith(':'):
                data_log['player'] = log[6].split(':')[0]
            elif log[7].endswith(':'):
                data_log['player'] = log[7].split(':')[0]
            else:
                data_log['player'] = log[8].split(':')[0]
        elif log[5] == '[Объявление]':
            data_log['type'] = 'bd_msg'
        elif log[5] == '[D]':
            data_log['type'] = 'discord_msg'
            if log[6].endswith(':'):
                data_log['player'] = log[6].split(':')[0]
            elif log[7].endswith(':'):
                data_log['player'] = log[7].split(':')[0]
            else:
                data_log['player'] = log[8].split(':')[0]
    return {
        'value': colored_line(data_log),
        'player': data_log['player']
    }


# Получение всех биндов
def get_macro_keys():
    data = {}
    keys = read_file(
        f'{Config.minecraft_path}/liteconfig/common/macros/.gui.xml',
        encoding='utf-8'
    )
    for line in keys.split('<gc:button')[1:]:
        name = line.split('<text>')[1].split('</text>')[0]
        macros_id = line.split('id="')[1].split('"')[0]
        data[macros_id] = name
    return data


# Получение значений всех биндов
def get_value_macros():
    data = {}
    keys = get_macro_keys()
    macros = read_file(
        f'{Config.minecraft_path}/liteconfig/common/macros/.macros.txt')
    for line in macros.split('Macro[')[1:]:
        macros_id = line.split(']')[0]
        if macros_id in keys and '.Macro=' in line:
            value = line.split('.Macro=')[1].splitlines()[0]
            if '$$' not in value:
                if value.startswith('!'):
                    value = value[1:]
                data[keys[macros_id]] = value
    return data


types_chat = ['[L]', '[G]', '[D]', '[Объявление]']
