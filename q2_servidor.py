import socket                   # Import socket module

port = 5002                   # Reserve a port for your service.
s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
s.bind((host, port))            # Bind to the port
s.listen(5)                     # Now wait for client connection.

print ('Server listening....')

while True:
    conn, addr = s.accept()     # Establish connection with client.
    print ('Got connection from', addr)
    data = conn.recv(1024)
    print ('Server received', repr(data))

    filename = 'q2_upload/wireshark_HTTP2.pdf'
    f = open(filename,'rb')
    l = f.read(1024)
    while (l):
       conn.send(l)
       print('Sent ',repr(l))
       l = f.read(1024)
    f.close()

    print ('Done sending')
    conn.send('Thank you for connecting'.encode('utf-8'))
    conn.close()

'''
import socket

class Servidor():
    def __init__(self):
        self.HOST = ''              # Endereco IP do Servidor
        self.PORT = 5012            # Porta que o Servidor esta
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.orig = (self.HOST, self.PORT)

    def enviar(self, arq):
        self.tcp.bind(self.orig)
        self.tcp.listen(10)
        f = open(arq, "rb")
        arquivo = f.read(1024)
        while True:
            con, cliente = self.tcp.accept()
            print ('Concetado por', cliente)

            while arquivo:
                con.send(arquivo)
                arquivo = f.read(1024)
                #print (cliente, msg.decode('utf-8'))

            print ('Finalizando conexao do cliente', cliente)
            con.close()


def main():
    server = Servidor()
    arq = "q3_upload/wireshark_HTTP2.pdf"

    server.enviar(arq)

main()
'''
