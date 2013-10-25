import socket
import simplejson


class Client():
    def __init__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.connect(('127.0.0.1', 13373))

    def send(self, json_message):
        self.s.send(simplejson.dumps(json_message))

        result = simplejson.loads(self.s.recv(10000))

        self.s.close()

        return result