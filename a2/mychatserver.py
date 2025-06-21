from socket import *
import threading

# func code
def chat_room():
    print("Test")


# main code
threads = []
port = 49999

server = socket(AF_INET,SOCK_STREAM)
server.bind(('',port))

server.listen(100)


print(f"Server listening on {server}")                    

while True:
    conn, addr = server.accept()
    print(f"New connection from {addr}")                                    #client address + port #
        
        
    t = threading.Thread(target=chat_room,args=(conn,addr))                 #threads handle mulitple clients
    t.start()
    threads.append(t)














