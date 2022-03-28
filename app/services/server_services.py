import requests
from time import sleep
from config.local import BASE

from utils.proc import process_running
from services.ngrok import get_ngrok_tunnels


def set_server_conn(ip: str, port: int, thread: bool = False):
    try:
        base = f"{BASE}/set-server-info?url=&ip={ip}&port={port}"
        response = requests.get(base)
        if response.status_code == 200:
            if not thread:
                print("[+] Server info updated")

    except Exception:
        print("[-] Failed updating server info")


def update_server_info():
    global SERVER_IS_RUNNING
    while SERVER_IS_RUNNING:
        _, pid = process_running("ngrok.exe")
        if pid and SERVER_IS_RUNNING:
            sleep(20)
            ip, port = get_ngrok_tunnels()
            if ip and port:
                set_server_conn(ip, port, True)