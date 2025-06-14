from socket import *

port = 12000
server = socket(AF_INET, SOCK_STREAM)
server.bind(('',port))

server.listen(10)

while True:
    conn, addr = server.accept()                #accept connection from client, addr = ip address
    response = conn.recv(64).decode()           #client response
    
    msg_length = int(response[:2])              #convert to int, gets the prefix
    msg = response[2:]                          


    while len(msg) < msg_length:                #with length given, read msg till
        msg += conn.recv(64).decode()
    

    print(f"Connected from {addr}\nmsg_len: {msg_length}\nprocessed: {msg}\nmsg_len_sent: {len(msg)}\nConnection closed")

    caplock = msg.upper()
    conn.send(caplock.encode())

    conn.close()


    




    
    

    



