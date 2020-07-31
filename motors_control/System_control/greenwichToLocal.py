#!/usr/bin/python3

import os
import constants
import transformations

WRITE_PIPE_OUT = True

# ------------------------------------------------------------------------------
                                                   # create pipe if not yet done
try:
    os.mkfifo(constants.local_coord_file)
except:
    pass
                                                                    # print info
print('Transforming from Greenwich to local coordintate system')
print(constants.INDENT + "Reading from {}".format(constants.GREENWICH_COORD_FILE))
print(constants.INDENT + "Writing to {}".format(constants.LOCAL_COORD_FILE))
print()
                                                                     # transform
while True:
                                                                # read from pipe
    greenwich_coord = open(constants.GREENWICH_COORD_FILE, "r")
    line = greenwich_coord.read()
    print(constants.INDENT + 'read: ' + line)
    greenwich_coord.close()
                                                         # transform coordinates
    (x_g, y_g, z_g) = transformations.read_coordinates(line)
    (x_l, y_l, z_l) = transformations.greenwich_to_local(x_g, y_g, z_g)
    line = str(x_l) + constants.SEPARATOR
    line = line + str(y_l) + constants.SEPARATOR
    line = line + str(z_l)
    print(constants.INDENT*2 + 'writing: ' + line)
                                                                 # write to pipe
    if WRITE_PIPE_OUT:
        local_coord = open(constants.LOCAL_COORD_FILE, "w")
        local_coord.write(line)
        local_coord.close()
