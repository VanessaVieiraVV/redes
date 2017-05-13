import socket
import threading
from q3_jogo import Game

class Game_client(threading.Thread):
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 6061
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (self.host, self.port)

    def send_msg(self, msg):
        self.udp.sendto (msg.encode('utf-8'), self.dest)

    def close_connection(self):
        self.udp.close()


class Game_server(threading.Thread):
    def __init__(self):
        self.host = ''              # Endereco IP do Servidor
        self.port = 6060           # Porta que o Servidor esta
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.orig = (self.host, self.port)

    def listen(self):
        while True:
            msg, cliente = self.udp.recvfrom(1024)
            if msg: break

        return msg.decode('utf-8')

    def close_connection(self):
        self.udp.close()

def main():
    game = Game()
    cliente = Game_client()
    servidor = Game_server()
    game.jogador = '0'

    while True:
        if game.jogadas_disponiveis > 0:
            if game.jogador == '0':
                if game.jogadas_disponiveis == 9:
                    servidor.udp.bind(servidor.orig)
                position_ant = servidor.listen()
                game.jogador = 'X'
                game.jogada(position_ant)
                game.jogadas1.append(position_ant)

                if game.ganhar(game.jogador):
                    game.showBoard()
                    print ('Jogador X ganhou')
                    break

                game.jogador = '0'
                game.showBoard()

                if game.jogadas_disponiveis  == 0:
                    print("Deu velha")
                    break

                position = input("\nDIGITE UMA POSIÇÃO PARA JOGAR (1-9): ")
                if not game.jogada(position):
                    while not game.jogada(position):
                        position = input("Posição já ocupada\n")

                game.jogadas2.append(position)
                cliente.send_msg(position)
                game.showBoard()
                if game.ganhar(game.jogador):
                    print('Jogador 0 ganhou')
                    break
                #game.jogador = 'X'

        if game.jogadas_disponiveis == 0:
            print("Deu velha")
            break

main()
