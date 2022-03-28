import os, sys
from config.local import LOCAL_HOST


def clear():
    OS = sys.platform == "win32"
    os.system("cls") if OS else os.system("clear")

def help():
    clear()
    print('_'*65)
    print('exit                        -    returns server interface')
    print('cls                         -    clears the output on server')
    print('startup                     -    gets client start folder path')
    print('list | ls                   -    list all connections available')
    print('select id                   -    select a client by id')
    print('"."                         -    select the first one')
    print('download file -o outfile    -    downloads a file')
    print('upload   file               -    uploads a file')
    print('dumplog                     -    get keylogger logs from client')
    print('temp                        -    move to temp folder')
    print('speak msg                   -    send a text to client to be speaked')
    print('scr | print                 -    get screenshot on the client')
    print('update-server               -    update server ip / port')
    print('send update                 -    send an updated msrvc version to client')
    print('restart                     -    restarts client connection')
    print('shutdown                    -    shutdown client connection')
    print(65*'_')
    print(f'Local Address: {LOCAL_HOST[0]}:{LOCAL_HOST[1]}')
    print(f'Ngrok tunnel: {NGROK_IP}: {NGROK_PORT}')
    print('_'*65)