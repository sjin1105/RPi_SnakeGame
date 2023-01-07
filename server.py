import os
import socket

IP = ''
PORT = 5000

id_pw = []

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 5)
s.bind((IP, PORT))
s.listen(True)
conn, addr = s.accept()
while True:
    os.system('clear')
    print(id_pw)
    option = conn.recv(1024).decode()
    print(option)
    if option == 'login':
        login = conn.recv(1024).decode()
        print(login)
        if login in id_pw:
            conn.sendall('True'.encode('utf-8'))
        else:
            conn.sendall('False'.encode('utf-8'))
    if option == 'register':
        register = conn.recv(1024).decode()
        print(register)
        id_pw.append(register)
        id_pw = list(set(id_pw))
        print(id_pw)
        conn.sendall('True'.encode('utf-8'))
    if option == 'get':
        conn.sendall(str(id_pw).encode('utf-8'))
        
s.close()