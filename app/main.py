import sys

from server.main import Server
from services.ngrok import get_ngrok_tunnels, start_ngrok
from services.server_services import set_server_conn

def main():
    if sys.platform == "win32":
        if start_ngrok():
            print("[+] Starting ngrok tunnel")
            ip, port = get_ngrok_tunnels()
            if ip and port:
                set_server_conn(ip, port)
        else:
            get_ngrok_tunnels()
    else:
        print("[+] Starting ngrok tunnel")
        ip, port = get_ngrok_tunnels()
        if ip and port:
            set_server_conn(ip, port)

    # init_server()
    # create_workers()


if __name__ == "__main__":
    # main()

    server = Server()

    server.run()

    if server.is_running:
        print("Server is running..\n", server.server)

