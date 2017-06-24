import socket
import http.server
import socketserver
import json

class POST_Handler(http.server.BaseHTTPRequestHandler):

    def do_POST(self):
        content_len = int(self.headers.get_all('content-length')[0])
        post_body = self.rfile.read(content_len)
        self.send_response(200)
        self.end_headers()

        data = json.loads(post_body.decode())
        print(data['msg'])

        self.wfile.write(data['msg'].encode())
        return


def get_protocol(arq):
    f = open(arq, "r")
    protocolo = f.readline()
    f.close()
    return protocolo

def echo(protocolo):
    if protocolo == "UDP\n":
        HOST = ''
        PORT = 5000
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

    elif protocolo == 'HTTP\n':
        PORT = 8000
        HOST = 'localhost'

        server = socketserver.TCPServer((HOST, PORT), POST_Handler)
        print ('Starting server....')
        server.serve_forever()


def main():
    protocol = get_protocol('q1_protocolo.txt')
    print ("protocolo:", protocol)
    echo(protocol)

if __name__ == '__main__':
    main()
