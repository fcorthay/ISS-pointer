#!/usr/bin/python3
from datetime import datetime
from math import *

# ------------------------------------------------------------------------------
# Pipe file specifications
#
SAMPLE_TIME_FILE = "/tmp/sample_time.fifo"
GREENWICH_COORD_FILE = "/tmp/ISS_coord_greenwich.fifo"
LOCAL_COORD_FILE = "/tmp/ISS_coord_local.fifo"
POINTING_ANGLES_FILE = "/tmp/ISS_angles.fifo"

# ------------------------------------------------------------------------------
# Date and time information
#
DATETIME_STRING = "%d-%m-%Y %H:%M:%S"

# ------------------------------------------------------------------------------
# Local coordinates
#
                                                            # Moscow coordinates
LOCAL_LONGITUDE = 0.6565929
LOCAL_LATITUDE = 0.9730211
                                                              # Sion coordinates
LOCAL_LONGITUDE = 0.1282817
LOCAL_LATITUDE = 0.80686571
                                                                 # earth ellipse
b = 6356.752*1000
a = 6378.137*1000
R = sqrt(
    (a**4*cos(LOCAL_LATITUDE)**2+b**4*sin(LOCAL_LATITUDE)**2) /
    (a**2*cos(LOCAL_LATITUDE)**2+b**2*sin(LOCAL_LATITUDE)**2)
)
#print('{:.5E}'.format(((a**4)*(cos(LOCAL_LATITUDE)**2)+(b**4)*(sin(LOCAL_LATITUDE)**2))))
Rprime = sqrt(R**2-R**2*sin(LOCAL_LATITUDE)**2)
OA=(
    0.001*Rprime*cos(LOCAL_LONGITUDE),
    0.001*Rprime*sin(LOCAL_LONGITUDE),
    0.001*R*sin(LOCAL_LATITUDE)
)
                                                                    # local axes
LOCAL_X_AXIS = (
    -sin(LOCAL_LONGITUDE),
    cos(LOCAL_LONGITUDE),
    0
) + OA
LOCAL_Y_AXIS = (
    0.5*(sin(LOCAL_LONGITUDE+LOCAL_LATITUDE)-sin(LOCAL_LONGITUDE-LOCAL_LATITUDE)),
    0.5*(cos(LOCAL_LONGITUDE+LOCAL_LATITUDE)-cos(LOCAL_LONGITUDE-LOCAL_LATITUDE)),
    cos(LOCAL_LATITUDE)
) + OA
LOCAL_Z_AXIS = (
    0.5*(cos(LOCAL_LONGITUDE+LOCAL_LATITUDE)+cos(LOCAL_LONGITUDE-LOCAL_LATITUDE)),
    0.5*(sin(LOCAL_LONGITUDE+LOCAL_LATITUDE)+sin(LOCAL_LONGITUDE-LOCAL_LATITUDE)),
    -sin(LOCAL_LATITUDE)
) + OA 


# ------------------------------------------------------------------------------
# Display elements
#
SEPARATOR = '|'
INDENT = '  '
