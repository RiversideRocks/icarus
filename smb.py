import socketserver # https://docs.python.org/3.5/library/socketserver.html
from abuseipdb import hackingabuseipdb
from memoryfile import lastattacker
import logging


class MyTCPHandler(socketserver.BaseRequestHandler):
    def handle(self):
        # self.request is the TCP socket connected to the client
        #self.data = self.request.recv(1024).strip()
        hackingabuseipdb(self.client_address[0])  # From abuseipdb.py
        lastattacker(self.client_address[0])  # From memoryfile.py


def runsmb():
    try:
        HOST, PORT = "0.0.0.0", 445
        server = socketserver.TCPServer((HOST, PORT), MyTCPHandler)
        server.allow_reuse_address = True
        server.serve_forever()

    except BaseException as e:  # should be more specific.
        logging.basicConfig(filename='logs.txt')
        logging.info(e)
