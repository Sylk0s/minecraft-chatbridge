from subprocess import Popen, PIPE
import threading

process = Popen(["publisher/exampleInput.sh"], stdout=PIPE, stdin=PIPE, universal_newlines=True)

process.stdin.write("5\n")
process.stdin.flush()
stdout = process.stdout.readline()

print(stdout)

if stdout == "25\n":
    process.stdin.write("yes\n")
    print(process.stdout.readline())

#class Out(threading.Thread):
#    def run(self):
#        for out in iter(popen.stdout.readline, ""):
#            print(out)

#class In(threading.Thread):
#    def run(self):
#        popen.stdin.write("hey")
#        popen.stdin.flush()

#out = Out()
#out.start()
#inp = In()
#inp.start()