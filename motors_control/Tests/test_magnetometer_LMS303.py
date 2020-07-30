#!/usr/bin/python3
import board
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import time
# Import math Library
import math

INDENT = '  '

i2c = busio.I2C(board.SCL, board.SDA)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
#accel = adafruit_lsm303_accel.LSM303_Accel(i2c)

#print("Magnetometer (micro-Teslas)): X=%0.3f Y=%0.3f Z=%0.3f"%mag.magnetic)
#print("Acceleration (m/s^2): X=%0.3f Y=%0.3f Z=%0.3f"%accel.acceleration)

for index in range(100):
    [X, Y, Z] = mag.magnetic
    print("Horizontal angle: {: >7.2f}°".format(math.atan2(X, Y)*360/(2*math.pi)))
    time.sleep(1)
