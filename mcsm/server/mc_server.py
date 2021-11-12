import json
from subprocess import Popen, PIPE
from queue import Queue
from threading import Thread

class Server:
    def __init__(self, name, app):
        self.configs = Configs(name, app.getServerConfigFile())

    def run(self):
        self.instance = Popen(["java","-jar",self.configs.getJarPath()], cwd=self.configs.path, stdin=PIPE, stdout=PIPE, universal_newlines=True, shell=False)

        self.in_queue = Queue()
        self.out_queue = Queue()

        tIn = Thread(target=self.sendInput, args=(self.instance.stdin, self.in_queue))
        tIn.daemon = True
        tIn.start()
        
        tOut = Thread(target=self.getOutput, args=(self.instance.stdout, self.out_queue))
        tOut.daemon = True
        tOut.start()

        print("Server Runnning...")

    def getOutput(self, out_pipe, queue):
        for line in iter(out_pipe.readline, b''):
            queue.put(line)

        out_pipe.close()

    def sendInput(self, in_pipe, queue):
        while True:
            try:
                cli_input = queue.get_nowait()
                in_pipe.write(cli_input+ '\n') # im an idiot :\
                in_pipe.flush()
            except:
                pass

class Configs:
    def __init__(self, name, config_file):
        all_configs = json.load(open(config_file))
        configs = all_configs[name]
        self.path = configs['path']
        self.jar = configs['jar']
    
    def getJarPath(self):
        return self.path + self.jar