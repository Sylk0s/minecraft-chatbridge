from server_manager.server.server import Server
import time

class Controller:
    def runServer(self):
        server = Server("server", self)
        server.run()

        while True:
           time.sleep(1)

    def getServerConfigFile(self):
        return "/home/sylkos/projects/minecraft-chatbridge/server_configs.json"

ctl = Controller()
ctl.runServer()