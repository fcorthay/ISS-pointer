#!/usr/bin/python3

import os
import time

path = "/tmp/tick.txt"
try:
    os.mkfifo(path)
except:
    pass

index = 0
while True:
    fifo = open(path, "w")
    line = "Message {:d}".format(index)
    print(line)
    fifo.write(line)
    fifo.close()
    time.sleep(1)
    index = index + 1
