import SocketServer
import json


class RuleTCPServer(SocketServer.ThreadingTCPServer):
    allow_reuse_address = True


class RuleTCPServerHandler(SocketServer.BaseRequestHandler):
    def handle(self):
        try:
            data = json.loads(self.request.recv(1024).strip())

            print data

            self.request.sendall(json.dumps({'return':'ok'}))
        except Exception, e:
            print "Exception while receiving messsage:", e

server = RuleTCPServer(('127.0.0.1', 13373), RuleTCPServerHandler)
server.serve_forever()
