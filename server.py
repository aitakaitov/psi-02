import socket
from sys import argv
from threading import Thread
import time


def main():
    if len(argv) != 2:
        print('Usage: <port>')
        exit()
    else:
        port = argv[1]

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("", int(port)))
        sock.listen()
        while True:
            conn, addr = sock.accept()
            thread = Thread(target=serve_connection, args=[conn])
            thread.start()


def serve_connection(connection: socket):
    with connection:
        # we need to deal with the fact that recv is blocking and can block on no more data sent, but the
        # connection would remain open so we would get stuck
        data = recv_timeout(connection)
        # the side effect of the above function
        if len(data) == 0:
            return
        # debug
        print('Received data')
        print(data.decode('utf-8'))

        # check if the request is HTTP/1.1 GET
        if not is_get(data):
            send_error(connection)
        else:
            send_ok(connection)


def recv_timeout(connection, timeout=2):
    # set the connection to non-blocking
    connection.setblocking(False)

    # to piece together the data
    complete_data = b''
    data = b''

    begin = time.time()
    while True:
        # if we have some data, then we break after some time
        if complete_data and time.time() - begin > timeout:
            break

        # if we have no data, we wait a little longer
        elif time.time() - begin > timeout * 2:
            break

        try:
            # we receive as much as we can
            data = connection.recv(8192)
            # if we receive something
            if data:
                # we append it
                complete_data += data
                # and change the beginning time for measurement
                begin = time.time()
            else:
                # otherwise we wait a little and repeat
                time.sleep(0.1)
        except:
            pass

    return complete_data


def is_get(data):
    split_data = data.decode('utf-8').split()
    method = split_data[0]
    http = split_data[2]

    if method != 'GET' or http != 'HTTP/1.1':
        return False
    else:
        return True


def send_error(connection):
    connection.sendall(b'HTTP/1.1 403 Forbidden')
    print('Sent 403')


def send_ok(connection):
    # construct OK header
    ok_html = b'<html><body><b>200 OK</b></body></html>'
    connection.sendall(b'HTTP/1.1 200 OK\n' +
                       b'Content-Type: text/html\n' +
                       b'Content-Length: ' + str(len(ok_html)).encode('utf-8') + b'\n' +
                       b'\n')
    connection.sendall(b'<html><body><b>200 OK</b></body></html>')
    print('Sent 200')


if __name__ == '__main__':
    main()
