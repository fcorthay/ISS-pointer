#!/usr/bin/python3

path = "/tmp/tick.txt"
while True:
    fifo = open(path, "r")
    line = fifo.read()
    print("Received: " + line)
    fifo.close()
