import socket
import threading
import pandas as pd
import json

from Math.MillerRabin import genPrime
from Protocols.AES import encrypt, decrypt
from Protocols.SHA import sha256
from test import pages

class Server:
    def __init__(self, HOST : str, PORT : int):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.user_data = pd.DataFrame(columns=["Username", "Password", "Contacts"])
        
        self.MSG_HEADER = 8
        self.AES_BASE = genPrime(8)
        self.AES_PRIV = genPrime(8)
        self.AES_N = genPrime(16)
        
        self.getConnections()
        
    def __del__(self):
        self.server.close()
        
    def getConnections(self):
        print("[System] Server Started.")
        try:
            self.server.listen()
            while True:
                client, addr = self.server.accept()
                thread = threading.Thread(target=self.handleClient, args=[client], daemon=True)
                thread.start()
                print("Client Connected")
        except KeyboardInterrupt:
            print("\n[System] Closing Server.")
            self.server.close() 
        
    def diffieHellman(self, client):
        self.openSend(client, self.AES_N)
        self.openSend(client, self.AES_BASE)
        self.openSend(client, pow(self.AES_BASE, self.AES_PRIV, self.AES_N))
        return pow(self.openRecv(client), self.AES_PRIV, self.AES_N)   
        
    def openRecv(self, client : socket.socket) -> str:
        msg_len = int.from_bytes(client.recv(self.MSG_HEADER))
        return int.from_bytes(client.recv(msg_len))
    
    def openSend(self, client : socket.socket, msg : str | int):
        if type(msg) is int:
            msg_len = (msg.bit_length() + 7)//8
            client.send((msg_len).to_bytes(self.MSG_HEADER))
            client.send(msg.to_bytes(msg_len))
        else: raise TypeError(f"Unsupported message type to openSend: {type(msg)}")
        
    def AESRecv(self, client : socket.socket, AES_KEY):
        msg_len = int.from_bytes(client.recv(self.MSG_HEADER))
        msg = decrypt(int.from_bytes(client.recv(msg_len)), AES_KEY)
        return (msg).to_bytes(msg_len).strip(b'\x00').decode()
    
    def AESSend(self, client : socket.socket, AES_KEY : int,  msg : str):
        msg : int = encrypt(msg, AES_KEY)
        msg_len = (msg.bit_length() + 7) // 8
        client.send(msg_len.to_bytes(self.MSG_HEADER))
        client.send(msg.to_bytes(msg_len))  
        
    def getPage(self, page_name):
        if not page_name in pages: return {}
        return pages[page_name]
            
            
    def handleClient(self, client : socket.socket):
        key = self.diffieHellman(client)
        while True:
            msg = self.AESRecv(client, key)
            if not msg: break
            if "GET" in msg: self.AESSend(client, key, json.dumps(self.getPage(msg[4:])))
            if "POST" in msg:
                msg = msg.split(" ")
                if msg[1] == "authenticate":
                    if not self.user_data[(self.user_data["Username"] == msg[2])&(self.user_data["Password"] == sha256(msg[3]))].empty:
                        self.AESSend(client, key, json.dumps(self.getPage("Lobby")))
                    else:
                        self.AESSend(client, key, json.dumps(self.getPage("Sign In")))
                elif msg[1] == "register":
                    self.user_data.loc[len(self.user_data)] = [msg[2], sha256(msg[3]), []]
                    self.AESSend(client, key, json.dumps(self.getPage("Lobby")))
        client.close()
        print("Client disconneted")
                
### Run Server ###            
if __name__ == "__main__":
    Server("localhost", 9091)