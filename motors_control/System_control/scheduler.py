#!/usr/bin/python3
import os, sys
import constants
import time
from datetime import datetime

WRITE_PIPE_OUT = False

INDENT = '  '

# ------------------------------------------------------------------------------
                                                   # create pipe if not yet done
try:
    os.mkfifo(constants.SAMPLE_TIME_FILE)
except:
    pass
                                                                    # print info
print('Sending sampling times')
print(constants.INDENT + "Writing to {}".format(constants.LOCAL_COORD_FILE))
                                                                     # transform
while True:
                                                           # prepare time string
    now = datetime.now()
    line = now.strftime(constants.DATETIME_STRING)
    #line = now.isoformat()
    print(constants.INDENT*2 + 'writing: ' + line)
                                                                 # write to pipe
    if WRITE_PIPE_OUT:
        sample_time = open(constants.SAMPLE_TIME_FILE, "w")
        sample_time.write(line)
        sample_time.close()
                                                          # wait for next sample
    time.sleep(constants.SAMPLING_PERIOD)
