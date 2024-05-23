import json
from subprocess import Popen, PIPE
from queue import Queue
from threading import Thread

class Server:
    def __init__(self, name, app, configs, args):
        self.args = args
        self.configs = configs
        self.name = name
        self.app = app

    def run(self):
        self.instance = Popen(self.args, cwd=self.configs.path, stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=False)

        self.in_queue = Queue()
        self.out_queue = Queue()

        tIn = Thread(target=self.sendInput, args=(self.instance.stdin, self.in_queue), daemon = True)
        tIn.start()
        
        tOut = Thread(target=self.getOutput, args=(self.instance.stdout, self.out_queue), daemon = True)
        tOut.start()

        print(self.name,'is running')

    # Reads the server's output and puts it into the output queue for the server
    def getOutput(self, out_pipe, queue):
        for line in iter(out_pipe.readline, b''):
            queue.put(line)
        out_pipe.close()

    # Reads the server's input queue and writes it to the input pipe for the server
    def sendInput(self, in_pipe, queue):
        while True:
            try:
                cli_input = queue.get_nowait()
                in_pipe.write(cli_input+ '\n') # im an idiot :\
                in_pipe.flush()
            except:
                pass

class MCServer(Server):
    def __init__(self, name, app):
        self.configs = Configs(name, app.getServerConfigFile())
        super().__init__(name, app, self.configs, ["java","-jar",self.configs.getServerPath(), "--nogui"])
        
class Configs:
    def __init__(self, name, config_file):
        all_configs = json.load(open(config_file))
        configs = all_configs[name]
        self.path = configs['path']
        self.runnable = configs['runnable']
    
    def getServerPath(self):
        return self.path + self.runnable
