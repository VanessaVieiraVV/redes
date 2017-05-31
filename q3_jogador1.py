import socket
import threading
from q3_jogo import Game, Game_client, Game_server

def main():
    game = Game()
    cliente = Game_client()
    servidor = Game_server()
    servidor.port = 5000
    cliente.port = 5001

    while True:
        if game.jogadas_disponiveis > 0:
            if game.jogador == 'X' :
                if game.jogadas_disponiveis == 9:
                    game.showBoard()
                    position = input("\nDIGITE UMA POSIÇÃO PARA JOGAR (1-9): ")
                    if not game.jogada(position):
                        while not game.jogada(position):
                            position = input("Posição já ocupada ")

                    game.jogadas1.append(position)
                    cliente.send_msg(position)
                    if game.ganhar(game.jogador):
                        game.showBoard()
                        print ('Jogador X ganhou')
                        break
                    #game.jogador = '0'
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
                    if not game.jogada(position):
                        while not game.jogada(position):
                            position = input("Posição já ocupada ")

                    game.jogadas1.append(position)
                    cliente.send_msg(position)
                    game.showBoard()
                    if game.ganhar(game.jogador):
                        print ('Jogador X ganhou')
                        break
                    #game.jogador = '0'


        if game.jogadas_disponiveis == 0:
            print("Deu velha")
            break

    cliente.close_connection()
    servidor.close_connection()

if __name__ == '__main__':
    main()
