#!/usr/bin/python3

#import os
#import sys

path = "/tmp/tick.txt"
while True:
    fifo = open(path, "r")
    line = fifo.read()
    print("Received: " + line)
    fifo.close()
