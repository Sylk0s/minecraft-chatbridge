from queue import Queue

class Reader:
    def __init__(self):
        self.server_output = queue
        self.message_out_queue = Queue()

    def getNextMessage(self):
        return self.server_output.get_nowait()

    def handleMsg(self, msg):
        pass
    # parses into Message() for use in plugins and programs
    # reads the output and calls core functionality first, then plugins