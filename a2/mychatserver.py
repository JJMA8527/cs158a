from socket import *
import threading

# func code
clients = []
def chat_room(conn,addr):
    clients.append(conn)
    while True:
        response = conn.recv(1024).decode()                                 
        if response == 'exit':
            conn.send("Disconnected from server".encode())
            break

        msg = f"{addr[1]}: {response}"                                   # port: client msg
        print(msg)

        for c in clients:
            if c is not conn:
                c.send(msg.encode())
    
    clients.remove(conn)
    conn.close()
        



# main code
threads = []
port = 49999

server = socket(AF_INET,SOCK_STREAM)
server.bind(('localhost',port))


print(f"Server listening on {server.getsockname()[0]}:{port}")              #gets the ip addr from tuple
server.listen(100)
                 

while True:
    conn, addr = server.accept()

    print(f"New connection from {addr}")                                    #client address + port #
              
    t = threading.Thread(target=chat_room,args=(conn,addr))                 #threads handle mulitple clients
    threads.append(t)
    t.start()
    














