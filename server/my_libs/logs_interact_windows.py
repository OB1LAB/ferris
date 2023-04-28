import subprocess
from pywinauto import Application
from my_libs.OB1L1B import read_file
from my_libs.config import Config
from my_libs.logs import get_value_macros, get_log_data


class Logs:
    def __init__(self):
        self.app = None
        self.form = None
        self.minecraft_pid = None
        self.log_path = f'{Config.minecraft_path}/logs/fml-client-latest.log'
        self.msg_path = f'{Config.minecraft_path}/liteconfig/common/macros/OB1LAB.txt'
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
            return False
        self.write_msg(msg)
        self.form.send_keystrokes('{RMENU down}')
        self.form.send_keystrokes('{RMENU}')
        return True

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
            return_lines.append({
                'lid': line,
                'content': get_log_data(local_logs[line])
            })
        return {
            'messages': return_lines,
            'offset': lines
        }
