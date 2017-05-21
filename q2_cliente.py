import socket                   # Import socket module

s = socket.socket()             # Create a socket object
host = socket.gethostname()     # Get local machine name
port = 5002                    # Reserve a port for your service.

s.connect((host, port))
s.send("Hello server!".encode('utf-8'))

with open('q2_download/received_file', 'wb') as f:
    print ('file opened')
    while True:
        print ('receiving data...')
        data = s.recv(1024)
        print('data=%s', (data))
        if not data:
            break
        # write data to a file
        f.write(data)

f.close()
print('Successfully get the file')
s.close()
print('connection closed')

'''
import socket

class Cliente():
    def __init__(self):
        self.HOST = '127.0.0.1'
        self.PORT = 5012
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.dest = (self.HOST, self.PORT)

    def receber(self, arq):
        self.tcp.connect(self.dest)
        f = open(arq, "wb")

        while True:
            arquivo = self.tcp.recv(1024)

            while arquivo:
                f.write(arquivo)
                arquivo = self.tcp.recv(1024)



def main():
    cliente = Cliente()
    arq = "q3_download/teste.pdf"

    cliente.receber(arq)
    cliente.tcp.close()

main()
'''
