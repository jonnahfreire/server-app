from services.ngrok import get_ngrok_tunnels, start_ngrok
from services.server_services import set_server_conn

from utils.globals import *
from server.main import Server
from services.server_services import *


def main():
    clear()

    if start_ngrok():
        print("[+] Starting ngrok tunnel")
        sleep(2)

        ip, port = get_ngrok_tunnels()
        if ip and port:
            set_server_conn(ip, port)
            print("[+] Setting server ngrok tunnel")
            sleep(2)
    else:
        set_server_conn(HOST[0], HOST[1])

    print("[+] Starting server")
    sleep(3)

    server = Server()
    server.run()
    server.create_workers()


if __name__ == "__main__":
    main()

