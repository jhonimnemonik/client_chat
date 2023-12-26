import socket
import threading

SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345
clients = []


def handle_client(client_socket, addr, name):
    try:
        print(f"По адресу {addr} подключился: {name}")

        while True:
            data = client_socket.recv(1024)
            if not data:
                break
            message = f"{name}: {data.decode('utf-8')}"
            print(f"Сообщение от {addr}: {message}")
            broadcast(message, client_socket)
    except Exception as e:
        print(f"Ошибка: {e}")
    finally:
        client_socket.close()


def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message.encode('utf-8'))
            except Exception as e:
                print(f"Ошибка отправки: {e}")
                clients.remove(client)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(50)
    print(f"Сервер запущен! {SERVER_HOST}:{SERVER_PORT}")
    while True:
        client_socket, addr = server_socket.accept()
        name = client_socket.recv(1024).decode('utf-8')
        clients.append(client_socket)
        client_handler = threading.Thread(target=handle_client, args=(client_socket, addr, name))
        client_handler.start()


if __name__ == "__main__":
    main()
