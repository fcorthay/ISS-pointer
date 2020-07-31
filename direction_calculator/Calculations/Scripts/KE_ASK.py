#!/usr/bin/python3

#################################################
###Translator from Keplerian elements to J2000###
#################################################

from math import *
import dateparser
from datetime import datetime

Earth_mu = 398600.4481
def KE_to_ASK(KE_vector = [0.0,0.0,0.0,0.0,0.0,0.0], deg_rad = "r"):
    a,e,inc,RAAN,om,u = KE_vector

    # __перевод в радианы из градусов___________________________________________
    if deg_rad != "r":
        u = radians(u)
        inc = radians(inc)
        om = radians(om)
        RAAN = radians(RAAN)

    # _ToO_______________________________________________________________

    if (e == 0.0):# Надо изменить условие (наверное)
        ToO = 0
    elif ((e > 0) and (e < 1)):
        ToO = 1
    elif (e == 1.0):
        ToO = 2
    elif (e > 1):
        ToO = 3

    # ___p____________________________________________________________________

    if (ToO == 0):  # Надо изменить условие (наверное)
        p = a
    elif (ToO == 1):
        p = a * (1 - pow(e, 2))
    elif (ToO == 2):
        p = 0
    elif (ToO == 3):
        p = a * (pow(e, 2) - 1)

    # __teta____________________________________________________________________
    teta = u - om
    teta = check_f_rad(teta)

    # __r____________________________________________________________________

    r = p / (1 + e * cos(teta))

    # __r0, n0____________________________________________________________________
    r0,n0 = [],[]

    r0.append(cos(RAAN) * cos(u) - sin(RAAN) * sin(u) * cos(inc))
    r0.append(sin(RAAN) * cos(u) + cos(RAAN) * sin(u) * cos(inc))
    r0.append(sin(u)    * sin(inc))
    # r0.normalize()
    n0.append( -cos(RAAN) * sin(u) - sin(RAAN) * cos(u) * cos(inc))
    n0.append( -sin(RAAN) * sin(u) + cos(RAAN) * cos(u) * cos(inc))
    n0.append( cos(u) * sin(inc))
    # n0.normalize() # может нужно нормализовывать?
    # __x, y, z_________________________________________________________________

    vR = []
    for i in range(3):
        vR.append(r * r0[i])
    # --------------------------------------------------------------------------

    # __vr, vn______________________________________________________________________
    Vr = sqrt(Earth_mu / p) * e * sin(teta)
    Vn = sqrt(Earth_mu / p) * (1 + e * cos(teta)) # vn = c / r

    # __v__________________________________________________________________________
    vV = []
    for i in range(3):
        vV.append(Vr * r0[i] + Vn * n0[i])

    vecASK = vV.copy()
    vecASK.extend(vR)
    return vecASK

def check_f_rad(f):
    if (f < 0.0):
        f += 2.0*pi

    if (f > 2*pi):
        f -= 2.0*pi

    return f


with open("KE_vector.txt", "r", encoding="utf-8") as Rfile:
    TextData = Rfile.read() # KE[DateTime,a[km],e[-],inc[deg],RAAN[deg],om[deg],u[deg]
    vecKEText = TextData.split(" | ")
    DT = dateparser.parse(vecKEText[0], languages=['ru'])
    vecKE = []
    for i in range(1, len(vecKEText)):
        vecKE.append(float(vecKEText[i]))
    vecASK = [0.0,0.0,0.0,0.0,0.0,0.0]
    vecASK = KE_to_ASK(vecKE,"d")

    razd = " | "
    outData = str(DT)
    for val in vecASK:
        outData += razd + str(val)

    with open("ASKinit_vector.txt", "w") as Wfile:
        Wfile.write(outData) # ASK[DateTime,Vx[km/s],Vy[km/s],Vz[km/s],x[km],y[km],z[km]]
    Wfile.close()
Rfile.close()
