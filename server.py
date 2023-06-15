import socket
import subprocess
import os
import threading


# функция по окраске текста
def colorize(text, color_code):
    if color_code == 'red': # покраска текста в красный (ошибка)
        return f'\033[91m{text}\033[0m'
    elif color_code == 'yellow': # покраска текста в желтый (предупреждение)
        return f'\033[93m{text}\033[0m'
    elif color_code == 'green': # покраска текста в зеленый (успешно)
        return f'\033[92m{text}\033[0m'
    else:
        return f'{text}'



# функция запуска сервера
def start_server():
    HOST, PORT = '192.168.0.103', 12345

    # создание сокета, привязка
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # сокет;  IPv4, TPC
    server_socket.bind((HOST, PORT))

    # прослушивание клиентов (ожидание их подключения)
    server_socket.listen(5)
    print(colorize('Сервер был запущен... Ожидает подключение клиента...', 'green'))


    while True:
        # подключен клиент
        sock_client, sock_adress = server_socket.accept()
        print(colorize(f'Клиент подключен: [*{sock_adress}*]  [*{sock_client}*]\n', 'green'))

        client_thread = threading.Thread(target=send_cmd, args=(sock_client, sock_adress))
        client_thread.start()



# функция работы cmd запросов
def send_cmd(sock_client, sock_adress):
    # отправка файла клиенту
    def send_file(file_name):
        with open(file_name, 'rb') as file:
            while True:
                file_data = file.read(1024)
                if len(file_data) == 0:
                    break
                sock_client.sendall(file_data)

    # обработка комманд cmd
    while True:
        cmd = sock_client.recv(1024).decode('utf-8')

        if cmd.startswith('download'):
            _, file_name = cmd.split(' ', 1)
            send_file(file_name)
            continue

        if cmd is None:
            break


        print(f'{colorize("Команда от клиента:", "yellow")} [- {cmd} -]')

        try:
            #  Создается новый процесс, в котором выполняется команда cmd. shell=True указывает на то, что команда будет выполнена через командную оболочку
            process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                       stdin=subprocess.PIPE)
            output, error = process.communicate()

            # проверка винда или линукс это, для установки соотвествующей кодировки, чтобы русский текст выводился и на линукс, и на винде
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

start_server()

