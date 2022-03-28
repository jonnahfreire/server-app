import socket
import os
from config.encodings import ENCODING

def get_filename_from_command(command: str, cmd: str) -> tuple:
    filename = None
    outfile = None
    if "-o" in command:
        file = command.replace(cmd, "").replace(
            '\\', "/").split("-o")
        filename = file[0].strip()
        outfile = file[1].strip()
    else:
        filename = command.replace(
            cmd, "").replace('\\', "/").strip()
    return filename, outfile


def recv_file(target: socket, filename: str, file_size: int, output: str = None):
    try:
        if file_size > 0:
            if output is None:
                output = os.path.join(os.getcwd(), filename)

            if os.path.isfile(output):
                name = os.path.splitext(filename)[0]
                extension = os.path.splitext(filename)[1]
                output = f"{name}-1{extension}"

            with open(output, "wb") as bfile:
                data_size = b''
                while True:
                    if len(data_size) == file_size:
                        break
                    data = target.recv(int(file_size))
                    data_size += data
                    bfile.write(data)
            return 0
        return 1

    except ValueError:
        print(f"[-] Error: Could not download file {filename}")


def send_file(filename: str, target: socket) -> int:
    if os.path.isfile(filename):
        with open(filename, "rb") as bfile:
            for line in bfile.readlines():
                target.send(line)

        return 0
    return 1


def file_download(command: str, target: socket):
    filename, _ = get_filename_from_command(command, "download")
    command = f"upload {filename}".encode(ENCODING)
    target.send(command)

    data = target.recv(1024).decode(ENCODING)
    data = data.replace("download", "").strip().split(" ")

    if not data[0] == "" and data[0].isnumeric():
        file_size = int(data[0])
        filename = data[1]

        target.send("ready".encode(ENCODING))
        print(f"[+] Receiving file: {filename}")
        print(f"[+] Size in bytes: {file_size/1024} Kb")
        stat = recv_file(target, filename, file_size)

        if stat == 0:
            print("[+] File received successfully\n")
        else:
            print("[-] Failed receiving file")


def file_upload(command: str, target: socket):
    if target is not None:
        filename, _ = get_filename_from_command(command, "upload")
        file_to_send = filename.replace(" ", "-")
        if '/' in filename:
            file_to_send = filename.split('/')[-1]

        if os.path.isfile(filename):
            file_size = int(os.stat(filename)[6])

            if file_size > 0:
                print(f"[+] Sending file: {file_to_send}")
                print(f"[+] Size in bytes: {file_size/1024} Kb")

                command = f"download {file_size} {file_to_send}".encode(
                    ENCODING)
                target.send(command)

                syn = target.recv(1024).decode(ENCODING)
                if syn == "ready":
                    print("[+] Target ready")
                    print("[+] Uploading file..")
                    stat = send_file(filename, target)

                    if stat == 0:
                        print("[+] File sent succesfully")
                    else:
                        print("[-] Failed sending file")
                else:
                    print("[-] Upload failed. Target is not ready")
        else:
            print("[-] Error: file or path was not found")
