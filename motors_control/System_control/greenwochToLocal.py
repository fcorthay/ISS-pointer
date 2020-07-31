import os , sys
from funcMagPos import ToLocalCoord
from funcMagPos import read_greenwich_coord_file

local_coord_file = "/tmp/ISS_coord_local.txt"

print('Starting transformation to local coordinates')
try:
    os.mkfifo(local_coord_file)
except:
    pass
else:
    print("coordinates FIFO {} has been created".format(local_coord_file))
                                                                     # open file
print('Opening pipe')
print('Waiting for somebody to read')
try:
    tick_pipe = open(local_coord_file, "w")
except Exception as e:
    print(e)
    sys.exit()

vx, vy, vz = ToLocalCoord(read_greenwich_coord_file(), "sion")

tick_pipe.write(str(vx))
tick_pipe.write(" ")
tick_pipe.write(str(vy))
tick_pipe.write(" ")
tick_pipe.write(str(vz))
tick_pipe.write(" ")

tick_pipe.close()
