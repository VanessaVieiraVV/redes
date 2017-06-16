import socket
import json
import os
from q2_functions import *
import time


data_file = 'json.txt'
dir_pastas = 'q2_pastas'

def get_jinfo(con):
    while True:
        msg = con.recv(1024)
        if msg.decode('utf-8').startswith('{'):
            break

    info = msg.decode('utf-8')
    jinfo = json.loads(info)

    return jinfo

def send_arq(arq, con):
    f = open(arq,'rb')
    l = f.read(1024)
    while (l):
        con.send(l)
        #print('Sent ',repr(l))
        l = f.read(1024)
    f.close()

    print ('Arquivo enviado')
    #con.close()

def new_user(con):
    con.send('OK'.encode('utf-8'))

    jinfo = get_jinfo(con)

    user = jinfo['user']
    password = jinfo['password']

    return add_user(data_file, user, password)

def user_login(con):
    con.send('OK'.encode('utf-8'))

    jinfo = get_jinfo(con)

    user = jinfo['user']
    password = jinfo['password']

    return [autentication(data_file, user, password), user]

def criar_pasta(con, user):
    con.send('OK'.encode('utf-8'))

    jinfo = get_jinfo(con)

    nome_pasta = jinfo['pasta']

    os.mkdir(dir_pastas + '/' + nome_pasta)
    new_pasta(data_file, user, nome_pasta)

def compartilha_pasta(con, user):
    con.send('OK'.encode('utf-8'))

    jinfo = get_jinfo(con)

    novo_user = jinfo['novo_user']
    nome_pasta = jinfo['pasta']

    if permission(data_file, user, nome_pasta) == True:
        con.send('OK'.encode('utf-8'))
        new_pasta(data_file, novo_user, nome_pasta)

    else: con.send('NO'.encode('utf-8'))

def rec_upload(con, user):
    con.send('OK'.encode('utf-8'))
    jinfo = get_jinfo(con)

    nome_arq = jinfo['nome_arq']
    nome_pasta = jinfo['pasta']

    if permission(data_file, user, nome_pasta) == True:
        con.send('OK'.encode('utf-8'))
        recebe_arq((dir_pastas + '/' + nome_pasta + '/' + nome_arq), con)

    else: con.send('NO'.encode('utf-8'))

def do_download(con, user):
    con.send('OK'.encode('utf-8'))
    jinfo = get_jinfo(con)

    nome_arq = jinfo['nome_arq']
    nome_pasta = jinfo['pasta']

    if permission(data_file, user, nome_pasta) == True:
        con.send('OK'.encode('utf-8'))
        time.sleep(0.2)
        send_arq((dir_pastas + '/' + nome_pasta + '/' + nome_arq), con)

        time.sleep(0.2)
        con.send('FIM'.encode('utf-8'))

    else: con.send('NO'.encode('utf-8'))

def main():
    logged = False
    user = ''

    port = 5001
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    tcp.bind((host, port))
    tcp.listen(5)
    print ('Server listening....')

    while True:
        con, addr = tcp.accept()
        print ('Got connection from', addr)

        #con.send('string'.encode('utf-8'))

        while True:
            msg = con.recv(1024)
            print (msg.decode('utf-8'))

            if msg.decode('utf-8') == 'NEW USER':
                new_user(con)

            elif msg.decode('utf-8') == 'LOGIN':
                login_info = user_login(con)
                if login_info[0] == True:
                    logged = True
                    user = login_info[1]
                    resposta = 'Logged in as ' + user

                else : resposta = 'ERROR'

                con.send(resposta.encode('utf-8'))

            elif msg.decode('utf-8') == 'NEW PASTA':
                criar_pasta(con, user)

            elif msg.decode('utf-8') == 'UPLOAD':
                rec_upload(con, user)

            elif msg.decode('utf-8') == 'DOWNLOAD':
                do_download(con, user)

            elif msg.decode('utf-8') == 'SHARE':
                compartilha_pasta(con, user)

            elif msg.decode('utf-8') == 'LOGOUT':
                logged = False
                user = ''

            elif msg.decode('utf-8') == 'DISCONNECT':
                con.close()

if __name__ == '__main__':
    main()
