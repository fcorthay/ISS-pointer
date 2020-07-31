import numpy as np
import math
import constants

# ------------------------------------------------------------------------------
def read_coordinates(line) :
    line_elements = line.split(constants.SEPARATOR)
    x = float(line_elements[-3])
    y = float(line_elements[-2])
    z = float(line_elements[-1])
    return (x, y, z)

# ------------------------------------------------------------------------------
def greenwich_to_local(x_g, y_g, z_g) :
    longi = constants.LOCAL_LONGITUDE
    lat   = constants.LOCAL_LATITUDE
    M = np.matrix([
        [
            0.5*(math.cos(longi+lat)+math.cos(longi-lat)),
            -math.sin(longi),
            0.5*(math.sin(longi+lat)-math.cos(longi-lat))
        ],
        [
            0.5*(math.sin(longi+lat)+math.sin(longi-lat)),
            math.cos(longi),
            0.5*(-math.cos(longi+lat)+math.cos(longi-lat))
        ],
        [
            -math.sin(lat),
            0,
            math.cos(lat)
        ]
    ])
    x_l = M[0,0]*x_g + M[0,1]*y_g  + M[0,2]*z_g
    y_l = M[1,0]*x_g + M[1,1]*y_g  + M[1,2]*z_g
    z_l = M[2,0]*x_g + M[2,1]*y_g  + M[2,2]*z_g
    return (x_l, y_l, z_l)

# ------------------------------------------------------------------------------
def norm (x) :
    n=0
    for i in range(0,2) :
            n+=x[i]**2
    return math.sqrt(n)

# ------------------------------------------------------------------------------
def local_to_angles(ai) :
    x = constants.LOCAL_X_AXIS
    z = constants.LOCAL_Z_AXIS
    phi1,phi2 = 0,0
    
    for i in range(0,3) :
        phi1+=x[i]*ai[i]/(norm(x)*norm(ai))
        phi2+=z[i]*ai[i]/(norm(z)*norm(ai))
    phi1 = 360/(2*math.pi)*(math.pi/2 - math.acos(phi1))
    phi2 = 360/(2*math.pi)*(math.pi/2 - math.acos(phi1))
#    phi2 = 360/(2*math.pi)*(math.pi/2 - math.acos(phi2))
    return phi1,phi2
