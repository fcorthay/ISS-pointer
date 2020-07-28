#!/usr/bin/python3
"""Test for using adafruit_motorkit with 2 stepper motors"""
import time
from adafruit_motorkit import MotorKit
from adafruit_motor import stepper

microstep_nb = 16
step_nb = 100
INDENT = '  '

print('Testing stepper motors')
kit = MotorKit()

for motor in [kit.stepper1, kit.stepper2]:

    if motor is kit.stepper1:
        print(INDENT + 'motor 1')
    else:
        print(INDENT + 'motor 2')

    print(INDENT*2 + 'forwards')
    for index in range(step_nb):
        motor.onestep()
        time.sleep(0.01)

    time.sleep(1)

    print(INDENT*2 + 'backwards')
    for index in range(step_nb):
        motor.onestep(direction=stepper.BACKWARD)
        time.sleep(0.01)

    time.sleep(1)

    print(INDENT*2 + 'double coil forwards')
    for index in range(step_nb):
        motor.onestep(style=stepper.DOUBLE)
        time.sleep(0.01)

    time.sleep(1)

    print(INDENT*2 + 'microstep backwards')
    for index in range(microstep_nb*step_nb):
        motor.onestep(direction=stepper.BACKWARD, style=stepper.MICROSTEP)
        time.sleep(0.01)

    motor.release()
    print()
