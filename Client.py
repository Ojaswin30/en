import socket
import threading
from cryptography.fernet import Fernet

key = b'CpIUK0ejZ18sdvlDvn_5zlbFAXqgHeF1mXmspdVAogQ='
cipher = Fernet(key)

def receive_messages(client_socket):
    while True:
        try:
            encrypted_response = client_socket.recv(1024)

            if not encrypted_response:
                print("Server connection closed.")
                break


            decrypted_response = cipher.decrypt(encrypted_response).decode('utf-8')
            print(f"\nReceived message: {decrypted_response}")


        except Exception as e:
            print(f"An error occurred while receiving: {e}")
            break

def start_client(host='127.0.0.1', port=65432):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))


    receive_thread = threading.Thread(target=receive_messages, args=(client,))
    receive_thread.start()

    while True:
        message = input("Enter a message (or 'exit' to quit): ")
        if message.lower() == 'exit':
            break


        encrypted_message = cipher.encrypt(message.encode('utf-8'))
        client.send(encrypted_message)
        print("Message sent to server.")

    client.close()

if __name__ == "__main__":
    start_client()
