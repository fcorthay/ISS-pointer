import numpy as np
import board
import busio
import adafruit_lsm303dlh_mag
import math


greenwich_coord_file = "/tmp/ISS_coord_greenwich.txt"
local_coord_file = "/tmp/ISS_coord_local.txt"

p=math.pi


lplace,lISS = "", ""

# ------------------------------------------------------------------------------
#read Iss greenwinch coordonates
def read_greenwich_coord_file() :
#ISS vector 
	with open (greenwich_coord_file,"r",encoding = "utf8") as f :
		lISS = (f.readlines())
	xI,yI,zI = lISS[0].split(" ")
	xI = float(xI)
	yI = float(yI)
	zI = float(zI)
	return (xI,yI,zI)



# ------------------------------------------------------------------------------
def readCoord() :
	with open ("/home/pi/readcoord/coord.txt","r",encoding = "utf8") as f :
		lplace = (f.readlines())
	x1,x2,x3 = lplace[0].split(" ")
	y1,y2,y3 = lplace[1].split(" ")
	z1,z2,z3 = lplace[2].split(" ")
	x1,x2,x3 = float(x1),float(x2),float(x3)
	y1,y2,y3 = float(y1),float(y2),float(y3)
	z1,z2,z3 = float(z1),float(z2),float(z3)
	return ([x1,x2,x3],[y1,y2,y3],[z1,z2,z3])
	
# ------------------------------------------------------------------------------
def localCoord() :
	with open ("/home/pi/readcoord/localCoord.txt","r",encoding = "utf8") as f :
		lISS = (f.readlines())
	xI,yI,zI = lISS[0].split(" ")
	xI = float(xI)
	yI = float(yI)
	zI = float(zI)
	return (xI,yI,zI)


# ------------------------------------------------------------------------------
def anglesCompas() :
	#init LSM303DHL
	i2c = busio.I2C(board.SCL, board.SDA)
	mag = adafruit_lsm303dlh_mag.LSM303DLH_Mag(i2c)


	# angle between x and y
	alphaxy = math.atan2(mag.magnetic[0],mag.magnetic[1])

	rxy = math.sqrt(mag.magnetic[0]**2+mag.magnetic[1]**2)

	#angle between z and plan xy
	alphaz = math.atan2(rxy,mag.magnetic[2])
	
	return alphaxy , alphaz
	
# ------------------------------------------------------------------------------
def norm (x) :
	n=0
	for i in range(0,2) :
			n+=x[i]**2
	return math.sqrt(n)
	
#have a look on mathilde's work	
def anglesPos(x,z,ai) :
	phi1,phi2 = 0,0
	
	for i in range(0,3) :
		phi1+=x[i]*ai[i]/(norm(x)*norm(ai))
		phi2+=z[i]*ai[i]/(norm(z)*norm(ai))
	phi1 = 360/(2*p)*(p/2 - math.acos(phi1))
	phi2 = 360/(2*p)*(p/2 - math.acos(phi2))
	return phi1,phi2
	
# ------------------------------------------------------------------------------
def ToLocalCoord(v, str) :
    longi, lat=0, 0
    if (str== "sion" ):
    #Sion
        longi = 0.1282817
        lat = 0.80686571
    if (str == "moscow") :
        longi =0.6565929
        lat = 0.9730211
    M = np.matrix([[0.5*(math.cos(longi+lat)+math.cos(longi-lat)),-math.sin(longi),0.5*(math.sin(longi+lat)-math.cos(longi-lat))],[0.5*(math.sin(longi+lat)+math.sin(longi-lat)),math.cos(longi),0.5*(-math.cos(longi+lat)+math.cos(longi-lat))],[-math.sin(lat),0,math.cos(lat)]])
    w1 = M[0,0]*v[0]+M[0,1]*v[1]+M[0,2]*v[2]
    w2 = M[1,0]*v[0]+M[1,1]*v[1]+M[1,2]*v[2]
    w3 = M[2,0]*v[0]+M[2,1]*v[1]+M[2,2]*v[2]
    return w1,w2,w3
