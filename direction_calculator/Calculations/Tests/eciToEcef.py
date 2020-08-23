#!/usr/bin/python3
import sys, os
import csv
import datetime
import math
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker

# ------------------------------------------------------------------------------
# constants
#
revolutions_per_day = 15.49162197
mean_anomaly = 311.3398 / 360 * math.pi

reference_time = datetime.datetime(2000, 1, 1, 12, 0)  # J2000
seconds_per_solar_day = 60 * 60 * 24
seconds_per_sidereal_day = 4.0905 + 60*(56 + 60*23)
sidereal_days_per_sidereal_year = 366.256363004
seconds_per_sidereal_year = \
    seconds_per_sidereal_day * sidereal_days_per_sidereal_year
seconds_per_revolution = seconds_per_solar_day / revolutions_per_day
#print(seconds_per_sidereal_day*sidereal_days_per_sidereal_year)
#print(seconds_per_sidereal_year)

to_deg = 180/math.pi

script_pathname = os.path.dirname(sys.argv[0])  

INDENT = '  '

# ==============================================================================
# Procedures and functions
#
def coordinates_to_latitude_longitude(x, y, z):
                                                                    # projection
    longitude = np.unwrap(np.arctan2(y, x))
    latitude = np.arctan(z / np.sqrt(np.square(x)+np.square(y)))
                                                           # wrap to 360 degrees
    wrap_index = 0
    while longitude[wrap_index] < 2*math.pi:
        wrap_index = wrap_index + 1
    longitude = np.roll(longitude, -wrap_index)
    longitude = np.mod(longitude, 2*math.pi*np.ones(len(longitude)))
    latitude = np.roll(latitude, -wrap_index)
                                                       # wrap to +/- 180 degrees
    wrap_index = 0
    while longitude[wrap_index] < math.pi:
        wrap_index = wrap_index + 1
    longitude = np.roll(longitude, -wrap_index)
    longitude = np.mod(longitude+math.pi, 2*math.pi*np.ones(len(longitude)))-math.pi
#    longitude = np.mod(longitude, 2*math.pi*np.ones(len(longitude)))
    latitude = np.roll(latitude, -wrap_index)

    return(longitude, latitude)

# ==============================================================================
# Transformation from ECI J2000 coordinates to ECEF rotating coordinates
#
# ------------------------------------------------------------------------------
# Read ECI coordinates from file created by issEllipse.py
#
print('Reading ECI coordinates from file')
CSV_file_spec = script_pathname + '/issEllipse-normal.csv'
CSV_file = open(CSV_file_spec, 'r')
with CSV_file:
    reader = csv.reader(CSV_file)
    point_nb = 0
    time = np.array([])
    x_ECI = np.array([])
    y_ECI = np.array([])
    z_ECI = np.array([])
    for row in reader:
        point_nb = point_nb + 1
        time = np.append(time, float(row[0]))
        x_ECI = np.append(x_ECI, float(row[1]))
        y_ECI = np.append(y_ECI, float(row[2]))
        z_ECI = np.append(z_ECI, float(row[3]))
CSV_file.close

# ------------------------------------------------------------------------------
# ECI to ECEF transformation
#
print()
print('Transforming to ECEF coordinates')
print(INDENT + 'now is ' + str(datetime.datetime.now()))
                  # elapsed time since the beginning of the present sirereal day
elapsed = (datetime.datetime.utcnow() - reference_time).total_seconds()
print(INDENT + "total seconds : {}".format(elapsed))
full_year_nb = int(elapsed / seconds_per_sidereal_year)
print(INDENT + "full year nb : {}".format(full_year_nb))
elapsed = elapsed - full_year_nb*seconds_per_sidereal_year
print(INDENT + "seconds this year : {}".format(elapsed))
full_day_nb = int(elapsed / seconds_per_sidereal_day)
print(INDENT + "additional full day nb : {}".format(full_day_nb))
elapsed = elapsed - full_day_nb*seconds_per_sidereal_day
print(INDENT + "seconds this day : {} out of {}"\
    .format(elapsed, seconds_per_sidereal_day))
                                                        # rotate the coordinates
x_ECEF = np.zeros(len(time))
y_ECEF = np.zeros(len(time))
z_ECEF = np.zeros(len(time))
for index in range(len(time)):
    offset = elapsed + time[index]
    rotation_angle = (offset/seconds_per_sidereal_day) * 2*math.pi
#    rotation_angle = rotation_angle - mean_anomaly
                                                    # define the rotation matrix
    earth_rotation = np.array([
        [ math.cos(rotation_angle), math.sin(rotation_angle), 0],
        [-math.sin(rotation_angle), math.cos(rotation_angle), 0],
        [           0            ,             0            , 1]
    ])
                                                        # rotate the coordinates
    coordinates_ECI = np.array([[
        x_ECI[index], y_ECI[index], z_ECI[index]
    ]]).transpose()
    coordinates_ECEF = np.dot(earth_rotation, coordinates_ECI).transpose()[0]
    x_ECEF[index] = coordinates_ECEF[0]
    y_ECEF[index] = coordinates_ECEF[1]
    z_ECEF[index] = coordinates_ECEF[2]

# ------------------------------------------------------------------------------
# ECI equirectangular projection
#
print()
print('Plotting equirectangular projections')
print(INDENT + 'Earth Centered Inertial (ECI) directions')
                                                                # prepare figure
pyplot.figure(figsize=(6, 9))
pyplot.subplots_adjust(hspace = 0.5)
                                                    # equirectangular projection
(longitude, latitude) = coordinates_to_latitude_longitude(x_ECI, y_ECI, z_ECI)
ECI_plot = pyplot.subplot(211)
ECI_plot.plot(longitude*to_deg, latitude*to_deg)
                                                              # grids and labels
ECI_plot.set_xlim(-180, 180)
ECI_plot.xaxis.set_major_locator(ticker.MultipleLocator(30))
ECI_plot.set_ylim(-90, 90)
ECI_plot.yaxis.set_major_locator(ticker.MultipleLocator(30))
ECI_plot.grid()
ECI_plot.set(
    xlabel='longitude []',
    ylabel='latitude []',
    title='Earth-centered inertial projection'
)

# ------------------------------------------------------------------------------
# ECEF equirectangular projection
#
print(INDENT + 'Earth Centered Earth Fixed (ECEF) directions')
                                                    # equirectangular projection
(longitude, latitude) = coordinates_to_latitude_longitude(x_ECEF, y_ECEF, z_ECEF)
ECEF_plot = pyplot.subplot(212)
ECEF_plot.plot(longitude*to_deg, latitude*to_deg)
                                                              # grids and labels
ECEF_plot.set_xlim(-180, 180)
ECEF_plot.xaxis.set_major_locator(ticker.MultipleLocator(30))
ECEF_plot.set_ylim(-90, 90)
ECEF_plot.yaxis.set_major_locator(ticker.MultipleLocator(30))
ECEF_plot.grid()
ECEF_plot.set(
    xlabel='longitude []',
    ylabel='latitude []',
    title='Earth-centered earth-fixed projection'
)

# ==============================================================================
# Display results
#
print()
print('Rendering')
print(INDENT + 
    'Compare with ' + 
    'https://www.esa.int/Science_Exploration/Human_and_Robotic_Exploration/International_Space_Station/Where_is_the_International_Space_Station'
)
                                                     # screen and file rendering
pyplot.savefig(script_pathname + '/eciToEcef.png')
pyplot.show()
