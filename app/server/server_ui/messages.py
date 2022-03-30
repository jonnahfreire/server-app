connection_recv_from = "\nConnection received from: {}\nPress enter to continue.."

socket_creation_error = "[-] Error: Cannot create socket"

ls_conn_header = f"{'_'*50}\nID{6*' '}IP{10*' '}PORT  {10*' '}NAME{6* ' '}\n{50*'_'}"
ls_conn_addrs = lambda i, conn: f"{i+1}{5 * ' '}{conn['address'][0]}{5*' '}{conn['address'][1]}{5*' '}{conn['hostname']}"

no_conn_available = "[-] No connections available"

screenshot_success = "[+] Screenshot saved"
screenshot_error = "[-] Failed to save screenshot"

speak_success = "[+] Finished speaking"

dir_not_found_error = "[-] Error: directory '{}' was not found"

client_ready = "[+] ready"

connecting_to = "[+] Connecting to {}: {}"
connected_to =  "[+] Connected to {}: {}"

download_request = "\n[+] Download request"
upload_request = "\n[+] Upload request"

download_error = "[-] Error: Could not download file {}"

recv_file_update = "[+] Receiving update: {}"
receiving_file = "[+] Receiving file: {}"
file_size_b = "[+] Size in bytes: {} Kb"
file_sent_success = "[+] File sent succesfully"
file_send_failed = "[-] Failed sending file"
file_recv_success = "[+] File received successfully\n"
file_recv_failed = "[-] Failed receiving file"
sending_file = "[+] Sending file: {}"

target_ready = "[+] Target ready"
upl_file = "[+] Uploading file.."
upl_failed = "[-] Upload failed. Target is not ready"
file_path_not_found = "[-] Error: file or path was not found"


restarting = "[+] Restarting..."


failed_getting_server_info = "[-] Failed getting server info"
failed_updating_server_info = "[-] Failed updating server info"
server_info_updated = "[+] Server info updated"
