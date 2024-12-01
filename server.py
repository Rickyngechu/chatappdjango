import socket
import threading


clients = {}
groups = {"developers": []}  # Default group


def broadcast(group_name, message, sender=None):
    for client in groups[group_name]:
        if client != sender:
            try:
                client.send(message.encode())
            except:
                groups[group_name].remove(client)

# Handle communication with a single client
def handle_client(client_socket, address):
    print(f"{address} connected.")
    client_socket.send("Welcome to the kyu developers chat! Enter your name:".encode())
    name = client_socket.recv(1024).decode()
    clients[name] = client_socket
    groups["developers"].append(client_socket)
    
    client_socket.send("You joined the 'developers' group. Use @<group> to switch groups.".encode())

    try:
        while True:
            message = client_socket.recv(1024).decode()
            if message.startswith("@"):
                # Handle group switching or private messaging
                target = message.split(" ")[0][1:]
                if target in groups:
                    groups[target].append(client_socket)
                    client_socket.send(f"You joined the '{target}' group.".encode())
                elif target in clients:
                    clients[target].send(f"[Private] {name}: {message.split(' ', 1)[1]}".encode())
                else:
                    client_socket.send("Group/User not found.".encode())
            else:
                # Broadcast message to the current group
                broadcast("developers", f"{name}: {message}", sender=client_socket)
    except:
        print(f"{name} disconnected.")
        groups["developers"].remove(client_socket)
        del clients[name]
        client_socket.close()


def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('0.0.0.0', 5000))
    server.listen(5)
    print("Server listening on port 5000...")

    while True:
        client_socket, client_address = server.accept()
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.start()

if __name__ == "__main__":
    main()
