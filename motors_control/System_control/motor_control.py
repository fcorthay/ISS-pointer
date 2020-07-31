#!/usr/bin/python3

from adafruit_motorkit import MotorKit
from adafruit_motor import stepper



kit = MotorKit()

def ToAngle(angleToReach,motorName,actualAngle) :
	motor = ""
	if motorName.lower() == "h" :
		motor = kit.stepper1
		print("Motor Hori")
	else :
		motor = kit.stepper2
		print("Motor Vert")

	if(angleToReach>360):
		angleToReach -= 360


	while abs(angleToReach-actualAngle)>1.8 :
		actualAngle+=1.8
		motor.onestep()
		if(actualAngle > 360) :
			actualAngle -= 360
	print("target reached  :"+str(actualAngle)+"°"+"\n\n")	
	motor.release()









