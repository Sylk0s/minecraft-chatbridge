import subprocess
import time

instance = subprocess.Popen(
    ["java","-jar","/home/sylkos/server/server.jar"], 
    cwd="/home/sylkos/server", 
    stdin=subprocess.PIPE, 
    stdout=subprocess.PIPE, 
    universal_newlines=True
    )

time.sleep(15)

instance.stdin.write("say testing")
instance.stdin.flush()