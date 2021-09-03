import redis
from subprocess import Popen, PIPE
from threading import Thread
import json
from queue import Queue, Empty
import asyncio

configs = json.load(open("publisher/configs.json"))

r = redis.Redis(host=configs['host'], port=configs['port'], password=configs['pass'])

server = Popen(["java","-jar",configs['path'], "--nogui"], stdout=PIPE,  stdin=PIPE, universal_newlines=True)

def getOut(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

def getIn(queue):
    while True:
        inp = input()
        queue.put(inp)
        
qOut = Queue()
tOut = Thread(target=getOut, args=(server.stdout, qOut))
tOut.daemon = True
tOut.start()
qIn = Queue()
tIn = Thread(target=getIn, args=(qIn,))
tIn.daemon = True
tIn.start()

while True:
    try: print(qOut.get_nowait())
    except: pass
    try: 
        prgmInput = qIn.get_nowait()
        server.stdin.write(prgmInput)
        print(f"Inputed: {prgmInput}")
    except: pass
