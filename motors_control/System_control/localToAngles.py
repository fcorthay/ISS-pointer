#!/usr/bin/python3

import os
import constants
import transformations

WRITE_PIPE_OUT = False

# ------------------------------------------------------------------------------
                                                   # create pipe if not yet done
try:
    os.mkfifo(POINTING_ANGLES_FILE)
except:
    pass
                                                                    # print info
print('Transforming from local coordintate system to pointing angles')
print(constants.INDENT + "Reading from {}".format(constants.LOCAL_COORD_FILE))
print(constants.INDENT + "Writing to {}".format(constants.POINTING_ANGLES_FILE))
print()
                                                                     # transform
while True:
                                                                # read from pipe
    local_coord = open(constants.LOCAL_COORD_FILE, "r")
    line = local_coord.read()
    print(constants.INDENT + 'read: ' + line)
    local_coord.close()
                                                         # coordinates to angles
    (x_l, y_l, z_l) = transformations.read_coordinates(line)
    (phi1, phi2) = transformations.local_to_angles([x_l, y_l, z_l])
    line = str(phi1) + constants.SEPARATOR + str(phi2)
    print(constants.INDENT*2 + 'writing: ' + line)
                                                                 # write to pipe
    if WRITE_PIPE_OUT:
        pointing_angles = open(constants.POINTING_ANGLES_FILE, "w")
        pointing_angles.write(line)
        pointing_angles.close()
