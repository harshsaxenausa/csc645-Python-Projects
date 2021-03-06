#######################################################################
# File:             server.py
# Author:           Jose Ortiz
# Purpose:          CSC645 Assigment #1 TCP socket programming
# Description:      Template server class. You are free to modify this
#                   file to meet your own needs. Additionally, you are
#                   free to drop this client class, and add yours instead.
# Running:          Python 2: python server.py
#                   Python 3: python3 server.py
#                   Note: Must run the server before the client.
########################################################################


from builtins import object
import socket
from threading import Thread
import pickle
from client_handler import ClientHandler


class Server(object):

    MAX_NUM_CONN = 10

    def __init__(self, ip_address='127.0.0.1', port=12005):
        """
        Class constructor
        :param ip_address:
        :param port:
        """
        # create an INET, STREAMing socket
        self.ip_address = ip_address
        self.port = port
        self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = {}
        self.chat_room = {}
        self.chat_room_owner = {}
        self.chat_room_messages = {}
        self.serversocket.bind((ip_address, port))


    def _listen(self):
        """
        Private method that puts the server in listening mode
        If successful, prints the string "Listening at <ip>/<port>"
        i.e "Listening at 127.0.0.1/10000"
        :return: VOID
        """
        #TODO: your code here
        try:
            self.serversocket.listen(self.MAX_NUM_CONN)
            print("Server running and listening at " + self.ip_address + "/" + str(self.port))
        except:
            self.serversocket.close()


    def _accept_clients(self):
        """
        Accept new clients
        :return: VOID
        """
        while True:
            try:
                clientsocket, address = self.serversocket.accept()
                Thread(target=self.client_handler_thread, args=(clientsocket, address)).start()
            except:
                #TODO: Handle exceptions
                self.serversocket.close()

    def send(self, clientsocket, data):
        """
        TODO: Serializes the data with pickle, and sends using the accepted client socket.
        :param clientsocket:
        :param data:
        :return:
        """
        serialized_data = pickle.dumps(data)
        clientsocket.send(serialized_data)


    def receive(self, clientsocket, MAX_BUFFER_SIZE=4096):
        """
        TODO: Deserializes the data with pickle
        :param clientsocket:
        :param MAX_BUFFER_SIZE:
        :return: the deserialized data
        """
        raw_data = clientsocket.recv(MAX_BUFFER_SIZE)
        data = pickle.loads(raw_data)
        return data

    def send_client_id(self, clientsocket, id):
        """
        Already implemented for you
        :param clientsocket:
        :return:
        """
        clientid = {'clientid': id}
        self.send(clientsocket, clientid)

    def client_handler_thread(self, clientsocket, address):
        """
        Sends the client id assigned to this clientsocket and
        Creates a new ClientHandler object
        See also ClientHandler Class
        :param clientsocket:
        :param address:
        :return: a client handler object.
        """

        #TODO: create a new client handler object and return it
        client_handler = ClientHandler(self, clientsocket, address)

        client_handler.send_client_id()
        client_handler.set_client_name()

        self.clients[client_handler.client_id] = client_handler

        print("Client {} with clientid: {} has connected to this server".format(client_handler.client_name, client_handler.client_id))

        client_handler.send_menu()

        while True:
            client_status = client_handler.process_options()
            if client_status == "CLIENT_DISCONNECTED":
                break


    def run(self):
        """
        Already implemented for you. Runs this client
        :return: VOID
        """
        self._listen()
        self._accept_clients()


if __name__ == '__main__':
    server = Server()
    server.run()

