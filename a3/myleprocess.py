from socket import *
import threading
import uuid
import json
import logging

logging.basicConfig(filename='log.txt',level=logging.INFO)

class Message:
    def __init__(self,uuid,flag):
        self.uuid = uuid                                                    #uuid.UUID
        self.flag = flag                                                    #int
    
    #convert obj to json string
    def dump_json(self):
        return json.dumps({'uuid': str(self.uuid),'flag': self.flag})
    
    #jsons string to  message obj
    @staticmethod
    def load_json(s):
        data = json.loads(s)
        return Message(uuid.UUID(data['uuid'],data['flag']))

class Node:
    def __init__(self):
        self.state = 0                                                      #state 1 show leader
        self.leader_id = None
        self.my_uuid = uuid.uuid4()
        self.lock = threading.Lock()
        self.cn_sock = None

#func code

def log_recv(msg,proc):
    #msg.uuid = sender, proc = me
    cmp = (
        "greater" if msg.uuid > proc.my_uuid else
            
        "less" if msg.uuid < proc.my_uuid else
            
        "same"         
    )
    log = (
        "Received: "
        f"Uuid= {msg.uuid}, "
        f"Flag= {msg.flag}, "
        f"{cmp}, "
        f"{proc.state}\n"
    )

    if proc.state == 1:
        log += f"Leader is decided to {proc.leader_id}\n"
    
    logging.info(log)


def log_send(msg):
    logging.info(f"Sent: uuid={msg.uuid}, flag={msg.flag}\n")


def ignore(msg):
    #log file show if recv msg is ignored
    logging.info(f"Ignored: {msg.uuid}\n")

#asynch ring server
def ring(conn,addr,proc):
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        msg = Message.load_json(data)
        '''
        How it works:
        O(n^2) proc send msg with id to left. Wait for msg from right
        msg id > proc id move msg to left else ignores this msg
        msg id == proc my id then send msg to left im leader
        other nodes update status to non-leader

        '''
        with proc.lock:
            log_recv(msg,proc)

            #leader election
            if msg.flag == 0:
                log_send(msg)
                proc.cn_sock.send(data.encode())
                return
            
            #already have leader
            if msg.flag == 1:
                proc.state = 1
                proc.leader_id = msg.uuid
                log_send(msg)
                proc.cn_sock.send(data.encode())
                return
            
            #I'm the leader
            if msg.uuid == proc.my_uuid:
                proc.state = 1
                proc.leader_id = proc.my_uuid
                resp = Message(uuid=proc.my_uuid, flag=1)
                proc.cn_sock.send(resp.encode())
                return
            
            if proc.state == 1 and msg.flag == 1:
                ignore(msg)
                return
              
    conn.close()

def config_setup():
    #format -> ip,port





# main code

threads = []

server = socket(AF_INET,SOCK_STREAM)
