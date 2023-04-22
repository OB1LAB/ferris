import os
import subprocess
from my_libs.OB1L1B import get_config, read_file
from pywinauto import Application
from my_libs.config import Config


def fix_last_line(filename: str):  # Удаление у последний строки перенос на новую строку для корректной работы си либы
    file = read_file(filename, encoding='utf-8')
    lines = file.splitlines()
    test = lines[-1]
    if list(test)[-1] == '\n':
        lines[-1] = lines[-1][:-1]
    file = open(filename, 'w', encoding='utf-8')
    file.writelines(lines)
    file.close()


def fix_local_logs():  # Фикс всех локальных логов
    path = get_config()['logs_path']
    for file in path:
        filename = f'{path}/{file}'
        fix_last_line(filename)


def contains_log(line, words):
    for word in words:
        if word in line or word == line:
            return True
    return False


def in_brackets(line):
    data = []
    left_brackets = line.split('[')[1:]
    if left_brackets:
        for i in left_brackets[1:]:
            data.append(i.split(']')[0])
    return data


def get_log_data(line: str) -> dict:
    log = line.split()
    data_log = {
        'content': line,
        'type': 'Other'
    }
    data_in_brackets = in_brackets(line)
    if len(log) > 5 and log[4] == '[CHAT]':
        data_log['content'] = f'{log[0]} {" ".join(log[5:])}'
        if log[5] == '[L]':
            data_log['type'] = 'local_msg'
        elif log[5] == '[G]':
            data_log['type'] = 'global_msg'
        elif len(log) == 7 and log[6] == 'отошел.':
            data_log['type'] = 'afk'
        elif len(log) == 7 and log[6] == 'вернулся.':
            data_log['type'] = 'afk_returned'
    elif len(log) > 2 and data_in_brackets and contains_log(in_brackets(line)[0],
                                                            ['thread/DEBUG', 'thread/WARN', 'thread/ERROR',
                                                             'thread/INFO', 'thread/TRACE']):
        data_log['type'] = 'Thread information'
    elif len(log) > 2 and data_in_brackets and contains_log(in_brackets(line)[0],
                                                            ['main/DEBUG', 'main/INFO', 'main/TRACE', 'main/WARN,'
                                                             'main/ERROR']):
        data_log['type'] = 'Main information'
    elif len(log) > 2 and data_in_brackets and contains_log(in_brackets(line)[0],
                                                            ['DEBUG', 'INFO', 'TRACE', 'WARN']):
        data_log['type'] = 'Other information'
    elif len(log) and log[0] in ['at', 'java.lang.NullPointerException', 'java.io.IOException:']:
        data_log['type'] = 'Error'
    return data_log


def get_macro_keys():
    data = {}
    keys = read_file(
        r'C:\Users\OB1CHAM\AppData\Roaming\McSkill\updates\Industrial_1.7.10\liteconfig\common\macros\.gui.xml',
        encoding='utf-8'
    )
    for line in keys.split('<gc:button')[1:]:
        name = line.split('<text>')[1].split('</text>')[0]
        macros_id = line.split('id="')[1].split('"')[0]
        data[macros_id] = name
    return data


def get_value_macros():
    data = {}
    keys = get_macro_keys()
    macros = read_file(
        r'C:\Users\OB1CHAM\AppData\Roaming\McSkill\updates\Industrial_1.7.10\liteconfig\common\macros\.macros.txt'
    )
    for line in macros.split('Macro[')[1:]:
        macros_id = line.split(']')[0]
        if macros_id in keys and '.Macro=' in line:
            value = line.split('.Macro=')[1].splitlines()[0]
            if '$$' not in value:
                if value.startswith('!'):
                    value = value[1:]
                data[keys[macros_id]] = value
    return data


class Logs:
    def __init__(self):
        self.app = None
        self.form = None
        self.minecraft_pid = None
        self.log_path = rf"{os.getenv('APPDATA')}\{Config.minecraft_logs_file}"
        self.msg_path = rf"{os.getenv('APPDATA')}\{Config.minecraft_msg_file}"
        self.macros = get_value_macros()

    def set_minecraft_app(self):
        pids = subprocess.check_output("tasklist", encoding="cp866").splitlines()
        for pid in pids:
            if 'javaw.exe' in pid.lower():
                self.minecraft_pid = int(pid.split()[1])
                self.app = Application(backend='win32').connect(process=int(self.minecraft_pid), timeout=10)
                self.form = self.app.window()
                return True
        return False

    def write_msg(self, msg):
        with open(self.msg_path, 'w') as file:
            file.write(msg)

    def send_msg(self, msg):
        if not self.app and not self.set_minecraft_app():
            return 'Minecraft not found'
        self.write_msg(msg)
        self.form.send_keystrokes('{RMENU down}')
        self.form.send_keystrokes('{RMENU}')
        return 'ok'

    def parser(self, offset):
        return_lines = []
        file = read_file(self.log_path)
        local_logs = file.splitlines()
        lines = len(local_logs)
        if offset > lines or not offset:
            macros = None
            if not offset:
                macros = self.macros
            return {
                'messages': [],
                'offset': lines,
                'macros': macros
            }
        for line in range(offset, len(local_logs)):
            if not local_logs[line]:
                continue
            log = get_log_data(local_logs[line])
            return_lines.append({
                'lid': line,
                'content': log['content'],
                'type': log['type']
            })
        return {
            'messages': return_lines,
            'offset': lines
        }
