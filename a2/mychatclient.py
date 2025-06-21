from socket import *

name = 'localhost'
port = 49999

conn = socket(AF_INET,SOCK_STREAM)
conn.connect((name,port))

