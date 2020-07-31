# from Int import Int_ASK
from datetime import datetime
# from ASK_GSK import *

# Calc = Int_ASK(datetime(2020,7,25,0,0,0),[0.0,4.210800438221973,6.459354829086378,6713.724608199999,0.0,0.0])
# Calc.setEnd_DateTime(datetime(2020,7,25,1,0,0))
# Calc.Calc()
# Calc.Step()

# for m in range(1,12):
# for dd in range(1,31):
#     for hh in range(0,23):
#         DT = datetime(2019,1,dd,hh,0,0)
#         print(str(DT)+" : "+str(alpha0(DT)))

import dateparser
#coordinates

timedate = '31 июля 2020 г. 9:28:14'
import datetime
result = dateparser.parse(timedate, languages=['ru'])
print(result)