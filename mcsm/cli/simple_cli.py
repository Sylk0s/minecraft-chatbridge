from mcsm.server.mc_server import Server
from queue import Queue

class SimpleCLI:
    def setServer(self, server):
        self.server = server

    def getServerInput(self):
        while True:
            user_in = input()

            if self.checkMCSM(user_in):
                pass
            self.server.in_queue.put(user_in)

    def getServerOutput(self):
        while True:
            try:
                # isn't getting here
                out = self.server.out_queue.get_nowait()
                print(out)
            except:
                pass

    def checkMCSM(self, msg):
        return False
