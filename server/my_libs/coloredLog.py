import re


classes = {
    'color0': 'color: #000000',
    'color1': 'color: #0000aa',
    'color2': 'color: #00aa00',
    'color3': 'color: #00aaaa',
    'color4': 'color: #aa0000',
    'color5': 'color: #aa00aa',
    'color6': 'color: #ffaa00',
    'color7': 'color: #aaaaaa',
    'color8': 'color: #555555',
    'color9': 'color: #5555ff',
    'colora': 'color: #55ff55',
    'colorb': 'color: #55ffff',
    'colorc': 'color: #ff5555',
    'colord': 'color: #ff55ff',
    'colore': 'color: #ffff55',
    'colorf': 'white'
}

color_codes = {
    "§0": "color: #000000",
    "§1": "color: #0000AA",
    "§2": "color: #00AA00",
    "§3": "color: #00AAAA",
    "§4": "color: #AA0000",
    "§5": "color: #AA00AA",
    "§6": "color: #FFAA00", 
    "§7": "color: #AAAAAA", 
    "§8": "color: #555555",
    "§9": "color: #5555FF", 
    "§a": "color: #55FF55", 
    "§b": "color: #55FFFF", 
    "§c": "color: #FF5555", 
    "§d": "color: #FF55FF",
    "§e": "color: #FFFF55", 
    "§f": "color: white",
    "§k": "",
    "§l": "font-weight: bold",
    "§o": "font-style: italic",
    "§r": "",
    "§m": "text-decoration: line-through",
    "§n": "text-decoration: underline"
}


def format_text(text):
    regex = r"§[0-9a-fklormn]"
    return re.sub(regex, lambda match: f'<span style="{color_codes[match.group()]}">', text).replace("&r", "</span>")


afk_list = ["afk", "afk_returned"]
type_chats = {
    'local_msg': '<span>L</span>',
    'global_msg': f'<span style="{classes["color6"]}">G</span>',
    'bd_msg': f'<span style="{classes["color4"]}">Объявление</span>',
    'mod_chat': f'<span style="{classes["color4"]}">Мод.чат</span>',
    'alisa': f'<span style="{classes["color4"]}">Малышка</span>',
    'discord_msg': f'<span style="{classes["colorc"]}">D</span>',
}
prefix = {
    "[Тех.Админ]": f'<span style="{classes["color4"]}">Тех.Админ</span>',
    "[Куратор]": f'<span style="{classes["color4"]}">Куратор</span>',
    "[Дизайнер]": f'<span style="{classes["color9"]}">Дизайнер</span>',
    "[Гл.Модератор]": f'<span style="{classes["color9"]}">Гл.Модератор</span>',
    "[Ст.Модератор]": f'<span style="{classes["color3"]}">Ст.Модератор</span>',
    "[Модератор]": f'<span style="{classes["color4"]}">Модератор</span>',
    "[Помощник]": f'<span style="{classes["color2"]}">Помощник</span>',
    "[Стажёр]": f'<span style="{classes["colora"]}">Стажёр</span>',
    "[Girl]": f'<span style="{classes["colord"]}">Girl</span>',
    "[Pro]": f'<span style="{classes["colorb"]}">Pro</span>',
    "[Vip]": f'<span style="{classes["color4"]}">Vip</span>',
    "[Gold]": f'<span style="{classes["color6"]}">Gold</span>',
    "[Grand]": f'<span style="{classes["color2"]}">Grand</span>',
    "[Deluxe]": f'<span style="{classes["colord"]}">Deluxe</span>',
    "[Mod]": f'<span style="{classes["color4"]}">Mod</span>',
    "[TrueMod]": f'<span style="{classes["color4"]}">TrueMod</span>',
    "[Creative]": f'<span style="{classes["color9"]}">Creative</span>',
    "[Admin]": f'<span style="{classes["color4"]}">Admin</span>',
    "[Vote]": f'<span style="{classes["color9"]}">Vote</span>',
    "[Новичок]": f'<span style="{classes["color2"]}">Новичок</span>',
    "[Объявление]": f'<span style="{classes["color4"]}">Объявление</span>'
}
has_html = f'</span><span style="{classes["color4"]}">Возможно данная строка содержит html код!</span>'


def has_html_code(s):
    pattern = re.compile('<.*?>')
    return pattern.search(s) is not None


def colored_line(line):
    if has_html_code(line['content']):
        return f'<span style="{classes["color8"]}">{line["content"].split()[0]} {has_html}'
    words = line["content"].split()
    new_line = []
    for index, value in enumerate(words):
        if index == 0 and value.startswith('['):
            new_line.append(
                f'<span style="{classes["color8"]}">{value} </span>'
            )
        elif (
            index == 1
            and line['type'] in type_chats.keys()
        ):
            new_line.append(
                f'<span><span style="{classes["color8"]}">[</span>{type_chats[line["type"]]}<span style="{classes["color8"]}">]</span> </span>'
            )
        elif (
            index in [2, 3]
            and line['type'] in type_chats.keys()
            and value.startswith("[")
        ):
            if prefix.get(value):
                new_line.append(
                    f'<span><span style="{classes["color8"]}">[</span>{prefix[value]}<span style="{classes["color8"]}">]</span> </span>'
                )
            else:
                new_line.append(
                    f'<span><span style="{classes["color8"]}">[</span><span style="{classes["colorb"]}">{value.split("[")[1].split("]")[0]}</span><span style="{classes["color8"]}">]</span> </span>'
                )
        elif (
            index == 2
            and not value.startswith("[")
            and not value.endswith(":")
            and line["type"] in type_chats.keys()
            and line["type"] not in ['bd_msg', 'alisa']
        ):
            new_line.append(
                f'<span style="{classes["color7"]}">{value} </span>'
            )
        elif (
            index in [2, 3, 4]
            and line["type"] in type_chats.keys()
            and value.endswith(":")
        ):
            if index == 2 and value != 'Алиса:' and line["type"] not in ['discord_msg', 'bd_msg']:
                new_line.append(
                    f'<span><span style="{classes["color7"]}">{value[:-1]}</span><span style="{classes["colorf"]}">: </span></span>'
                )
            else:
                new_line.append(
                    f'<span><span style="{classes["color8"]}">{value[:-1]}</span><span style="{classes["color7"]}">: </span></span>'
                )
        elif line["type"] == "private_msg" and index in [1, 2, 3]:
            if index == 2:
                new_line.append(
                    f'<span style="{classes["color6"]}">{value} </span>'
                )
            elif index == 1:
                new_line.append(
                    f'<span><span style="{classes["color6"]}">[</span><span style="{classes["colorc"]}">{value.split("[")[1]} </span></span>'
                )
            else:
                new_line.append(
                    f'<span><span style="{classes["colorc"]}">{value.split("]")[0]}</span><span style="{classes["color6"]}">] </span></span>'
                )
        elif line["type"] in afk_list:
            new_line.append(
                f'<span style="{classes["color5"]}">{value} </span>'
            )
        else:
            new_line.append(f"{value} ")
    return format_text("".join(new_line))
