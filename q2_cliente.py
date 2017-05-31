import socket

def recebe_arq(arq, tcp):
    with open(arq, 'wb') as f:
        while True:
            print ('receiving data...')
            data = tcp.recv(1024)
            print('data=%s', (data))
            if not data:
                break
            f.write(data)

    f.close()
    print('Download concluido')


def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 5000

    tcp.connect((host, port))

    arq = 'q2_download/received_file'
    recebe_arq(arq, tcp)

    tcp.close()
    print('connection closed')

if __name__ == '__main__':
    main()
