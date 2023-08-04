import subprocess
from pywinauto import Application
from my_libs.config import Config
from my_libs.OB1L1B import read_file
from my_libs.logs import get_value_macros, get_log_data
from app import socketio


class Logs:
    def __init__(self):
        self.app = None
        self.form = None
        self.offset = 0
        self.run = False
        self.minecraft_pid = None
        self.players = []
        self.history = []
        self.log_path = f'{Config.minecraft_path}/logs/fml-client-latest.log'
        self.msg_path = f'{Config.minecraft_path}/liteconfig/common/macros/OB1LAB.txt'
        self.macros = get_value_macros()
        self.limit = 150
        self.timeout_update = 0.1

    def set_minecraft_app(self):
        pids = subprocess.check_output(
            "tasklist", encoding="cp866").splitlines()
        for pid in pids:
            if 'javaw.exe' in pid.lower():
                self.minecraft_pid = int(pid.split()[1])
                self.app = Application(backend='win32').connect(
                    process=int(self.minecraft_pid), timeout=10)
                self.form = self.app.window()
                return True
        return False

    def write_msg(self, msg):
        with open(self.msg_path, 'w') as file:
            file.write(msg)

    def send_msg(self, msg):
        if not self.app and not self.set_minecraft_app():
            socketio.emit('error', 'Майнкрафт не запущен')
            return False
        self.write_msg(msg)
        self.form.send_keystrokes('{RMENU down}')
        self.form.send_keystrokes('{RMENU}')
        return True

    def parser(self):
        while True:
            while self.run:
                new_msg = []
                file = read_file(self.log_path)
                local_logs = file.splitlines()
                len_lines = len(local_logs)
                if len_lines < self.offset:
                    self.offset = len_lines
                if len_lines - self.offset > self.limit:
                    self.offset = len_lines - self.limit
                for line_index in range(self.offset, len_lines):
                    line_data = get_log_data(local_logs[line_index])
                    if line_data:
                        player = ''
                        if line_data['player'] and line_data['player'] not in self.players:
                            self.players.append(line_data['player'])
                            player = line_data['player']
                        new_msg.append({
                            'lid': line_index,
                            'content': line_data['value'],
                            'player': player
                        })
                        self.history.append(new_msg[-1])
                if new_msg:
                    socketio.emit('new_msg', new_msg)
                self.offset = len_lines
                socketio.sleep(self.timeout_update)
                self.history = self.history[-self.limit:]
            socketio.sleep(1)

    def get_data(self):
        return {
            'macros': self.macros,
            'players': self.players,
            'logs': self.history
        }
