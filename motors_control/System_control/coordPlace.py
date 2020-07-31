from math import *

# Sion coord
alpha = 0.1282817
phi = 0.80686571

#Moscow coord
#alpha = 0.6565929
#phi = 0.9730211


b = 6356.752*1000
a = 6378.137*1000

R = sqrt((a**4*cos(phi)**2+b**4*sin(phi)**2)/(a**2*cos(phi)**2+b**2*sin(phi)**2))
#print('{:.5E}'.format(((a**4)*(cos(phi)**2)+(b**4)*(sin(phi)**2))))
Rprime = sqrt(R**2-R**2*sin(phi)**2)

OA=(0.001*Rprime*cos(alpha),0.001*Rprime*sin(alpha),0.001*R*sin(phi))

with open ("localCoord.txt","w",encoding ="utf8") as f :
	f.write(str(OA[0])+" "+str(OA[1])+" "+str(OA[2]))

#print(OA) #vector earth center to user position unit = km

# New axes

x= (-sin(alpha),cos(alpha),0)+OA
y= (0.5*(sin(alpha+phi)-sin(alpha-phi)),0.5*(cos(alpha+phi)-cos(alpha-phi)),cos(phi)) + OA
z = (0.5*(cos(alpha+phi)+cos(alpha-phi)) ,0.5*(sin(alpha+phi)+sin(alpha-phi)),-sin(phi)) + OA 

#print('new axis x ' + str(x))
#print('new axis y ' + str(y))
#print('new axis z ' + str(z)) 

with open ("coord.txt","w",encoding ="utf8") as f :
	f.write(str(x[0]) + " " + str(x[1]) + " " + str(x[2]) )
	f.write('\n')
	f.write(str(y[0]) + " " + str(y[1]) + " " + str(y[2]) )
	f.write('\n')
	f.write(str(z[0]) + " " + str(z[1]) + " " + str(z[2]) )
	f.write('\n')
