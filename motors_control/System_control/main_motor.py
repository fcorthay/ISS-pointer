from motor_control import ToAngle
import time

targetH,targetV = range(0,360,10), range(0,360,10)
actualH = 0
actualV = 0

ToAngle(180,"h",actualH)

# for i in targetH :
# 	ToAngle(i,"h",actualH)
# 	ToAngle(i,"v",actualV)
# 	time.sleep(2)
