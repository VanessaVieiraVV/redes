import socket

def get_protocol(arq):
    f = open(arq, "r")
    protocolo = f.readline()
    f.close()
    return protocolo

def echo(protocolo):
    if protocolo == "UDP\n":
        HOST = ''              # Endereco IP do Servidor
        PORT = 5001           # Porta que o Servidor esta
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
        HOST = ''              # Endereco IP do Servidor
        PORT = 5001            # Porta que o Servidor esta
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

main()
