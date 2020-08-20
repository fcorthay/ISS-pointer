#!/usr/bin/python3
import sys, os
import requests
import math
from datetime import datetime
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import time
import csv

#import matplotlib
#import numpy as np

ISS_position_URL = 'http://api.open-notify.org/iss-now.json'
backgroung_image_file = os.path.dirname(sys.argv[0]) + '/earth.jpg'

x_axis_range = [-180, 180]
x_axis_length = x_axis_range[1]-x_axis_range[0]
x_tick_length = 60
y_axis_range = [-90, 90]
y_tick_length = 60

point_nb = 200
sleep_time = 7000 / point_nb

simulate_data = True
simulate_data = False
if simulate_data:
    sleep_time = 1/20
    sim_longitude = x_axis_range[0]

(figure, axes) = pyplot.subplots()

# ------------------------------------------------------------------------------
# Get ISS current location
#
found_point_nb = 0
timestamps = [0] * point_nb
longitudes = [0.0] * point_nb
latitudes = [0.0] * point_nb

while True:
    if simulate_data:
        timestamp = time.time()
        sim_longitude = sim_longitude + x_axis_length/point_nb
        if sim_longitude > x_axis_range[1]:
            sim_longitude = sim_longitude - x_axis_length
        sim_latitude = y_axis_range[0] * math.sin(sim_longitude * math.pi/180)
        ISS_position = {
            'timestamp': timestamp,
            'iss_position': {
                'longitude': str(sim_longitude),
                'latitude': str(sim_latitude)
            },
            'message': 'success'
        }
    else:
        ISS_position = requests.get(ISS_position_URL).json()
    # print(type(ISS_position))
    # print(ISS_position)
    status = ISS_position['message']
    if status == 'success':
                                                                  # get position
        timestamp = int(ISS_position['timestamp'])
        longitude = float(ISS_position['iss_position']['longitude'])
        latitude = float(ISS_position['iss_position']['latitude'])
        print("{:d} : {} : ({:+6.1f}, {:+6.1f})".format(
            timestamp,
            datetime.fromtimestamp(timestamp),
            longitude,
            latitude
        ))
                                                                # update vectors
#        print(found_point_nb)
        timestamps[found_point_nb] = timestamp
        longitudes[found_point_nb] = longitude
        latitudes[found_point_nb] = latitude
        found_point_nb = found_point_nb + 1
                                                               # draw trajectory
    if found_point_nb > 2:
        if longitudes[found_point_nb-1] < longitudes[1]:
            pyplot.close(figure)
            (figure, axes) = pyplot.subplots()
            figure.set_size_inches(8, 4)
            background_image = pyplot.imread(backgroung_image_file)
            axes.imshow(
                background_image,
                extent=[
                    x_axis_range[0], x_axis_range[1],
                    y_axis_range[0], y_axis_range[1]
                ],
                aspect='auto'
            )
            axes.plot(
                longitudes[0:found_point_nb-1],
                latitudes[0:found_point_nb-1]
            )
            axes.set_xlim(x_axis_range)
            axes.xaxis.set_major_locator(ticker.MultipleLocator(x_tick_length))
            axes.set_ylim(y_axis_range)
            axes.yaxis.set_major_locator(ticker.MultipleLocator(y_tick_length))
            pyplot.draw()
            pyplot.pause(0.5)
            pyplot.savefig('/tmp/flyover.png')
                                                                 # write to file
            CSV_file_spec = "/tmp/flyover-{}.csv"\
                .format(timestamps[found_point_nb-1])
            print(CSV_file_spec)
            CSV_file = open(CSV_file_spec, 'w')
            with CSV_file:
                writer = csv.writer(CSV_file)
                for index in range(found_point_nb-1):
                    writer.writerow([
                        timestamps[index],
                        round(longitudes[index], 3),
                        round(latitudes[index], 3)
                    ])
            found_point_nb = 0
                                                          # wait for next sample
    time.sleep(sleep_time)
