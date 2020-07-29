#!/usr/bin/python3
import os, sys
import time

tick_pipe_filespec = "/tmp/tick.txt"
INDENT = '  '

print("Starting scheduler")
try:
    os.mkfifo(tick_pipe_filespec)
except:
    pass
else:
    print(INDENT + "Tick FIFO {} has been created".format(tick_pipe_filespec))

try:
    tick_pipe = open(tick_pipe_filespec, "w")
except Exception as e:
    print (e)
    sys.exit()

x = 0
while x < 5:
    tick_pipe.write(str(x))
    tick_pipe.flush()
    print (INDENT + "sending {:d}".format(x))
    x+=1
    time.sleep(1)
print ("Closing")
tick_pipe.close()
try:
    os.unlink(tick_pipe)
except:
    pass



#     tick_fifo = os.open(tick_pipe_filespec, os.O_WRONLY)

# with open(tick_pipe_filespec, mode = 'w') as tick_pipe:
#     print("FIFO opened")
#     data = tick_pipe.write("signal")
#     if len(data) == 0:
#         print("Writer is closed")
#     print('Write: "{0}"'.format(data))
#     tick_pipe.close()
