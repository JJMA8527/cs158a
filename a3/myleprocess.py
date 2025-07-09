from socket import *
import threading
import uuid
import json
import logging
import time
import sys

node_num = sys.argv[1] if len(sys.argv) > 1 else ""
log_file = f"log{node_num}.txt"
logging.basicConfig(filename=log_file,level=logging.INFO, format='%(message)s')


class Message:
    def __init__(self,uuid,flag):
        self.uuid = uuid                                                    #uuid.UUID
        self.flag = flag                                                    #int
    
    #convert obj to json string
    def dump_json(self):
        return json.dumps({'uuid': str(self.uuid),'flag': self.flag}) + '\n' #every json msg end with \n
    
    #jsons string to  message obj
    @staticmethod
    def load_json(s):
        data = json.loads(s)
        return Message(uuid.UUID(data['uuid']),data['flag'])

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

def server_init(srv_sock,proc):
    conn, addr = srv_sock.accept()
    ring(conn,addr,proc)

#asynch ring server
def ring(conn,addr,proc):
    buffer = ''
    while True:
        data = conn.recv(1024).decode()
        if not data:
            break
        buffer += data
        while '\n' in buffer:
            line, buffer = buffer.split('\n',1)
            if line.strip() == '':
                continue
            msg = Message.load_json(line)
        '''
        How it works:
        O(n^2) proc send msg with id to left. Wait for msg from right
        msg id > proc id move msg to left else ignores this msg
        msg id == proc my id then send msg to left im leader
        other nodes update status to non-leader

        '''
        with proc.lock:
            log_recv(msg,proc)

            #I'm the leader
            if msg.uuid == proc.my_uuid and msg.flag==0:
                proc.state = 1
                proc.leader_id = proc.my_uuid
                resp = Message(uuid=proc.my_uuid, flag=1)
                log_send(resp)
                proc.cn_sock.send(resp.dump_json().encode())
                continue

            #already have leader
            if msg.flag == 1:
                if proc.state == 0:
                    proc.state = 1
                    proc.leader_id = msg.uuid
                    log_send(msg)
                    proc.cn_sock.send((line+'\n').encode())
                else:
                    ignore(msg)
                continue

            #leader election
            if msg.flag == 0:
                if proc.state == 0:
                    log_send(msg)
                    proc.cn_sock.send((line+'\n').encode())
                else:
                    ignore(msg)
                continue
    
    conn.close()


def config_setup():
    #format -> ip,port\n
    try:                                                                        #testing purposes for more nodes
        node_ind = int(sys.argv[1])
    except (IndexError,ValueError):
        node_ind = 0
    
    with open('test_config.txt','r') as f:
        lines = [line.strip() for line in f if line.strip()]
        self_ip, self_port = lines[node_ind].split(',')
        other_ind = (node_ind+1) % len(lines)
        other_ip, other_port = lines[other_ind].split(',')                      #should work for more than 1 cn conn

        return (self_ip,int(self_port)), (other_ip,int(other_port))



# main code

threads = []
(srv_ip, srv_port), (cn_ip, cn_port) = config_setup()
proc = Node()

server = socket(AF_INET,SOCK_STREAM)
server.bind((srv_ip,srv_port))

server.listen(5)

proc.cn_sock = socket(AF_INET,SOCK_STREAM)
while True:
    try:
        proc.cn_sock.connect((cn_ip,cn_port))
        break
    except:
        time.sleep(1)

t = threading.Thread(target=server_init, args=(server,proc))                       #server thread
t.start()

time.sleep(5)   


#1 time send uuid
init_msg = Message(uuid=proc.my_uuid,flag=0)
log_send(init_msg)
proc.cn_sock.send(init_msg.dump_json().encode())

while proc.state == 0:
    time.sleep(1)

time.sleep(5)
#when terminating node print leader
print(f"Leader is {proc.leader_id}\n")