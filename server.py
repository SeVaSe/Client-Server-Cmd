import socket
import subprocess
import os

HOST, PORT = '', 12345

# создание сокета, привязка
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # сокет;  IPv4, TPC
server_socket.bind((HOST, PORT))

# прослушивание клиентов (ожидание их подключения)
server_socket.listen(5)
print('Сервер был запущен... Ожидает подключение клиента...')

# подключен клиент
sock_client, sock_adress = server_socket.accept()
print(f'Клиент подключен: [*{sock_adress}*]  [*{sock_client}*]')


# обработка комманд cmd
while True:
    cmd = sock_client.recv(1024).decode('utf-8')
    print(f'Сообщение от клиента {cmd}')



