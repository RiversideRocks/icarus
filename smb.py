import socket
from abuseipdb import snmpabuseipdb


def runsmb():
    s = socket.socket()
    host = '0.0.0.0'
    port = 445
    s.bind((host, port))
    s.listen()

    conn, addr = s.accept()
    print(conn)
    print(addr)

    while 1:
        data = conn.recv(1024)
        if not data: break
        print(data)

    conn.close()

runsmb()