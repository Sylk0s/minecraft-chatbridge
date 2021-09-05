import redis
from subprocess import Popen, PIPE
from threading import Thread
import json
from queue import Queue, Empty
import asyncio

def main():
    configs = json.load(open("publisher/configs.json"))
    r = redis.Redis(host=configs['host'], port=configs['port'], password=configs['pass'])
    server = Popen(["java","-jar",configs['path'], "--nogui"], stdout=PIPE,  stdin=PIPE, universal_newlines=True)

    # queue for program output
    qOut = Queue()
    tOut = Thread(target=getOut, args=(server.stdout, qOut))
    tOut.daemon = True
    tOut.start()

    # queue for program input
    qIn = Queue()
    tIn = Thread(target=getIn, args=(qIn,))
    tIn.daemon = True
    tIn.start()

    # queue for discord input
    qExt = Queue()
    tExt = Thread(target=getExt, args=())
    tExt.daemon = True
    tExt.start()

    while True:
        try: 
            prgmOutput = parseB(qOut.get_nowait())
            print(prgmOutput)
            # parse output
            # handle any client cmd output
            # send parsed to redis
        except: pass
        try:
            prgmInput = qIn.get_nowait()
            server.stdin.write(parseTellraw(prgmInput))
        except: pass
        try:
            extInput = qExt.get_nowait()
            server.stdin.write(parseTellraw(extInput))
        except: pass

# Output:
# in form b'message'
# full server message = message[2:-1]
# parsed discord message looks for <> and grabs the rest of it
# add special cases for contains joined the game etc
# two types of parse, one for external and one for cmd

def getOut(out, queue):
    for line in iter(out.readline, b''):
        queue.put(line)
    out.close()

# Input:
# publishes to redis exactly what should be put into the game
# input as a tellraw command to look fancy
# custom color?

def getIn(queue):
    while True:
        inp = input()
        queue.put(inp)

def getExt():
    pass

def parseB(message):
    return message[2:-1]

def parseTellraw(message):
    return f"/tellraw @a {{\"rawtext\":[{{\"text\":\"{message}\"}}]}}"

def isFromPlayer():
    pass

def handleExt(message):
    # if send ext
    # parse special case
    # parse player message
    # send
    pass

def handleCommands():
    # if player message and commands enabled
    # find command
    # execute command
    pass
        
if __name__ == "__main__":
    main()