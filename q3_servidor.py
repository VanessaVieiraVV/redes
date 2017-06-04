import socket
import json

def get_info_peer(cliente):
    peer = dict()

    peer['ip'] = cliente[0]
    peer['port'] = cliente[1]+1
    peer['rec_port'] = 0

    return peer


def get_rec_port(cliente, peer):
    peer['rec_port'] = cliente[1]+1

    jpeer = json.dumps(peer)

    return jpeer.encode('utf-8')


def send_peer(data, udp, cliente):
    return udp.sendto(data, cliente)

def main():
    host = ''
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port = 6007
    orig = (host, port)
    udp.bind(orig)

    while True:
        msg, cliente = udp.recvfrom(1024)
        if msg.decode('utf-8') == 'Hello':
            con1 = get_info_peer(cliente)
            udp.sendto('ok'.encode('utf-8'), cliente)
            print (cliente, msg.decode('utf-8'))

        while True:
            msg2, cliente2 = udp.recvfrom(1024)
            if msg2.decode('utf-8') == 'Hello':
                con2 = get_info_peer(cliente2)
                udp.sendto('ok'.encode('utf-8'), cliente2)
                print (cliente2, msg2.decode('utf-8'))

                break

        jpeer1 = get_rec_port(cliente, con2)
        jpeer2 = get_rec_port(cliente2, con1)

        send_peer(jpeer2, udp, cliente2)
        send_peer(jpeer1, udp, cliente)

    udp.close()

if __name__ == '__main__':
    main()
