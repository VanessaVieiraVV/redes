import socket

def get_protocol(arq):
    f = open(arq, "r")
    protocolo = f.readline()
    f.close()
    return protocolo

def echo(protocolo):
    if protocolo == "UDP\n":
        HOST = '127.0.0.1'  # Endereco IP do Servidor
        PORT = 5001           # Porta que o Servidor esta
        udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        dest = (HOST, PORT)
        print ('Para sair use CTRL+X\n')
        msg = input()

        while msg != '\x18':
            udp.sendto (msg.encode('utf-8'), dest)

            resp, server = udp.recvfrom(1024)
            print (server, resp.decode('utf-8'))

            msg = input()

        udp.close()


    if protocolo == "TCP\n":
        HOST = '127.0.0.1'     # Endereco IP do Servidor
        PORT = 5001            # Porta que o Servidor esta
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        dest = (HOST, PORT)
        tcp.connect(dest)
        print ('Para sair use CTRL+X\n')
        msg = input()
        while msg != '\x18':
            tcp.send(msg.encode('utf-8'))


            resp = tcp.recv(1024)
            print (dest, resp.decode('utf-8'))

            msg = input()

        tcp.close()

def main():
    protocol = get_protocol('q1_protocolo.txt')
    print ("protocolo:", protocol)
    echo(protocol)

main()
