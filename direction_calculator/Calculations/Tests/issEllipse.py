#!/usr/bin/python3
import matplotlib
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import numpy as np

# ------------------------------------------------------------------------------
# constants
#
perigee_distance = 418.0E3
perigee_distance = 218.0E3
apogee_distance = 420.0E3

a = (perigee_distance + apogee_distance) / 2
b = np.sqrt(perigee_distance * apogee_distance)
c = (apogee_distance - perigee_distance) / 2
p = b**2 / a
e = c / a

mu = 0.986004418E14
A = a*b*np.pi

distance_scaling_factor = 1E3
display_max_distance = 500E3
display_increment = 100E3
point_nb = 1000

# ------------------------------------------------------------------------------
# ISS ellipse
#
                                                                # elliptic curve
theta = np.arange(0.0, 2.0*np.pi, 2.0*np.pi/point_nb)
r = p / (1 + e*np.cos(theta))
                                                               # ellipse drawing
ellipse_plot = pyplot.subplot(311, projection='polar')
ellipse_plot.plot(theta, r/distance_scaling_factor)
                                                              # grids and labels
ellipse_plot.set_rmax(display_max_distance/distance_scaling_factor)
ellipse_plot.set_rticks(
	np.arange(
		display_increment, display_max_distance, display_increment
	)/distance_scaling_factor
)
ellipse_plot.grid(True)
ellipse_plot.set_title("ISS elliptic trajectory [km]")

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
                                                               # ellipse drawing
surface_plot = pyplot.subplot(312)
surface_plot.plot(theta*180/np.pi, A1_A2/A)
                                                              # grids and labels
surface_plot.set_xlim(0, theta[-1]*180/np.pi)
surface_plot.xaxis.set_major_locator(ticker.MultipleLocator(45))
surface_plot.set_ylim(0, 1)
surface_plot.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
surface_plot.grid()
surface_plot.set(
	xlabel='angle',
	ylabel='relative surface',
    title='Swept surface'
)

# ------------------------------------------------------------------------------
# Display results
#
                                                     # screen and file rendering
#fig.savefig("issEllipse.png")
pyplot.show()
