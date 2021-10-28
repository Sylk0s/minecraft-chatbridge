from mcsm.server.mc_server import Server
from mcsm.cli.cli_manager import Manager
import time
import argparse

#parser = argparse.ArgumentParser(description='Server managing cli utility', prog='mcsm')
#parser.add_argument('-s','--start', help='Starts the designated server')

#args = parser.parse_args()



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