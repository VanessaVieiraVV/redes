import socket
import json
from q2_servidor import send_arq
import time
from q2_functions import *

def send_user(tcp):
    data = dict()

    user = input('username: ')
    password = input('password: ')

    data['user'] = user
    data['password'] = password

    juser = json.dumps(data)

    tcp.send(juser.encode('utf-8'))

def send_pasta(tcp):
    data = dict()

    nome_pasta = input('nome da pasta: ')

    data['pasta'] = nome_pasta

    jpasta = json.dumps(data)

    tcp.send(jpasta.encode('utf-8'))

def send_arquivo(tcp):
    data = dict()

    nome_pasta = input('nome da pasta: ')
    nome_arq = input('nome arquivo: ')
    diretorio = input('diretorio do arquivo: ')

    data['nome_arq'] = nome_arq
    data['pasta'] = nome_pasta

    jinfo = json.dumps(data)

    tcp.send(jinfo.encode('utf-8'))

    while True:
        conf = tcp.recv(1024)

        if conf.decode('utf-8') == 'OK':
            send_arq(diretorio, tcp)
            time.sleep(0.2)
            tcp.send('FIM'.encode('utf-8'))
            break

        elif conf.decode('utf-8') == 'NO':
            print ('Access Denied')
            break

def get_arquivo(tcp):
    data = dict()

    nome_pasta = input('nome da pasta: ')
    nome_arq = input('nome arquivo: ')
    diretorio = input('diretorio de destino: ')

    data['nome_arq'] = nome_arq
    data['pasta'] = nome_pasta

    jinfo = json.dumps(data)

    tcp.send(jinfo.encode('utf-8'))

    while True:
        conf = tcp.recv(1024)

        if conf.decode('utf-8') == 'OK':
            recebe_arq((diretorio + '/' + nome_arq), tcp)
            break

        elif conf.decode('utf-8') == 'NO':
            print ('Access Denied')
            break

def show_info(tcp):
    while True:
        msg = tcp.recv(1024)
        if msg.decode('utf-8').startswith('{'):
            break

    info = msg.decode('utf-8')
    jinfo = json.loads(info)

    print ('Pastas: ')
    for pasta in jinfo['pastas']:
        print(pasta)

    print ('Arquivos: ')
    for arquivo in jinfo['arquivos']:
        print (arquivo)


def send_novo_user(tcp):
    data = dict()

    nome_pasta = input('nome da pasta: ')
    novo_user = input('nome do usuario: ')

    data['pasta'] = nome_pasta
    data['novo_user'] = novo_user

    jinfo = json.dumps(data)

    tcp.send(jinfo.encode('utf-8'))

    while True:
        conf = tcp.recv(1024)

        if conf.decode('utf-8') == 'OK':
            print ('Shared')
            break

        elif conf.decode('utf-8') == 'NO':
            print ('Access Denied')
            break


def main():
    logged = False
    user = ''

    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 5006

    tcp.connect((host, port))

    print ('Para sair use CTRL+X\n')
    msg = input('DIGITE COMANDO: ')

    while msg != '\x18':
        if msg == 'NEW USER':
            tcp.send(msg.encode('utf-8'))

            resp = tcp.recv(1024)
            if resp.decode('utf-8') == 'OK':
                send_user(tcp)
                msg = input('DIGITE COMANDO: ')
            else: msg = input('DIGITE COMANDO: ')

        elif msg == 'LOGIN':
            if logged == True:
                print('Already Logged in as ', user)
                msg = input('DIGITE COMANDO: ')

            else:
                tcp.send(msg.encode('utf-8'))

                resp = tcp.recv(1024)
                if resp.decode('utf-8') == 'OK':
                    send_user(tcp)
                    resposta = tcp.recv(1024)
                    print (resposta.decode('utf-8'))

                    if not resposta.decode('utf-8') == 'ERROR':
                        logged = True
                        user = resposta[13:]

                    msg = input('DIGITE COMANDO: ')

        elif msg == 'NEW PASTA':
            tcp.send(msg.encode('utf-8'))

            resp = tcp.recv(1024)
            if resp.decode('utf-8') == 'OK':
                send_pasta(tcp)

            msg = input('DIGITE COMANDO: ')

        elif msg == 'UPLOAD':
            tcp.send(msg.encode('utf-8'))

            resp = tcp.recv(1024)
            if resp.decode('utf-8') == 'OK':
                send_arquivo(tcp)

            msg = input('DIGITE COMANDO: ')

        elif msg == 'DOWNLOAD':
            tcp.send(msg.encode('utf-8'))

            resp = tcp.recv(1024)
            if resp.decode('utf-8') == 'OK':
                get_arquivo(tcp)

            msg = input('DIGITE COMANDO: ')

        elif msg == 'SHARE':
            tcp.send(msg.encode('utf-8'))

            resp = tcp.recv(1024)
            if resp.decode('utf-8') == 'OK':
                send_novo_user(tcp)

            msg = input('DIGITE COMANDO: ')

        elif msg == 'LOGOUT':
            tcp.send(msg.encode('utf-8'))
            logged = False
            user = ''
            print ('Logged out')
            msg = input('DIGITE COMANDO: ')

        elif msg == 'INFO':
            if logged == False:
                print('Not logged in')
                msg = input('DIGITE COMANDO: ')

            else:
                tcp.send(msg.encode('utf-8'))

                resp = tcp.recv(1024)
                if resp.decode('utf-8') == 'OK':
                    show_info(tcp)

                msg = input('DIGITE COMANDO: ')

        elif msg == 'DISCONNECT':
            tcp.send(msg.encode('utf-8'))
            time.sleep(0.1)
            tcp.close()
            break

        else:
            print('Comando inválido')
            msg = input('DIGITE COMANDO: ')


if __name__ == '__main__':
    main()
