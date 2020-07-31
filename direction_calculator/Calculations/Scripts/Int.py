#!/usr/bin/python3

###########################
###Trajectory Calculator###
###########################

from datetime import datetime
from datetime import timedelta
import dateparser
import numpy as np
from int_func import *

tick_pipe_filespec = "/tmp/tick.txt"


class Int_ASK:
    def __init__(self,InitDateTime = datetime(2020,7,25,0,0,0),InitASK = [0.0,0.0,0.0,0.0,0.0,0.0], # ASK[Vx[km/s],Vy[km/s],Vz[km/s],x[km],y[km],z[km]]
                 Settings = [30,0,0,False], ExportSettings = [0]):
        self.DT0 = InitDateTime
        self.DTcur = InitDateTime
        self.DTtemp = InitDateTime

        self.vec0 = InitASK.copy()
        self.veccur = InitASK.copy()
        self.vectemp = InitASK.copy()
        self.curStepnum = 0
        self.K = np.zeros((4,6))

        self.dt = Settings[0]           #Integration Step
        self.IntStopMode = Settings[1]  # 0 - Calc to Ending,1 - Calc until the script stopping
        self.IntDelayMode = Settings[2] # 0 - Calc without delays ,1 - Calc with delays
        self.IntReadfromFile = Settings[3] # False|True - Read DateTime

        self.IntExpChanal = ExportSettings[0] # 0 - Export to Terminal ,1 - Export to File

        self.EoR = False
        self.EoS = True


        self.EndVariant = 2 # 0 - End with any, 1 - End with StepsCount, 2 - End with DateTime
        self.EndSC = 1000
        self.EndDT = self.DT0 + timedelta(days  =(int(round(1))))

    def restart(self):
        self.DTcur = self.DT0
        self.DTtemp = self.DT0

        self.veccur = self.vec0
        self.vectemp = self.vec0
        self.curStepnum = 0
        self.K = np.zeros((4,6))

        self.EoR = False
        self.EoS = True

        self.EndVariant = 2 # 0 - End with any, 1 - End with StepsCount, 2 - End with DateTime
        self.EndSC = 1000
        self.EndDT = datetime(2020,7,26,0,0,0)


    def setEnd_StepCount(self, StepCount):
        self.EndSC = StepCount

        if self.curStepnum < self.EndSC:
            self.EoR = False

    def setEnd_DateTime(self, DateTime):
        self.EndDT = DateTime

        if self.DTcur < self.EndDT:
            self.EoR = False

    def Calc(self):
        self.writeSData()
        while(not self.EoR):
            self.Step()
        self.writeSData()


    def Step(self):
#        self.StepStart()
        self.RaschetStep()
        self.Proverka()
        self.StepEnd()

    def RaschetStep(self):
        for i in range(4):
            self.Calc_K(i)

    def RrightParts(self):
        dval_dt = []
        vecR,vecV =[],[]
        for i in range(3):
            vecR.append(self.vectemp[i+3])
            vecV.append(self.vectemp[i])

        dval_dt.append(f_dVx_dt(vecR))
        dval_dt.append(f_dVy_dt(vecR))
        dval_dt.append(f_dVz_dt(vecR))
        dval_dt.append(f_dx_dt(vecV[0]))
        dval_dt.append(f_dy_dt(vecV[1]))
        dval_dt.append(f_dz_dt(vecV[2]))
        return dval_dt

    def Calc_K(self,num_K):
        dval_dt = self.RrightParts().copy()

        self.K[num_K] = dval_dt.copy()

        if (num_K < 2):
            self.Under_K_Calc(num_K, 0.5)
        else:
            self.Under_K_Calc(num_K, 1)

    def Under_K_Calc(self, num_K,mn):
        sv_ASK_step = []

        K_v = np.zeros(6)
        if (num_K < 3):
            K_v = self.K[num_K]

        if (num_K == 3):
            for i in range(6):
                K_v[i] = self.K[0][i] + self.K[1][i]*2 + self.K[2][i]*2 + self.K[3][i]
                K_v[i] /= 6.0

        for num in range(6):
            sv_ASK_step.append(self.veccur[num] + self.dt * K_v[num] * mn)

        self.DTtemp = self.DTcur + timedelta(milliseconds=(int(round(self.dt * mn * 1000))))
        self.vectemp = sv_ASK_step.copy()

    def PredRaschet(self):
        pass

    def Proverka(self):
        self.CheckEndofstep()
        self.CheckEndofRaschet()


    def StepEnd(self):
        if (self.EoS):
            self.veccur = self.vectemp.copy()
            self.DTcur = self.DTtemp
            #self.writeSData()
            self.curStepnum += 1

    def CheckEndofstep(self):
        pass

    def CheckEndofRaschet(self):
        if (self.curStepnum >= self.EndSC and (self.EndVariant <= 1 )):
            self.EoR = True

        if (self.DTtemp >= self.EndDT and (self.EndVariant == 0 or self.EndVariant == 2)):
            self.EoR = True

    def writeSData(self):
        razd = " | "
        outData = str(self.DTcur)
        for val in self.veccur:
            outData += razd + str(val)

        if self.IntExpChanal == 0:
            print(outData)
        elif self.IntExpChanal == 1:
            with open("ASK_vector.txt", "w") as file:
                file.write(outData)
            print(outData)
            file.close()

with open("ASKinit_vector.txt", "r", encoding="utf-8") as Rfile:
    TextData = Rfile.read() # ASK[DateTime,a[km],e[-],inc[deg],RAAN[deg],om[deg],u[deg]
    vecASK0Text = TextData.split(" | ")
    DT0 = dateparser.parse(vecASK0Text[0])
    vecASK0 = []
    for i in range(1, len(vecASK0Text)):
        vecASK0.append(float(vecASK0Text[i]))
    Rfile.close()


Int = Int_ASK(DT0,vecASK0,[0.1,0,0,False],[0])
Int = Int_ASK(DT0,vecASK0,[0.1,0,0,False],[1])
while True:
    tick_pipe = open(tick_pipe_filespec, "r")
    textDateTime = tick_pipe.read()
    print("Received: " + textDateTime)
    tick_pipe.close()
    Int.setEnd_DateTime(datetime.strptime(textDateTime, '%Y-%m-%d %H:%M:%S'))
    Int.Calc()
    prtextDateTime = textDateTime
