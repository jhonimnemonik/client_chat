import socket
import threading

HOST = '127.0.0.1'
PORT = 12345


def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024)
            if not data:
                break
            print(f"\n{data.decode('utf-8')}")
        except Exception as e:
            print(f"Ошибка получения сообщения от сервера: {e}")
            break


def send_messages():
    while True:
        message = input()
        try:
            client_socket.send(message.encode('utf-8'))
        except Exception as e:
            print(f"Ошибка отправки сообщения: {e}")
            break


client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
name = input("Введите имя: ")
client_socket.send(name.encode('utf-8'))
receive_thread = threading.Thread(target=receive_messages)
receive_thread.start()
send_thread = threading.Thread(target=send_messages)
send_thread.start()
