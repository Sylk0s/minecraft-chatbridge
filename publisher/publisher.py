from subprocess import Popen, PIPE
from threading import Thread
import json
from queue import Queue, Empty

hasCommands = False
hasRedis = False

if True:
    import redis
    hasRedis = True


if file in directory:
    # import commands
    hasCommands = True
    

def main():
    configs = json.load(open("publisher/configs.json"))
    aliasList = json.load(open("publisher/aliases.json"))
    commandList = [] # this will change later on {"trigger":"method_name"}

    o = redis.Redis(host=configs['host'], port=configs['port'], password=configs['pass'])
    i = redis.Redis(host="",port="",password="")
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
            prgmOutput = parseMsg(qOut.get_nowait())
            print(prgmOutput)
            if hasCommands:
                if (cmd := prgmOutput.handleAlias()): # dont think this should be here
                    qIn.put(cmd)
                if (cmd := prgmOutput.handleCommands()):
                    qIn.put(cmd)
            if hasRedis:
                # import redis
                pass
        except: pass
        try:
            prgmInput = qIn.get_nowait()
            if True:
                server.stdin.write(parseTellraw(prgmInput))
        except: pass
        try:
            extInput = qExt.get_nowait()
            if True:
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

def parseTellraw(msg):
    return f"/tellraw @a {{\"rawtext\":[{{\"text\":\"{msg}\"}}]}}"

def isFromPlayer():
    pass

def handleExt(msg):
    # if send ext
    # parse special case
    # parse player message
    # send
    pass

def parseToMsg(msg):
    message = Message("", "", "", msg)
    return message

class Message():
    def __init__(self, sender, content, time, full):
        self.sender = sender
        self.content = content
        self.time = time
        self.full = full

    def __str__(self):
        return self.full

    def getCmdArgs(self, key):
        split = self.content.split(" ")
        return split[split.index(key):]

    def isAlias(self):
        for alias in aliasList:
            if alias in self.content:
                return alias
        return False

    def isCommand(self):
        for command in commandList:
            if command in self.content:
                return command
        return False

    # Commands refer to some listener command that requires a bit more logic to implement
    # these commands could do something on the local machine, check for some permission leve
    # do something in the web, etc...
    # The user can write their own in commands.py 

    def handleCommands(self):
        if (command := self.isCommand()):
            args = self.getCmdArgs(command)
            return getattr(commands, command)(self, args)

    # Aliases refer to a listener command mapped to an mc command
    # These are stored in alises.json in the format "key":"mc-command"
    # if the alias is "!ping":"say pong" then the program should run /say pong
    # additionally this supports custom args
    # for example "!tp":"tp [1] [2]" would take the two words after !tp and use them
    
    # TODO make this much better and add error handling and regex

    def handleAlias(self):
        if (alias := self.isAlias()):
            args = self.getCmdArgs(alias)
            cmd = aliasList[alias]
            for i in range(1,99):
                if f"[{i}]" in cmd:
                    cmd.replace(f"[{i}]",args[i])
                else: break
            return cmd
        else: return False

if __name__ == "__main__":
    main()
