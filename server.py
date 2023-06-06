import socket
import subprocess
import os

HOST, PORT = 'localhost', 12345

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

    if cmd is None:
        break

    print(f'Команда от клиента: [- {cmd} -]')


    try:
        #  Создается новый процесс, в котором выполняется команда cmd. shell=True указывает на то, что команда будет выполнена через командную оболочку
        process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                   stdin=subprocess.PIPE)
        output, error = process.communicate()

        # проверка винда или линукс это, для установки соотвествующей кодировки
        if output:
            if os.name == 'nt':
                answer = output.decode('cp866')
            else:
                answer = output.decode('utf-8')
        else:
            if os.name == 'nt':
                answer = error.decode('cp866')
            else:
                answer = error.decode('utf-8')

        # # выполнение команд
        # output = subprocess.check_output(cmd, shell=True)
        # answer = output.decode('cp866')
    except Exception as e:
        answer = str(e)


    # отправка ответа
    sock_client.sendall(answer.encode('utf-8'))



server_socket.close()
sock_client.close()