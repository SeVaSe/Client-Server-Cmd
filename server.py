import select
import socket
import subprocess
import os
import threading
import signal
import shutil



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



# КЛАСС ДЛЯ РАБОТЫ С ДОПОЛНИТЕЛЬНЫМИ КОМАНДАМИ
class DopCmdCommands:
    # отключение клиента
    def closeCL(self):
        print(f'{colorize("Клиент был закрыт".upper(), "red")}\n')
        self.sock_client.sendall('Клиент отключен'.encode('utf-8'))
        self.sock_client.close()

    # отключение сервера
    def closeSRV(self):
        print(f'{colorize("Сервер был выключен".upper(), "red")}\n')
        self.sock_client.sendall('Сервер был выключен'.encode('utf-8'))
        self.sock_client.close()
        os.kill(os.getpid(), signal.SIGINT)  # Прерывание основного цикла



# КЛАСС ДЛЯ РАБОТЫ С ФАЙЛАМИ
class WorkWithFiles:
    # поиск файла и копирование
    def find_copy_file(self, file_name, destin_path):
        # проверка файла, на то, что есть ли он в текущей директории
        destin_file_now = os.path.join("C:\PYTHON_\_PROJECT_PYTHON\Python_Project_Other\socket", file_name)
        if os.path.exists(destin_file_now):
            print(
                f'{colorize("[- ", "yellow")}{colorize("Файл уже существует в целевой директории: ", "green")}{colorize(destin_path, "red")}{colorize(" -]", "yellow")}')
            return self.send_file(file_name, file_flag=False)

        # поиск файла на пк
        for root, dirs, files in os.walk('/'):
            if file_name in files:
                file_path = os.path.join(root, file_name)

                # копирование файла в дирректорию сервера
                shutil.copy2(file_path, destin_path)
                print(
                    f'{colorize("[- ", "yellow")}{colorize("Файл скопирован в дирректорию: ", "green")}{colorize(destin_path, "red")}{colorize(" -]", "yellow")}')
                return True

        print(f'{colorize("[- ", "yellow")}{colorize("Файл был не найден на данном устройстве!", "red")}{colorize(" -]", "yellow")}')
        return False

    # отправка файла клиенту
    def send_file(self, file_name, file_flag=True):
        if file_flag:
            # создаем путь, куда сохраним наш файл
            destin_path = os.path.join("C:/PYTHON_/_PROJECT_PYTHON/Python_Project_Other/socket/cacheSRV", file_name)
            self.sock_client.sendall(destin_path.encode('utf-8'))

            if self.find_copy_file(file_name, destin_path):
                # чтение нового файла и отправка его содержимого клиенту
                with open(destin_path, 'rb') as file:
                    while True:
                        file_data = file.read(1024)
                        if len(file_data) == 0:
                            break
                        self.sock_client.sendall(file_data)
        else:
            with open(file_name, 'rb') as file:
                while True:
                    file_data = file.read(1024)
                    if len(file_data) == 0:
                        break
                    self.sock_client.sendall(file_data)

    # принятие файлов от клиента
    def receiv_file(self, file_path):
        self.sock_client.sendall(f'upload {file_path}'.encode('utf-8'))
        with open(file_path, 'wb') as file:
            while True:
                readable, _, _ = select.select([self.sock_client], [], [], 10.0)
                if readable:
                    file_data = self.sock_client.recv(1024)
                    if not file_data:
                        break
                    file.write(file_data)
                else:
                    break



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
    # класс, для обработки дополнительных команд
    dop_cmd_commands = DopCmdCommands()
    dop_cmd_commands.sock_client = sock_client

    # класс, для работы с файлами
    work_with_files = WorkWithFiles()
    work_with_files.sock_client = sock_client



    '''Оператор os.walk() используется для рекурсивного обхода директорий и файловой структуры, начиная с указанного пути.
    root - текущая дирректория
    dirs - Поддиректории
    files - Файлы'''


    # обработка комманд cmd
    while True:

        cmd = sock_client.recv(1024).decode('utf-8')

        if cmd.startswith('download'):
            _, file_name = cmd.split(' ', 1)
            work_with_files.send_file(file_name)
            print(f'{colorize("Отправлен файл на клиент", "green")}\n')
            continue
        if cmd.startswith('upload'):
            _, file_path = cmd.split(' ', 1)
            work_with_files.receiv_file(file_path)
            print(f'{colorize("Был получен файл от клиента", "green")}\n')
            continue

        if cmd == '':
            print(f'{colorize("КЛИЕНТ УПАЛ! Перезапустите его или проверьте интернет-соединение", "red")}\n')
            break
        else:
            print(f'{colorize("Команда от клиента:", "yellow")} [- {cmd} -]')

        if cmd == 'closeCL':
            dop_cmd_commands.closeCL()
        elif cmd == 'closeSRV':
            dop_cmd_commands.closeSRV()



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


# запуск подключений клиентов
start_server()






