from socket import *
import threading
import uuid
import json



class Message:
    def __init__(self,uuid,flag):
        self.uuid = uuid                            #uuid.UUID
        self.flag = flag                            #int
    
    #convert obj to json string
    def dump_json(self):
        return json.dumps({'uuid': str(self.uuid),'flag': self.flag})
    

#func code

def log_recv():
    #smth


def log_send():
    #smth


def ignore():
    #log file show if recv msg is ignored





# main code

threads = []

server = socket(AF_INET,SOCK_STREAM)
