from Xlib import X, XK
from Xlib.display import Display
from Xlib.protocol.event import KeyPress, KeyRelease
from my_libs.OB1L1B import read_file
from my_libs.config import Config
from my_libs.logs import get_value_macros, get_log_data


def get_event(function, display, current_window, keycode):
	return function(
		time=X.CurrentTime,
		root=display.screen().root,
		window=current_window,
		same_screen=True,
		child=X.NONE,
		root_x=0,
		root_y=0,
		event_x=0,
		event_y=0,
		state=X.Mod1Mask,
		detail=keycode
	)


def press_button(display, current_window):
    keycode = display.keysym_to_keycode(XK.XK_Alt_R)
    current_window.send_event(get_event(KeyPress, display, current_window, keycode))
    display.sync()
    current_window.send_event(get_event(KeyRelease, display, current_window, keycode))
    display.sync()
    display.flush()


class Logs:
    def __init__(self):
        self.display = Display()
        self.root = self.display.screen().root
        self.current_window = None
        self.log_path = f'{Config.minecraft_path}/logs/fml-client-latest.log'
        self.msg_path = f'{Config.minecraft_path}/liteconfig/common/macros/OB1LAB.txt'
        self.macros = get_value_macros()

    def set_minecraft_app(self):
        windowIDs = self.root.get_full_property(self.display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value
        for windowID in windowIDs:
            window = self.display.create_resource_object('window', windowID)
            window_name = window.get_wm_name()
            if type(window_name) == str and 'McSkill' in window_name:
                self.current_window = window
                return True

    def write_msg(self, msg):
        with open(self.msg_path, 'w') as file:
            file.write(msg)

    def send_msg(self, msg):
        if not self.current_window and not self.set_minecraft_app():
            return False
        self.write_msg(msg)
        press_button(self.display, self.current_window)
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
