#!/usr/bin/python3
import os, sys
import time

tick_pipe_filespec = "/tmp/tick.txt"
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
print(INDENT + 'Waiting for soembody to read')
try:
    tick_pipe = open(tick_pipe_filespec, "w")
except Exception as e:
    print(e)
    sys.exit()
                                                               # send time ticks
x = 0
#while True:
while x < 10:
    print (INDENT + "sending {:d}".format(x))
    tick_pipe.write(str(x) + "\n")
#    tick_pipe.flush()
    x+=1
    time.sleep(1)
                                                                    # close file
print ('Closing pipe')
tick_pipe.close()
                                                              # delete pipe file
try:
    os.unlink(tick_pipe_filespec)
except:
    pass
