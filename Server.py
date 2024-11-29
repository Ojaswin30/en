# cd college\5th sem\Exploring the Networks\Chat Application

import socket
import threading
from cryptography.fernet import Fernet


key = Fernet.generate_key()
cipher = Fernet(key)

clients = {}

def handle_client(client_socket, addr):
    clients[addr] = client_socket  # Add client to the dictionary
    print(f"Client {addr} connected.")

    while True:
        try:
            encrypted_message = client_socket.recv(1024)
            if not encrypted_message:
                print(f"Connection with {addr} closed.")
                break

            decrypted_message = cipher.decrypt(encrypted_message).decode('utf-8')
            print(f"Received from {addr}: {decrypted_message}")

            try:
                target_address_str, actual_message = decrypted_message.split(":", 1)
                target_address = eval(target_address_str.strip())

                print(f"Routing message to {target_address}: {actual_message}")

                if target_address in clients:
                    target_client = clients[target_address]
                    encrypted_response = cipher.encrypt(actual_message.encode('utf-8'))
                    target_client.send(encrypted_response)
                    print(f"Message sent to {target_address}")
                else:
                    print(f"Client {target_address} not connected.")
                    failure_message = f"Client {target_address} not connected."
                    encrypted_response = cipher.encrypt(failure_message.encode('utf-8'))
                    client_socket.send(encrypted_response)

            except ValueError as e:
                print(f"Error in message format: {e}")
        
        except Exception as e:
            print(f"An error occurred: {e}")
            break

    del clients[addr]
    client_socket.close()



def start_server(host='127.0.0.1', port=65432):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()
    print(f"Generated Key: {key.decode()}")
    print(f"Server listening on {host}:{port}")

    while True:
        client_socket, addr = server.accept()
        print(f"Accepted connection from {addr}")
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr))
        client_handler.start()


if __name__ == "__main__":
    start_server()
