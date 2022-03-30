import requests
from time import sleep
from config.local import ROUTE

from server.server_ui.messages import *


def set_server_conn(ip: str, port: int, thread: bool = False):
    try:
        url = ROUTE["set-info"].format(ROUTE["base"], ip, port)
        response = requests.get(url)

        if response.status_code == 200:
            if not thread:
                print(server_info_updated)

    except Exception:
        print(failed_updating_server_info)

