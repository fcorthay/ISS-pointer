#!/usr/bin/python3

import os, sys
import time
from datetime import datetime
from datetime import timedelta

tick_pipe_filespec = "/tmp/tick.txt"
INDENT = '  '

# ------------------------------------------------------------------------------
                                                              # create pipe file
print('Starting scheduler')
try:
    os.unlink(tick_pipe_filespec)
except:
    pass
os.mkfifo(tick_pipe_filespec)
print(INDENT + "Tick FIFO {} has been created".format(tick_pipe_filespec))
                                                               # send time ticks
x = datetime(2020,7,31,10,0,0)
#while True:
while x < datetime(2020,7,31,10,1,0):
    x_str = str(x)
    print (INDENT + "sending " + x_str)
    tick_pipe = open(tick_pipe_filespec, "w")
    tick_pipe.write(str(x_str))
#    tick_pipe.flush()
    tick_pipe.close()
    x+= timedelta(milliseconds=(int(round(1000))))
    time.sleep(1)
                                                              # delete pipe file
print ('Deleting pipe')
try:
    os.unlink(tick_pipe_filespec)
except:
    pass
