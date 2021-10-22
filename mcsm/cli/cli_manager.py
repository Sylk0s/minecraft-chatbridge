from mcsm.cli.simple_cli import SimpleCLI
from threading import Thread

class Manager:
    def __init__(self, server):
        self.cli = SimpleCLI()
        self.cli.setServer(server)

    def startCLI(self):
        inThread = Thread(target=self.cli.getServerInput, args=())
        inThread.daemon = True
        inThread.start()

        outThread = Thread(target=self.cli.getServerOutput, args=())
        outThread.daemon = True
        outThread.start()