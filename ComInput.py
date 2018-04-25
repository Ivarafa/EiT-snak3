# This Python file uses the following encoding: utf-8
import socketserver
import json



class Connection(socketserver.BaseRequestHandler):

    def handle(self):
        """
        This method handles the connection between a client and the server.
        """
        self.ip = self.client_address[0]
        self.port = self.client_address[1]
        self.connection = self.request
        global messages
        global lock

        while True:
            try:
                received_string = self.connection.recv(4096)
            except:
                # handles the errno-10054, might not be the best solution.
                # drops this BaseRequestHandler with finish() thats called after handle returns
                return
            try:
                received_json = json.loads(received_string.decode('UTF-8'))

                request = received_json["request"]
                content = received_json["content"]
                lock.acquire()
                messages.append([request,content])
                #print(messages)
                lock.release()
                self.connection.send(bytes(json.dumps({"status":"added"}),'UTF-8'))
            except ValueError:
                return



class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    """
    This class is present so that each client connected will be ran as a own
    thread. In that way, all clients will be served by the server.

    No alterations are necessary
    """
    allow_reuse_address = True

def run(mes, loc):
    global messages, lock
    lock = loc
    messages = mes
    HOST, PORT = "192.168.111.12",45006
    server = ThreadedTCPServer((HOST,PORT),Connection)
    server.serve_forever()

"192.168.100.111"
