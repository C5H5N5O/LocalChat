from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA
from rsa import PrivateKey


class Coder():
    
    def encrypt(self, data, key):
        cipherrsa = PKCS1_OAEP.new(key)
        return cipherrsa.encrypt(data)


    def decrypt(self, data, key):
        cipherrsa = PKCS1_OAEP.new(key)
        return cipherrsa.decrypt(data)
        
        

    def check_out_signature(self, massage, signature_key, sig):
        myhash = SHA.new(massage)
        signature = PKCS1_v1_5.new(signature_key)
        return signature.verify(myhash, sig)


    def generate_keys(self):
        privtre_key = RSA.generate(2048)
        public_key = privtre_key.publickey()
        return privtre_key, public_key


    def sig_massage(massage, encript_signature_key):
        myhash = SHA.new(massage)
        signature = PKCS1_v1_5.new(encript_signature_key)
        signature = signature.sign(myhash)
        return signature