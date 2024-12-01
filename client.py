import socket
import threading

def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode()
            print(message)
        except:
            print("Disconnected from server.")
            client_socket.close()
            break

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(('127.0.0.1', 5000))
    print("Connected to the server.")

    # Start a thread for receiving messages
    threading.Thread(target=receive_messages, args=(client,)).start()

    try:
        while True:
            message = input()
            client.send(message.encode())
    except KeyboardInterrupt:
        print("Exiting...")
        client.close()

if __name__ == "__main__":
    main()
