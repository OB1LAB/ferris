import platform


class Config:
    staff_url = 'https://mcskill.net/api/v2/?section=admin&action=get_crew'
    servers = ['HTC Titan', 'HTC Phobos', 'HTC Elara']
    junior_staff = ['helper1', 'helper2', 'moder']
    server_names_convert = {
        'HiTech #1 1.7.10 - Titan': 'HTC Titan',
        'HiTech #2 1.7.10 - Phobos': 'HTC Phobos',
        'HiTech #3 1.7.10 - Elara': 'HTC Elara'
    }
    private_chat_commands = ['/tell', '/m', '/w', '/msg', '/pm', '/t', '/whisper', '/mail']
    mute_commands = ['/mute', '/tempmute']
    ban_commands = ['/ban', '/tempban']
    if platform.system() == 'Windows':
        pass
    else:
        program_path = '/home/ob1cham/OB1LAB/python/ferris/server'
        minecraft_path = '/home/ob1cham/McSkill/updates/Industrial_1.7.10'
