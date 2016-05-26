import socket
import threading
from itertools import cycle
import time
import logging


HOST = '127.0.0.1'    # The remote host
PORT = 50007

COMMANDS = cycle([
    'IN,1','IN,2','IN,3','IN,4'
])

REPLIES = dict([
 ('IN,1,1','OUT,1,1'),
 ('IN,2,1','OUT,2,1'),
 ('IN,3,1','OUT,3,1'),
 ('IN,4,1','OUT,4,1'),
 ('IN,1,0','OUT,1,0'),
 ('IN,2,0','OUT,2,0'),
 ('IN,3,0','OUT,3,0'),
 ('IN,4,0','OUT,4,0')
])


CR = '\r\n' #в контроллерах обычно \r, в винде \r\n, в линуксах \n - нужно поставить то что просит железяка


def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    
    try:
        process(s)    
    except:
        s.close()
        time.sleep(5)


def read(fd,lock):
    while True:
        l = fd.readline().strip()
        logging.debug('< ' + l)
        if l in REPLIES.keys():
            lock.acquire()
            fd.write(REPLIES[l])
            fd.write(CR)
            lock.release()
        
        
def write(fd,lock):
    for cmd in COMMANDS:
        logging.debug('> ' + l)
        lock.acquire()
        fd.write(cmd)
        fd.write(CR)
        lock.release()
        time.sleep(1)



def process(s):
    fd = s.makefile('w+U')
    lock = threading.Lock()
    rt = threading.Thread(target=read, args=(fd,lock))
    wt = threading.Thread(target=write, args=(fd,lock))
    rt.start()
    wt.start()
    rt.join()
    wt.join()
    
    
if __name__ == "__main___":
    logging.basicConfig(level=logging.DEBUG)
    while True:
        connect()
