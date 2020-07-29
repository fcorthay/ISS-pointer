from Int import Int_ASK
from datetime import datetime

Calc = Int_ASK(datetime(2020,7,25,0,0,0),[0.0,4.210800438221973,6.459354829086378,6713.724608199999,0.0,0.0])
Calc.setEnd_DateTime(datetime(2020,7,25,1,0,0))
Calc.Calc()
#Calc.Step()

