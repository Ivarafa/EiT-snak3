# This Python file uses the following encoding: utf-8

import socket
import json
import threading
from time import sleep

class Client:
    '''
    This is the chat client class
    '''

    def __init__(self, host, server_port):
        '''
        This method is run when creating a new Client object
        '''
        self.valid_reqs = ['login', 'logout', 'msg', 'names', 'help']
        self.host = host
        self.server_port = server_port
        self.connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.run()

    def run(self):
        # Initiate the connection to the server
        self.connection.connect((self.host, self.server_port))
        # Setup and start a daemon-reciever thread
        recieve_thread = threading.Thread(target=self.receive_message)
        recieve_thread.setDaemon(True)
        recieve_thread.start()
        # And a daemon-sender thread
        send_thread = threading.Thread(target=self.send_message)
        send_thread.setDaemon(True)
        send_thread.start()
        while 1:
            # Let client send payloads
            #self.send_payload()
            pass
    '''
    def disconnect(self):
        # close() releases the resource associated with a connection but does not necessarily close the connection
        # immediately. If you want to close the connection in a timely fashion, call shutdown() before close(). - python docs.
        self.connection.shutdown()
        self.connection.close()
    '''
    def receive_message(self):
        while 1:
            message = self.connection.recv(4096)
            #print message
            try:
                received_json = json.loads(message.decode('UTF-8'))
                print(received_json)

            except ValueError:
                return

    def send_message(self):
        while 1:
            req = input("Command: ")
            message_to_send = {'request': req, 'content': None}
            print(message_to_send)
            self.connection.send(bytes(json.dumps(message_to_send), 'UTF-8'))
            # Let the console have time to output response from server, find better solution?
            sleep(0.5)

if __name__ == '__main__':
    '''
    This is the main method and is executed when you type 'python Client.py'
    in your terminal.

    No alterations are necessary
    '''
    client = Client("localhost", 9998)