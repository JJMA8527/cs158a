from socket import *
import threading

name = 'localhost'
port = 49999

conn = socket(AF_INET,SOCK_STREAM)
conn.connect((name,port))

print("Connected to chat server. Type 'exit' to leave")

def receive_msg(conn):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        print(data)

def send_msg(conn):
    while True:
        msg = input()
        conn.send(msg.encode())
        if msg == 'exit':                                           #exit chat server
            break


#run both threads parallel 
recv_thread = threading.Thread(target=receive_msg, args = (conn,))
send_thread = threading.Thread(target=send_msg, args = (conn,))
recv_thread.start()
send_thread.start()
recv_thread.join()
send_thread.join()


conn.close()






