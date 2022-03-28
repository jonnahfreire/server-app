import os
import sys
import subprocess

def get_process_list():
    output = os.popen('wmic process get description, processid').read()
    output = output.replace(" ", "").replace("\n\n", ":").split(":")
    process_list = []
    
    for process in output:
        if ".exe" in process:
            process_name = process[:process.rindex(".exe")+4]
            pid = process[process.rindex(".exe")+4:]
            process_list.append([process_name, pid])
    return process_list


def process_running(proc_name: str):
    process_list = get_process_list()

    for process in process_list:
        if proc_name == process[0]:
            return process[0], process[1]
    return False, False


def process_kill(pid: str):
    if sys.platform == "win32":
        subprocess.run(f"TASKKILL /F /PID {pid}")