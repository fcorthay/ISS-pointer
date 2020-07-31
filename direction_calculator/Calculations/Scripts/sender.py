#!/usr/bin/python3

import os
import time

path = "/tmp/tick.txt"
try:
    os.unlink(path)
except:
    pass
os.mkfifo(path)

for index in range(3):
    fifo = open(path, "w")
    line = "Message {:d}!".format(index)
    print(line)
    fifo.write(line)
    fifo.close()
    time.sleep(1)
