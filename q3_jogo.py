import threading
import socket

class Game():
    def __init__(self):
        self.board = [
        [['1', '_'], ['2', '_'], ['3', '_']],
        [['4', '_'], ['5', '_'], ['6', '_']],
        [['7', '_'], ['8', '_'], ['9', '_']],
        ]

        self.jogador = 'X'

        self.jogadas_disponiveis = 9

        self.jogadas1 = []
        self.jogadas2 = []


    def showBoard(self):
        print('\n')
        for linha in self.board:
            print(' ', linha[0][1], '|', linha[1][1], '|', linha[2][1])
            if not linha == self.board[2]:
                print ('-------------')
        print ('\n')


    def jogada(self, posicao):
        success = False

        for linha in self.board:
            for position in linha:
                if position[0] == posicao:
                    if position[1] == '_':
                        position[1] = self.jogador
                        self.jogadas_disponiveis -= 1
                        success = True
                        break

                    else:
                        break

                else: continue
        return success


    def ganhar(self, jogador):
        ganhou = False

        ganho = [
          ['1', '2', '3'],
          ['4', '5', '6'],
          ['7', '8', '9'],
          ['1', '4', '7'],
          ['2', '5', '8'],
          ['3', '6', '9'],
          ['3', '5', '7'],
          ['1', '5', '9']
        ]

        if jogador == 'X':
            for possib in ganho:
                if (possib[0] in self.jogadas1) and (possib[1] in self.jogadas1) and (possib[2] in self.jogadas1):
                    ganhou = True

        else:
            for possib in ganho:
                if (possib[0] in self.jogadas2) and (possib[1] in self.jogadas2) and (possib[2] in self.jogadas2):
                    ganhou = True

        return ganhou

class Game_client():
    def __init__(self):
        self.host = '127.0.0.1'
        self.port = 0
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.dest = (self.host, self.port)

    def send_msg(self, msg):
        self.dest = (self.host, self.port)
        self.udp.sendto (msg.encode('utf-8'), self.dest)

    def close_connection(self):
        self.udp.close()


class Game_server():
    def __init__(self):
        self.host = ''              # Endereco IP do Servidor
        self.port = 1           # Porta que o Servidor esta
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.orig = (self.host, self.port)

    def listen(self):
        self.orig = (self.host, self.port)
        while True:
            msg, cliente = self.udp.recvfrom(1024)
            if msg: break

        return msg.decode('utf-8')

    def close_connection(self):
        self.udp.close()
