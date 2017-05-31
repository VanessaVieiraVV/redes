import socket

def get_protocol(arq):
    f = open(arq, "r")
    protocolo = f.readline()
    f.close()
    return protocolo

def echo(protocolo):
    if protocolo == "UDP\n":
        HOST = ''
        PORT = 5001
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        orig = (HOST, PORT)
        udp.bind(orig)
        while True:
            msg, cliente = udp.recvfrom(1024)
            print (cliente, msg.decode('utf-8'))

            if msg:
                sent = udp.sendto(msg, cliente)

        udp.close()

    elif protocolo == "TCP\n":
        HOST = ''
        PORT = 5001
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (HOST, PORT)
        tcp.bind(orig)
        tcp.listen(1)
        while True:
            con, cliente = tcp.accept()
            print ('Concetado por', cliente)

            while True:
                msg = con.recv(1024)
                print (cliente, msg.decode('utf-8'))

                if msg:
                    con.send(msg)
                else: break

            print ('Finalizando conexao do cliente', cliente)
            con.close()

def main():
    protocol = get_protocol('q1_protocolo.txt')
    print ("protocolo:", protocol)
    echo(protocol)

if __name__ == '__main__':
    main()
