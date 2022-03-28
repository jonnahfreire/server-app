import threading
import socket
import sys
import json

from config.local import LOCAL_HOST
from config.encodings import ENCODING
from utils.globals import clear

# from server_ui.interface import prompt
from config.command_map import restart


class Server:
    def __init__(self, listen: int = 5) -> None:
        self.server: socket = None
        self.connections: list = []
        self.is_running: bool = False
        self.listen: int = listen

    def create_workers(self):
        threaded_workers = [self.accept, prompt]
        for worker in threaded_workers:
            t = threading.Thread(target=worker, args=(self.server,))
            t.start()

    def run(self):
        try:
            self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server.bind(LOCAL_HOST)
            self.server.listen(self.listen)
            self.is_running = True

        except socket.error:
            print("[-] Error: Cannot create socket")
            sys.exit(1)
    
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
                host_info = sockaddr.recv(1024).decode(ENCODING)
                host_info = json.loads(host_info)
                connection_info = {"conn": sockaddr, "address": [
                    host_info["ipaddr"], addr[1]], "hostname": host_info["hostname"]}

                if host_info["hostname"] is not None or not host_info["hostname"] == "":
                    self.connections.append(connection_info)

                    sockaddr.send("ready".encode(ENCODING))

                    print("\nConnection received from: ", host_info["hostname"])
                    print("Press enter to continue..")

            except Exception:
                break

    def shutdown(self):
        if self.connections:
            try:
                [self.connections[i]["conn"].send(restart.encode(ENCODING))
                    for i in range(len(self.connections))]
            except ConnectionResetError:
                self.is_running = False
                self.server.close()
    

    def list_connections(self):
        print(
            f"{'_'*50}\nID{6*' '}IP{10*' '}PORT  {10*' '}NAME{6* ' '}\n{50*'_'}")

        for i, conn in enumerate(self.connections):
            try:
                conn["conn"].send(" ".encode(ENCODING))
            except:
                del self.connections[i]
                continue

        for i, conn in enumerate(self.connections):
            if len(self.connections) > 0:
                print(
                    f"{i+1}{5 * ' '}{conn['address'][0]}{5*' '}{conn['address'][1]}{5*' '}{conn['hostname']}")

        if len(self.connections) == 0:
            print("No connections available")
        print()


    
