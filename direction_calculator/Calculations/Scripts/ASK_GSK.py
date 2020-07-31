#!/usr/bin/python3

####################################
###Translator from J2000 to Fixed###
####################################

from datetime import datetime
from math import *

om_Earth = 0.000072921158553

def alpha0(D1 = datetime(2000,1,1,0,0,0)):
    hh = int(D1.hour)
    mm = int(D1.minute)
    ss = int(D1.minute)

    day = int(D1.day)
    month = int(D1.month)
    year = int(D1.year)
    #delta_TAI_UTC =36
    #delta_TT_UT1 =68.4
    #delta_UT1_UTC =delta_TAI_UTC-delta_TT_UT1+32.184
    delta_UT1_UTC =0 #0.08
    #delta_UT1_UTC =-0.463326

    UTC = hh*60*60+mm*60+ss

    d = UTC/86400+367*year-(7*(year+(month+9) // 12)) // 4 + (275*month) // 9 + day - 730531.5
    S_mean =280.46061837+360.98564736629*d

    while(S_mean/2>180):
        S_mean = S_mean-360
    #writeln('1var:')
    #writeln('S_mean[deg] >', S_mean:15:10)
    seconds = S_mean/15*60*60
    hours = 0
    minutes = 0
    while(seconds>3600):
        seconds =seconds-3600
        hours =hours+1

    while(seconds>60):
        seconds =seconds-60
        minutes =minutes+1

    #в полночь совпадает с вариантом 3 (по UTC а не UT1), но в остальное время какая то хрень с кол-вом часов
    S_mean =24110.54841+8640184.812866*d/36525+0.093104*d*d/36525/36525-0.0000062*d*d*d/36525/36525/36525

    #в предположении что это формула для полуночной S_mean нужно сделать (теперь нет такой фигни с часами):
    S_mean =S_mean+UTC

    S_mean =S_mean*15/60/60
    while(S_mean/2>180):
        S_mean =S_mean-360

    return S_mean

def ASK_to_GSK(DateTime = datetime(2000,1,1,0,0,0),vecASK = [0.0,0.0,0.0,0.0,0.0,0.0]): # ASK[Vx[km/s],Vy[km/s],Vz[km/s],x[km],y[km],z[km]]
    Alpha = alpha0(DateTime)

    Alpha = radians(Alpha)

    vecGSK = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    vecGSK[0] =  vecASK[0] * cos(Alpha) + vecASK[1] * sin(Alpha)
    vecGSK[1] = -vecASK[0] * sin(Alpha) + vecASK[1] * cos(Alpha)
    vecGSK[2] =  vecASK[2]

    vecGSK[3] =  vecASK[3] * cos(Alpha) + vecASK[4] * sin(Alpha) + om_Earth * vecGSK[1]
    vecGSK[4] = -vecASK[3] * sin(Alpha) + vecASK[4] * cos(Alpha) - om_Earth * vecGSK[0]
    vecGSK[5] =  vecASK[5]

    return vecGSK  # GSK[Vx[km/s],Vy[km/s],Vz[km/s],x[km],y[km],z[km]]


intput_pipe_path = "/tmp/ASK_vector.txt"
output_pipe_path = "/tmp/GSK_vector.txt"

# for i in range(10):
#     with open("ASK_vector.txt", "r") as Rfile:
#         TextData = Rfile.read() # ASK[DateTime,Vx[km/s],Vy[km/s],Vz[km/s],x[km],y[km],z[km]]
#         vecASKText = TextData.split(" | ")
#         DT = datetime.strptime(vecASKText[0], '%Y-%m-%d %H:%M:%S')
#         vecASK = []
#         for i in range(1, len(vecASKText)):
#             vecASK.append(float(vecASKText[i]))
#         vecGSK = ASK_to_GSK(DT,vecASK)
#
#         razd = " | "
#         outData = str(DT)
#         for val in vecGSK:
#             outData += razd + str(val)
#
#         with open("GSK_vector.txt", "w") as Wfile:
#             Wfile.write(outData) # GSK[DateTime,Vx[km/s],Vy[km/s],Vz[km/s],x[km],y[km],z[km]]
#         Wfile.close()
#     Rfile.close()


while True:
    ASK_pipe = open(intput_pipe_path, "r")
    TextData = ASK_pipe.read()
    print("Received: " + TextData)
    ASK_pipe.close()
    vecASKText = TextData.split(" | ")
    DT = datetime.strptime(vecASKText[0], '%Y-%m-%d %H:%M:%S')
    vecASK = []
    for i in range(1, len(vecASKText)):
        vecASK.append(float(vecASKText[i]))
    vecGSK = ASK_to_GSK(DT, vecASK)

    razd = " | "
    outData = str(DT)
    for val in vecGSK:
        outData += razd + str(val)

    Outfile = open(output_pipe_path, "w")
    print("Sended: " +outData)
    Outfile.write(outData)
    Outfile.close()