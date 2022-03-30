import os
import subprocess

from utils.globals import *


def get_process_list():
    if WIN:
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


def get_pid_by_name(procname: str) -> int:
    if WIN:
        # Not implemented
        pass
    else:
        output = os.popen(f"pidof {procname}").read()
        if len(output) > 0:
            return int(output)
    return 0

def process_kill(pid: str) -> bool:
    if WIN:
        subprocess.run(f"TASKKILL /F /PID {pid}")
        return True
    else:
        try:
            os.system(f"kill {pid}")
        except FileNotFoundError:
            return False
    return True