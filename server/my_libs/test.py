import time
from Xlib import X, XK
from Xlib.ext import xtest
from Xlib.display import Display
from Xlib.protocol.event import KeyPress, KeyRelease


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
    display.screen().root.grab_keyboard(True, X.GrabModeAsync, X.GrabModeAsync, X.CurrentTime)
    current_window.send_event(get_event(KeyPress, display, current_window, keycode))
    display.sync()
    display.screen().root.ungrab_key(keycode, X.AnyModifier, X.CurrentTime)
    current_window.send_event(get_event(KeyRelease, display, current_window, keycode), propagate=True)
    display.sync()
    display.screen().root.ungrab_key(keycode, X.AnyModifier, X.CurrentTime)
    display.flush()


display = Display()
root = display.screen().root
windowIDs = root.get_full_property(display.intern_atom('_NET_CLIENT_LIST'), X.AnyPropertyType).value
current_window = None
for windowID in windowIDs:
    window = display.create_resource_object('window', windowID)
    window_name = window.get_wm_name()
    if type(window_name) == str and 'McSkill' in window_name:
        current_window = window
if current_window:
    keycode = display.keysym_to_keycode(XK.XK_Alt_R)
    xtest.fake_input(display, X.KeyPress, keycode)
    display.sync()

    # Эмуляция отпускания клавиши
    xtest.fake_input(display, X.KeyRelease, keycode)
    display.sync()
else:
    print('Window not found')

time.sleep(3)
