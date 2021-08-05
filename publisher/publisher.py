import redis
from subprocess import Popen, PIPE
from threading import Thread
import json

#asyncio coroutine
#pipe file mkfifo

configs = json.load(open("publisher/configs.json"))

r = redis.Redis(host=configs['host'], port=configs['port'], password=configs['pass'])

server = Popen(["java","-jar",configs['path'], "--nogui"], stdout=PIPE,stdin=PIPE, universal_newlines=True)

def readOutput(serverOutput):
   for line in iter(serverOutput.readline, b''):
       print(line)

def provideInput(serverInput):
    while True:
        inp = input()
        serverInput.write(inp)
        serverInput.flush()

inputHandler = Thread(target=provideInput,args=server.stdin)
outputHandler = Thread(target=readOutput, args=server.stdout)
inputHandler.daemon = True
outputHandler.daemon = True
inputHandler.start()
outputHandler.start()

print("upsi")