from Protocols.RSA import GenKeyPair
from Protocols.AES import encrypt, decrypt
from Math.MillerRabin import genPrime
import socket
import json

class Client:
    def __init__(self, host, port):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.connect((host, port))
        
        self.MSG_HEADER = 8
        self.AES_PRIV = genPrime(8)
        self.AES_KEY = self.diffieHellman()
        
    def diffieHellman(self):
        AES_N = self.openRecv()
        AES_P = self.openRecv()
        key = self.openRecv()
        self.openSend(pow(AES_P, self.AES_PRIV, AES_N))
        return pow(key, self.AES_PRIV, AES_N)
        
    def openRecv(self):
        msg_len = int.from_bytes(self.server.recv(self.MSG_HEADER))
        return int.from_bytes(self.server.recv(msg_len))
    
    def openSend(self, msg : int):
        if type(msg) is int:
            msg_len = (msg.bit_length() + 7) // 8
            self.server.send((msg_len).to_bytes(self.MSG_HEADER))
            self.server.send(msg.to_bytes(msg_len))
        else: raise TypeError(f"Unsupported message type to openSend: {type(msg)}")
    
    def AESRecv(self):
        msg_len = int.from_bytes(self.server.recv(self.MSG_HEADER))
        msg = decrypt(int.from_bytes(self.server.recv(msg_len)), self.AES_KEY)
        return (msg).to_bytes(msg_len).strip(b'\x00').decode()
        
    def AESSend(self, msg : str):
        msg : int = encrypt(msg, self.AES_KEY)
        msg_len = (msg.bit_length() + 7) // 8
        self.server.send(msg_len.to_bytes(self.MSG_HEADER))
        self.server.send(msg.to_bytes(msg_len))

if __name__ == "__main__":
    client = Client("localhost", 9998, "Client1")
    print(client.AESRecv())