import socket
import subprocess
import os

HOST, PORT = 'adminLOG', 8080

# создание сокета, привязка
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # сокет;  IPv4, TPC
server_socket.bind((HOST, PORT))

# прослушивание клиентов (ожидание их подключения)
server_socket.listen(5)
print('Сервер был запущен... Ожидает подключение клиента...')

# подключен клиент






