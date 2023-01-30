from email.headerregistry import ContentTransferEncodingHeader
from rsa import encrypt
from coder import Coder
from database_reader import DB
from request_handler import RequestHendler
from user import User
import socket, threading

from Crypto.PublicKey import RSA

class Server():
    


    def __init__(self, host, port, database_path):
        
        print("creating server")

        self.HOST = host
        self.PORT = port
        self.database_path = database_path

        self.s = socket.socket()

        print("connecting to the database")
        self.DataBase = DB(self.database_path)
        print("[ok] succesfully connected to the database")

        self.Coder = Coder()
        self.Handler = RequestHendler()

        self.active_clients = {
            #key: id, value: object
            
        }
        self.server_signature_encrypt_key, self.server_signature_decrpt_key = self.Coder.generate_keys()

        print("[ok] server created")

    def start_server(self):
        print("starting server...")
        self.s.bind((self.HOST, self.PORT))
        self.s.listen()

        print("SERVER STARTED")
        print(f"IP - {self.HOST}:{self.PORT}")


    def listen_connections(self):
        while True:

            connection, addr = self.s.accept()
            print(f"new user connected   IP: {addr}]")
            self.create_new_connection(connection, addr)


    def create_new_connection(self, connection, addr):

        # генерируется и отправляется публичный ключ
        users_massage_decription_key, users_massage_incription_key = self.Coder.generate_keys()
        
        # отправка клиенту ключа шифрования сообщений для сервера и ключа дешифрования подписи сервера
        connection.send(users_massage_incription_key.export_key("PEM"))
        #connection.send(self.server_signature_decrpt_key.export_key("PEM"))
        
        # получение ключеней шифрования сообщений для клиента и дешифрования его подписи
        #signature_decrypt_key = RSA.import_key(connection.recv(2048))
        encrypt_massage_for_user_key = RSA.import_key(connection.recv(2048))

        # проверка клиента
        for _ in range(3):
            login = self.Coder.decrypt(connection.recv(2048), users_massage_decription_key)
            password = self.Coder.decrypt(connection.recv(2048), users_massage_decription_key)
            
            #signature = self.Coder.decrypt(connection.recv(2048), users_massage_decription_key)
            #singnature_correctness = self.Coder.check_out_signature(login_password, signature_decrypt_key, signature)

            
            id = DB.check_user_password(login.decode("utf-8"), password.decode("utf-8"))
            #id = "TEST"
            #if not singnature_correctness:
            #    connection.close()
            #    return
                
            if not id:
                connection.send(self.Coder.encrypt("SERVER: incorrect login/password".encode("utf-8"), encrypt_massage_for_user_key))
                continue

            connection.send(self.Coder.encrypt("SERVER: login successful".encode("utf-8"), encrypt_massage_for_user_key))

            break
        
        # если после трёх попыток вход не был выполнен, соединение сбрасывается
        if not id:
            connection.close()
            return

        user = User(id, connection, users_massage_decription_key, encrypt_massage_for_user_key, self)  #TODO signature, decrypt signature key
        self.active_clients[id] = user

        print(f"new user added to list with id={id}")

        threading.Thread(target=user.listen,).start()



if __name__ == "__main__":
    server = Server(socket.gethostbyname(socket.gethostname()), 12333, "PATH TO DATABASE")
    server.start_server()

    threading.Thread(target=server.listen_connections,).start()