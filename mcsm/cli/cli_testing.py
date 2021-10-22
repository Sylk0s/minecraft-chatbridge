import os
import time

# ⬛

(width, height) = os.get_terminal_size()

chars = int(width) * int(height)

def genString(c, size):
    s = ""
    for l in range(size):
        s = s + c
    return s

s1 = genString("|", chars)
s2 = genString("/", chars)
s3 = genString("-", chars)
s4 = genString("\\", chars)

a = [s1, s2, s3, s4]

print(s1)
time.sleep(1)
print(s2)
time.sleep(1)
print(s3)
time.sleep(1)
print(s4)
time.sleep(1)

count = 0
while True:
    print(a[count % len(a)], end = "\r")
    count += 1
    time.sleep(1)