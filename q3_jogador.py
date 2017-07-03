import socket
from q3_jogo import Game, Game_client, Game_server, Connection

posicoes = '''

      1 | 2 | 3
    -------------
      4 | 5 | 6
    -------------
      7 | 8 | 9

'''

def valida(posicao):
    validade = False
    if posicao.isdigit():
        if 0 < int(posicao) < 10:
            validade = True

    return validade

def do_jogo_X(game, cliente, servidor):
    while True:
        if game.jogador == 'X':
            if game.jogadas_disponiveis > 0:
                if game.jogadas_disponiveis == 9:
                    game.showBoard()
                    position = input("\nDIGITE UMA POSIÇÃO PARA JOGAR (1-9): ")

                    while not valida(position):
                        position = input("Posição Inválida ")
                    if not game.jogada(position):
                        while not game.jogada(position):
                            position = input("Posição já ocupada ")

                    game.jogadas1.append(position)
                    cliente.send_msg(position)
                    game.showBoard()
                    if game.ganhar(game.jogador):
                        game.showBoard()
                        print ('Jogador X ganhou')
                        break

                else:
                    if game.jogadas_disponiveis == 8:
                        servidor.orig = (servidor.host, servidor.port)
                        servidor.udp.bind(servidor.orig)

                    position_ant = servidor.listen()
                    game.jogador = '0'
                    game.jogada(position_ant)
                    game.jogadas2.append(position_ant)

                    if game.ganhar(game.jogador):
                        game.showBoard()
                        print ('Jogador 0 ganhou')
                        break

                    game.jogador = 'X'

                    game.showBoard()
                    position = input("\nDIGITE UMA POSIÇÃO PARA JOGAR (1-9): ")
                    while not valida(position):
                        position = input("Posição Inválida ")

                    if not game.jogada(position):
                        while not game.jogada(position):
                            position = input("Posição já ocupada ")

                    game.jogadas1.append(position)
                    cliente.send_msg(position)
                    game.showBoard()
                    if game.ganhar(game.jogador):
                        print ('Jogador X ganhou')
                        break

def do_jogo_0(game, cliente, servidor):
    while True:
        if game.jogador == '0':
            if game.jogadas_disponiveis > 0:
                if game.jogador == '0':
                    if game.jogadas_disponiveis == 9:
                        servidor.orig = (servidor.host, servidor.port)
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
                    while not valida(position):
                        position = input("Posição Inválida ")

                    if not game.jogada(position):
                        while not game.jogada(position):
                            position = input("Posição já ocupada\n")

                    game.jogadas2.append(position)
                    cliente.send_msg(position)
                    game.showBoard()
                    if game.ganhar(game.jogador):
                        print('Jogador 0 ganhou')
                        break



        if game.jogadas_disponiveis == 0:
            print("Deu velha")
            break


def main():
    print(posicoes)

    game = Game()
    cliente = Game_client()
    servidor = Game_server()
    con = Connection()
    peer = con.get_peer()
    servidor.port = peer['rec_port']
    cliente.port = peer['port']
    cliente.host = peer['ip']
    game.jogador = peer['jogador']

    if game.jogador == 'X':
        do_jogo_X(game, cliente, servidor)

    elif game.jogador == '0':
        do_jogo_0(game, cliente, servidor)



    cliente.close_connection()
    servidor.close_connection()

if __name__ == '__main__':
    main()
