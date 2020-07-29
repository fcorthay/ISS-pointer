from math import *


Earth_mu = 398600.4481
E = 2.634*10**10

def f_dVx_dt(vec_r_ask = [0.0,0.0,0.0]): #dvx/dt
    x,y,z = vec_r_ask
    r = sqrt(x**2+y**2+z**2)
    return -Earth_mu*x/r**3+(5*E*z**2*x/r**7-E*x/r**5)

def f_dVy_dt(vec_r_ask = [0.0,0.0,0.0]): #dvy/dt
    x,y,z = vec_r_ask
    r = sqrt(x**2+y**2+z**2)
    return -Earth_mu*y/r**3+(5*E*z**2*y/r**7-E*y/r**5) #-mu*y/power(r,3)+5*E*power(z,2)*y/power(r,7)-E*y/power(r,5);

def f_dVz_dt(vec_r_ask = [0.0,0.0,0.0]): #dvz/dt
    x,y,z = vec_r_ask
    r = sqrt(x**2+y**2+z**2)
    return -Earth_mu*z/r**3+(5*E*z**3/r**7-3*E*z/r**5) #-mu*z/power(r,3)+(5*E*power(z,3)/power(r,7)-3*E*z/power(r,5))

def f_dx_dt (Vx = 0.0): #dx/dt
    return Vx
def f_dy_dt (Vy = 0.0): #dy/dt
    return Vy
def f_dz_dt (Vz = 0.0): #dz/dt
    return Vz