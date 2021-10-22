from mcsm.server.mc_server import Server
from mcsm.cli.cli_manager import Manager
import time

class Controller:
    def runServer(self):
        server = Server("server", self)
        server.run()

        cli = Manager(server)
        cli.startCLI()

        while True:
           time.sleep(1)

    def getServerConfigFile(self):
        return "/home/sylkos/projects/minecraft-chatbridge/server_configs.json"

ctl = Controller()
ctl.runServer()