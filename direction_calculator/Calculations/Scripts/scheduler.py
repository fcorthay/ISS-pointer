#!/usr/bin/python3

import os, sys
import time
from datetime import datetime
from datetime import timedelta

tick_pipe_filespec = "Tick.txt"
INDENT = '  '

# ------------------------------------------------------------------------------
                                                              # create pipe file
print('Starting scheduler')
try:
    os.mkfifo(tick_pipe_filespec)
except:
    pass
else:
    print(INDENT + "Tick FIFO {} has been created".format(tick_pipe_filespec))
                                                                     # open file
print('Opening pipe')
print(INDENT + 'Waiting for somebody to read')
try:
    tick_pipe = open(tick_pipe_filespec, "w")
except Exception as e:
    print(e)
    sys.exit()
                                                               # send time ticks
x = datetime(2020,7,25,0,0,0)
#while True:
while x < datetime(2020,7,25,0,1,0):
    x_str = str(x)
    print (INDENT + "sending " + x_str)
    tick_pipe.write(str(x_str))
#    tick_pipe.flush()
    x+= timedelta(milliseconds=(int(round(1000))))
    time.sleep(1)
                                                                    # close file
print ('Closing pipe')
tick_pipe.close()
                                                              # delete pipe file
try:
    os.unlink(tick_pipe_filespec)
except:
    pass
