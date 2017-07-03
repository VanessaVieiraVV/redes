import json
import socket

def recebe_arq(arq, tcp):
    with open(arq, 'wb') as f:
        while True:
            print ('receiving data...')
            data = tcp.recv(1024)
            print('data=%s', (data))
            if not data:
                break
            if data == b'FIM':
                break
            f.write(data)

    f.close()
    print('Concluido')


def get_users(fname):
    arq = open(fname, 'r')
    content = arq.read()
    arq.close()
    if not content.startswith('{'):
        data = json.loads('{}')

    else:
        with open(fname) as f:
            data = json.load(f)
        f.close()

    return data

def add_user(fname, username, password):
    success = False

    data = get_users(fname)

    if not username in data:
        data[username] = {'password' : password, 'pastas' : []}

        with open(fname, 'w') as f:
            json.dump(data, f)

        f.close()
        success = True

    return success

def new_pasta(fname, user, nome_pasta):
    data = get_users(fname)
    data[user]['pastas'].append(nome_pasta)

    with open(fname, 'w') as f:
        json.dump(data, f)

    f.close()

def autentication(fname, user, password):
    data = get_users(fname)
    if not user in data:
        return False
    elif data[user]['password'] == password:
        return True
    else:
        return False

def permission(fname, user, nome_pasta):
    data = get_users(fname)

    if not user in data:
        return False

    elif nome_pasta in data[user]['pastas']:
        return True

    else: return False

def get_pastas(fname, user):
    data = get_users(fname)

    pastas = data[user]['pastas']

    return pastas

def send_arq(arq, con):
    f = open(arq,'rb')
    l = f.read(1024)
    while (l):
        con.send(l)
        l = f.read(1024)
    f.close()

    print ('Arquivo enviado')
