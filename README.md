# socket_server

# Описание: 

Данный репозиторий содержит реализацию простой сокет-связи между клиентом и сервером. Данная программа работает, как и на Linux так и на Windows для этого потребовалось проработать выводы команд и вывод информации без ее искожения. Проект состоит из двух основных компонентов: сервера и клиента.



# Сервер:

-Сервер создает сокет и привязывается к указанному IP-адресу и порту.
-Он ожидает подключения клиентов и принимает входящие соединения.
-После успешного подключения клиента сервер принимает команды для консоли, отправленные клиентом.
-Команды выполняются на сервере, и их результат отправляется обратно клиенту.
-Сервер остается в режиме прослушивания новых подключений и обработки команд от клиентов.



# Клиент:

-Клиент создает сокет и подключается к указанному IP-адресу и порту сервера.
-После успешного подключения клиент получает приглашение вводить команды в консоль.
-Команды, введенные пользователем, отправляются на сервер для выполнения.
-Клиент принимает результат выполнения команд от сервера и выводит его в консоль.
-Клиент может продолжать вводить команды и получать результаты от сервера.



# Скриншоты работы программы:

[Сервер]
![image](https://github.com/SeVaSe/socket_server/assets/108822198/0c1703d0-f837-4eb8-ba91-ab26e529b4e7)


[Клиент]
![image](https://github.com/SeVaSe/socket_server/assets/108822198/1879f12e-07dc-4d7b-ac51-c7b78dc075c1)
