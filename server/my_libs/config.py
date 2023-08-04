import os
import platform
import requests


def get_staff():
    return requests.get('https://ob1lab.ru/api/staff').json()


def info_server():
    return requests.get('https://ob1lab.ru/api/info').json()


class Config:
    program_path = os.getcwd()
    logs_path = f'{program_path}/logs'
    staff = get_staff()
    servers = ['HTC Titan', 'HTC Phobos', 'HTC Elara']
    private_chat_commands = ['/tell', '/m', '/w',
                             '/msg', '/pm', '/t', '/whisper', '/mail']
    mute_commands = ['/mute', '/tempmute']
    ban_commands = ['/ban', '/tempban']
    info_server = info_server()
    if platform.system() == 'Windows':
        minecraft_path = f'{os.getenv("APPDATA")}/McSkill/updates/Industrial_1.7.10/'
    else:
        minecraft_path = '/home/ob1cham/McSkill/updates/Industrial_1.7.10'

    def create_files(self):
        if 'logs' not in os.listdir(self.program_path):
            os.mkdir(self.logs_path)
        local_servers = os.listdir(self.logs_path)
        for server in self.servers:
            path = f'{self.logs_path}/{server}'
            if server not in local_servers:
                os.mkdir(path)
            if 'chat_public' not in os.listdir(path):
                os.mkdir(f'{path}/chat_public')
            if 'chat_private' not in os.listdir(path):
                os.mkdir(f'{path}/chat_private')
            if 'drop_private' not in os.listdir(path):
                os.mkdir(f'{path}/drop_private')
