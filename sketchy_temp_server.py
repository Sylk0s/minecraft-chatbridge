# instance = Popen(["java","-jar",self.configs.getJarPath(),"--nogui"], cwd=self.configs.path, stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=False, bufsize=0)

import pexpect
from threading import Thread
import time

p = pexpect.spawn("java -jar /home/sylkos/server/server.jar --nogui", cwd="/home/sylkos/server/")

def sendInput():
    while True:
        userin = input()
        print("Input",userin)
        p.write(userin)

def getOutput():
    while True:
        if x := p.readline():
            print(x)

tIn = Thread(target=sendInput)
tIn.daemon = True
tIn.start()

tOut = Thread(target=getOutput)
tOut.daemon = True
tOut.start()

while True:
    time.sleep(5)