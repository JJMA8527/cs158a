from socket import *

name = 'localhost'
port = 12000

conn = socket(AF_INET, SOCK_STREAM)
conn.connect((name,port))

msg = input("Input lowercase sentence: ")
conn.send(msg.encode())

msg_length = int(msg[:2])
response = ''

while len(response) < msg_length:
    response += conn.recv(64).decode()

print("From server: ", response)



