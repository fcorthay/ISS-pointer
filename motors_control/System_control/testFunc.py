import board
import busio
import adafruit_lsm303_accel
import adafruit_lsm303dlh_mag
import math
import funcMagPos

#init LSM303DHL
i2c = busio.I2C(board.SCL, board.SDA)
mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)
accel = adafruit_lsm303_accel.LSM303_Accel(i2c)


# angle between x and y
alpahxy = math.atan2(mag.magnetic[0],mag.magnetic[1])

rxy = math.sqrt(mag.magnetic[0]**2+mag.magnetic[1]**2)

#angle between z and plan xy
alphaz = math.atan2(rxy,mag.magnetic[2])

#get iss position
Iss = funcMagPos.readISS()

#get our three axes
place = funcMagPos.readCoord()

#get greenwich coord local position
local = funcMagPos.localCoord()

ai = []
zip_object = zip(local,Iss)
for list1_i, list2_i in zip_object:
    ai.append(list1_i-list2_i)
    
funcMagPos.anglesPos(place[0],place[2],ai)

#for i in range(0,100):
	#ax,az = funcMagPos.anglesCompas()
	#ax=1/(2*math.pi)*ax*360
	#az=1/(2*math.pi)*az*360
	#print('Horizontal angle : ' + '{:4f}'.format(ax) + '°','angle z and Hor :' + '{:4f}'.format(az)+'°')
    
print(funcMagPos.ToLocalCoord(Iss,str))
