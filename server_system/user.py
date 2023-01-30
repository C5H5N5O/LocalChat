class User:

    def __init__(self, id, connection, decrypt_massage_key, encrypt_massage_key, decrypt_signature_key, server):
        
        self.id = id
        self.connection = connection

        self.encrypt_massage_key = encrypt_massage_key
        self.decrypt_signature_key = decrypt_signature_key
        self.decrypt_key = decrypt_massage_key
        self.server = server

    def listen(self):
        while True:
            try:
                data = self.server.Coder.decrypt(self.connection.recv(2048), self.decrypt_key)
                signature = self.server.Coder.decrypt(self.connection.recv(2048), self.decrypt_key)

                verified = self.server.Coder.check_out_signature(data, self.decrypt_signature_key, signature)
                if not verified: return
                    
                self.server.Handler.handle(data.decode("utf-8"))
            
            # если соедиенение разорвано клиент удаляется из активных клиентов  
            except ConnectionAbortedError:
                self.server.active_users.pop(id)


    def send_data(self, data):
        self.connection.send(self.server.Coder.encrypt(data, self.encrypt_massage_key))
        self.connection.send(self.server.Coder.encrypt(self.server.Coder.sig_massage(data, self.server.server_signature_encrypt_key), self.encrypt_massage_key))

