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

delay_in_sec = 30
                                                               # send time ticks
x = datetime.now() + timedelta(seconds = delay_in_sec-1)

# Initial step for Int.py have
x_str = str(x)
print (INDENT + "sending " + x_str)
tick_pipe = open(tick_pipe_filespec, "w")
tick_pipe.write(str(x_str))
#    tick_pipe.flush()
tick_pipe.close()
x+= timedelta(milliseconds=(int(round(1000))))
time.sleep(delay_in_sec)

x = datetime.now()
x_end = x + timedelta(days = 7) #work will end after 7 days
while x < x_end:
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
