#!/usr/bin/python3
import sys, os
import math
import numpy as np
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import datetime

# ------------------------------------------------------------------------------
# constants
#
exaggerate_ellipse = True
exaggerate_ellipse = False
perigee_from_surface = 418.0E3
apogee_from_surface = 420.0E3
earth_radius = 6.3781E6
if exaggerate_ellipse:
	perigee_from_surface = 218.0E3
	earth_radius = 0
perigee_from_center = earth_radius + perigee_from_surface
apogee_from_center = earth_radius + apogee_from_surface

a = (perigee_from_center + apogee_from_center) / 2
b = np.sqrt(perigee_from_center * apogee_from_center)
c = (apogee_from_center - perigee_from_center) / 2
p = b**2 / a
e = c / a

# G = 6.67408E-11
# M = 5.9736E24
# mu = G*M
mu = 3.986004418E14
ellipse_surface = a*b*np.pi
rotation_period = 2 * np.pi * math.sqrt(a**3/mu)
delta_angle = 2*math.pi / 1000
max_angle_slope = 2 * ellipse_surface \
    / (rotation_period * perigee_from_center**2)

point_nb = 1000
distance_scaling_factor = 1E3
distance_scale = 'km'
display_max_distance = 8000E3
display_increment = 2000E3
if exaggerate_ellipse:
	display_max_distance = 500E3
	display_increment = 100E3

INDENT = '  '

pyplot.figure(figsize=(6, 9))
pyplot.subplots_adjust(hspace = 0.5)

# ==============================================================================
# Procedures and functions
#
def radius_at_angle(theta):
	r = p / (1 + e*math.cos(theta))
	return(r)

def time_at_angle(theta):
	theta_upper = theta
	if theta > math.pi:
		theta_upper = 2*math.pi - theta

	A1 = radius_at_angle(theta_upper)**2/4 * math.sin(2*theta_upper)
	x_a = (c + radius_at_angle(theta_upper)*math.cos(theta_upper)) / a
	A2 = a*b/2 * (math.pi/2 - x_a*math.sqrt(1-x_a**2) - math.asin(x_a))
	t = rotation_period * (A1 + A2)/ellipse_surface

	if theta > math.pi:
		t = rotation_period - t

	return(t)

def angle_at_time(t):
                                                       # define global variables
	global previous_time, previous_angle
	if t == 0:
		angle = 0.0
	else:
		angle_over = previous_angle + max_angle_slope * (t - previous_time)
		t_over = time_at_angle(angle_over)
		angle = previous_angle + \
			(angle_over - previous_angle) * (t - previous_time) \
			/ (t_over - previous_time)
                                                         # store previous values
	previous_time = t
	previous_angle = angle

#	print("{:.3f} -> {:.3f}".format(t, angle))
	return(angle)

# ==============================================================================
# Program start
#

# ------------------------------------------------------------------------------
# Print information
#
print('ISS elliptic trajectory')
print(INDENT + "perigee from earth surface : {:.1f} {}".format(
	perigee_from_center / distance_scaling_factor,
	distance_scale
))
print(INDENT + "apogee from earth surface  : {:.1f} {}".format(
	apogee_from_center / distance_scaling_factor,
	distance_scale
))
print()
print(INDENT + "a : {:.1f} {}".format(
	a / distance_scaling_factor,
	distance_scale
))
print(INDENT + "b : {:.1f} {}".format(
	b / distance_scaling_factor,
	distance_scale
))
print(INDENT + "c : {:.1f} {}".format(
	c / distance_scaling_factor,
	distance_scale
))
print()
print(INDENT + "A : {:.1f} {}2".format(
	ellipse_surface / distance_scaling_factor**2,
	distance_scale
))
print(INDENT + "T : {:d} s = {}".format(
	round(rotation_period),
	datetime.timedelta(seconds = rotation_period)
))

# ------------------------------------------------------------------------------
# ISS ellipse
#
                                                                # elliptic curve
theta = np.arange(0.0, 2.0*np.pi, 2.0*np.pi/point_nb)
r = p / (1 + e*np.cos(theta))
earth_shape = earth_radius * np.ones(len(r))
                                                               # ellipse drawing
ellipse_plot = pyplot.subplot(311, projection='polar')
ellipse_plot.plot(theta, r/distance_scaling_factor)
ellipse_plot.plot(theta, earth_shape/distance_scaling_factor)
                                                              # grids and labels
ellipse_plot.set_rmax(display_max_distance/distance_scaling_factor)
ellipse_plot.set_rticks(
	np.arange(
		display_increment, display_max_distance, display_increment
	)/distance_scaling_factor
)
ellipse_plot.grid(True)
ellipse_plot.set_title("Elliptic trajectory [km]")

# ------------------------------------------------------------------------------
# Swept surface
#
                                                                      # triangle
A1 = r**2/4 * (np.sin(2*theta))
                                                                      # integral
x_a = (c + r*np.cos(theta)) / a
A2 = a*b/2 * (np.pi/2 - x_a*np.sqrt(1-x_a**2) - np.arcsin(x_a))
A1_A2 = A1 + A2
A1_A2[int(len(A1_A2)/2):] = 2*A1_A2[int(len(A1_A2)/2)] - A1_A2[int(len(A1_A2)/2)-1::-1]
#A1_A2[int(len(A1_A2)/2):] = -A1_A2[int(len(A1_A2)/2)-1::-1]
                                                          # plot normalized time
surface_plot = pyplot.subplot(312)
surface_plot.plot(theta*180/np.pi, A1_A2/ellipse_surface)
                                                              # grids and labels
surface_plot.set_xlim(0, 360)
surface_plot.xaxis.set_major_locator(ticker.MultipleLocator(45))
surface_plot.set_ylim(0, 1)
surface_plot.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
surface_plot.grid()
surface_plot.set(
	xlabel='angle [°]',
	ylabel='relative surface',
    title='Swept surface as a function of the angle'
)

# ------------------------------------------------------------------------------
# Angle as function of time
#
#print(theta[1]/(rotation_period*A1_A2[1]/ellipse_surface))
#print(max_angle_slope)
                                                               # linear time set
time = np.arange(0.0, rotation_period, rotation_period/point_nb)
                                                             # angle calculation
angles = np.zeros(len(time))
for sample in range(len(time)):
	angles[sample] = angle_at_time(time[sample])
                                                          # plot normalized time
angle_plot = pyplot.subplot(313)
angle_plot.plot(time, angles*180/math.pi)
                                                              # grids and labels
angle_plot.set_xlim(0, time[-1])
angle_plot.xaxis.set_major_locator(ticker.MultipleLocator(rotation_period/8))
angle_plot.set_ylim(0, 360)
angle_plot.yaxis.set_major_locator(ticker.MultipleLocator(60))
angle_plot.grid()
angle_plot.set(
	xlabel='time [s]',
	ylabel='angle [°]',
    title='Angle as a function of time'
)

# ------------------------------------------------------------------------------
# Display results
#

                                                     # screen and file rendering
pathname = os.path.dirname(sys.argv[0])  
pyplot.savefig(pathname + '/issEllipse.png')
pyplot.show()
