import socketserver


class snmpd(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request[0].strip()
        socket = self.request[1]
        print (self.client_address[0])
  #      print (data)
#        socket.sendto("bob", self.client_address)


if __name__ == "__main__":
    HOST, PORT = "0.0.0.0", 161
    with socketserver.UDPServer((HOST, PORT), snmpd) as server:
        server.serve_forever()