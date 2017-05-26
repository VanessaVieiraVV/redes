import socket

def recebe_arq(arq, s):
    with open(arq, 'wb') as f:
        print ('file opened')
        while True:
            print ('receiving data...')
            data = s.recv(1024)
            print('data=%s', (data))
            if not data:
                break
            f.write(data)

    f.close()
    print('Successfully get the file')


def main():
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 5000

    tcp.connect((host, port))
    tcp.send("Hello server!".encode('utf-8'))

    arq = 'q2_download/received_file'
    recebe_arq(arq, tcp)

    tcp.close()
    print('connection closed')

if __name__ == '__main__':
    main()
