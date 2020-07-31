#!/usr/bin/python3

import os
import time
import constants

try:
    os.mkfifo(constants.GREENWICH_COORD_FILE)
except:
    pass

index = 0
while True:
    greenwich_coord = open(constants.GREENWICH_COORD_FILE, "w")
    line = "2020-07-25 00:00:00 | 0.0 | 4.210800438221973 | 6.459354829086378 | 6713.724608199999 | 0.0 | 0.0"
    print(line)
    greenwich_coord.write(line)
    greenwich_coord.close()
    time.sleep(1)
    index = index + 1
