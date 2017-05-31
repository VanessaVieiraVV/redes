import socket

def send_arq(arq, tcp):
    while True:
        conn, addr = tcp.accept()
        print ('Got connection from', addr)

        f = open(arq,'rb')
        l = f.read(1024)
        while (l):
           conn.send(l)
           #print('Sent ',repr(l))
           l = f.read(1024)
        f.close()

        print ('Arquivo enviado')
        conn.close()

def main():
    print ('Server listening....')
    port = 5000
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    tcp.bind((host, port))
    tcp.listen(5)

    arq = 'q2_upload/wireshark_HTTP2.pdf'
    send_arq(arq, tcp)

if __name__ == '__main__':
    main()
