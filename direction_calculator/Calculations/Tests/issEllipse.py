#!/usr/bin/python3
import sys, os
import math
import numpy as np
import matplotlib.pyplot as pyplot
import matplotlib.ticker as ticker
import datetime
import csv

# ------------------------------------------------------------------------------
# constants
#
exaggerate_ellipse = True
#exaggerate_ellipse = False
perigee_from_surface = 418.0E3
apogee_from_surface = 420.0E3
earth_radius = 6.3781E6
if exaggerate_ellipse:
    earth_radius = 100E3
    apogee_from_surface = apogee_from_surface - earth_radius
    perigee_from_surface = 218.0E3 - earth_radius
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

inclination = 51.6462/180 * math.pi
right_ascension = 60.7322/180 * math.pi

point_nb = 1000
distance_scaling_factor = 1E3
distance_scale = 'km'
display_max_distance = 8000E3
display_increment = 2000E3
if exaggerate_ellipse:
    display_max_distance = 500E3
    display_increment = 100E3
to_deg = 180/math.pi
earth_color = 'lightskyblue'
earth_projection_color = 'lightblue'
trajectory_color = 'darkgrey'
trajectory_projection_color = 'lightgrey'
script_pathname = os.path.dirname(sys.argv[0])  

INDENT = '  '

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

#   print("{:.3f} -> {:.3f}".format(t, angle))
    return(angle)

# ==============================================================================
# Print information
#
print('Estimating ISS elliptic trajectory')
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

# ==============================================================================
# ISS ellipse
#
print()
print('Plotting elliptic trajectories')
print(INDENT + 'polar plot')
                                                                # prepare figure
pyplot.figure(1, figsize=(6, 9))
pyplot.subplots_adjust(hspace = 0.5)
                                                                # elliptic curve
theta = np.arange(0.0, 2.0*np.pi, 2.0*np.pi/point_nb)
r = p / (1 + e*np.cos(theta))
earth_shape = earth_radius * np.ones(len(r))
                                                        # plot satellite ellipse
ellipse_plot = pyplot.subplot(311, projection='polar')
ellipse_plot.plot(theta, r/distance_scaling_factor, color=trajectory_color)
                                                             # plot earth circle
ellipse_plot.plot(theta, earth_shape/distance_scaling_factor, color=earth_color)
ellipse_plot.fill_between(
    theta, earth_shape/distance_scaling_factor,
    color=earth_color
)
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
print(INDENT + 'surface as a function of the angle')
                                                                      # triangle
A1 = r**2/4 * (np.sin(2*theta))
                                                                      # integral
x_a = (c + r*np.cos(theta)) / a
A2 = a*b/2 * (np.pi/2 - x_a*np.sqrt(1-x_a**2) - np.arcsin(x_a))
A1_A2 = A1 + A2
A1_A2[int(len(A1_A2)/2):] = 2*A1_A2[int(len(A1_A2)/2)] - A1_A2[int(len(A1_A2)/2)-1::-1]
#A1_A2[int(len(A1_A2)/2):] = -A1_A2[int(len(A1_A2)/2)-1::-1]
                                                       # plot normalized surface
surface_plot = pyplot.subplot(312)
surface_plot.plot(theta*180/np.pi, A1_A2/ellipse_surface)
                                                              # grids and labels
surface_plot.set_xlim(0, 360)
surface_plot.xaxis.set_major_locator(ticker.MultipleLocator(45))
surface_plot.set_ylim(0, 1)
surface_plot.yaxis.set_major_locator(ticker.MultipleLocator(0.25))
surface_plot.grid()
surface_plot.set(
    xlabel='angle []',
    ylabel='relative surface',
    title='Swept surface as a function of the angle'
)

# ------------------------------------------------------------------------------
# Angle as function of time
#
print(INDENT + 'angle as a function of time')
#print(theta[1]/(rotation_period*A1_A2[1]/ellipse_surface))
#print(max_angle_slope)
                                                               # linear time set
time = np.arange(0.0, rotation_period, rotation_period/point_nb)
                                                             # angle calculation
angles_t = np.zeros(len(time))
for sample in range(len(time)):
    angles_t[sample] = angle_at_time(time[sample])
                                                          # plot normalized time
angle_plot = pyplot.subplot(313)
angle_plot.plot(time, angles_t*180/math.pi)
                                                              # grids and labels
angle_plot.set_xlim(0, time[-1])
angle_plot.xaxis.set_major_locator(ticker.MultipleLocator(rotation_period/8))
angle_plot.set_ylim(0, 360)
angle_plot.yaxis.set_major_locator(ticker.MultipleLocator(60))
angle_plot.grid()
angle_plot.set(
    xlabel='time [s]',
    ylabel='angle []',
    title='Angle as a function of time'
)
pyplot.savefig(script_pathname + '/issEllipse-1.png')

# ==============================================================================
# 3D plot
#
print()
print('Plotting 3D trajectories')
print(INDENT + '3D ellipse')
                                                         # prepare second window
pyplot.figure(2, figsize=(6, 9))
pyplot.subplots_adjust(hspace = 0.5)
space_plot = pyplot.subplot(311, projection='3d')
plot_limits = [
    -display_max_distance/distance_scaling_factor,
    display_max_distance/distance_scaling_factor
]
space_plot.set_xlim3d(plot_limits)
space_plot.set_ylim3d(plot_limits)
space_plot.set_zlim3d(plot_limits)
                                  # satellite trajectory on the equatorial plane
radius_t = p / (1 + e*np.cos(angles_t))
flat_x = radius_t * np.cos(angles_t)
flat_y = radius_t * np.sin(angles_t)
flat_z = np.zeros(len(flat_x))
#space_plot.plot(flat_x, flat_y, flat_z)
                                                  # define the rotation matrices
inclination_rotation = np.array([
    [1,           0          ,           0           ],
    [0, math.cos(inclination), -math.sin(inclination)],
    [0, math.sin(inclination),  math.cos(inclination)]
])
ascension_rotation = np.array([
    [math.cos(right_ascension), -math.sin(right_ascension), 0],
    [math.sin(right_ascension),  math.cos(right_ascension), 0],
    [            0            ,              0            , 1]
])
                                                           # calculate rotations
rotated_x = np.zeros(len(flat_x))
rotated_y = np.zeros(len(flat_x))
rotated_z = np.zeros(len(flat_x))
for index in range(len(flat_x)):
    flat_coordinates = np.array([[
        flat_x[index], flat_y[index], flat_z[index]
    ]]).transpose()
    rotated_coordinates = np.dot(inclination_rotation, flat_coordinates)
    rotated_coordinates = np.dot(ascension_rotation, rotated_coordinates)
    rotated_coordinates = rotated_coordinates.transpose()[0]
    rotated_x[index] = rotated_coordinates[0]
    rotated_y[index] = rotated_coordinates[1]
    rotated_z[index] = rotated_coordinates[2]
                                                               # plot trajectory
space_plot.plot(
    rotated_x/distance_scaling_factor,
    rotated_y/distance_scaling_factor,
    rotated_z/distance_scaling_factor,
    color=trajectory_color
)
                                                             # plot earth sphere
u = np.linspace(0, 2 * np.pi, point_nb)
v = np.linspace(0, np.pi, point_nb)
earth_x = earth_radius * np.outer(np.cos(u), np.sin(v))
earth_y = earth_radius * np.outer(np.sin(u), np.sin(v))
earth_z = earth_radius * np.outer(np.ones(np.size(u)), np.cos(v))
space_plot.plot_surface(
    earth_x/distance_scaling_factor,
    earth_y/distance_scaling_factor,
    earth_z/distance_scaling_factor,
    color=earth_color
)
space_plot.set(title='Inclination and ascension')

# ------------------------------------------------------------------------------
# Projections on the side planes
#
                                                         # trajectory projection
projected_trajectory = np.ones(len(flat_x)) * display_max_distance
space_plot.plot(
    -projected_trajectory/distance_scaling_factor,
    rotated_y/distance_scaling_factor,
    rotated_z/distance_scaling_factor,
    color=trajectory_projection_color
)
space_plot.plot(
    rotated_x/distance_scaling_factor,
    projected_trajectory/distance_scaling_factor,
    rotated_z/distance_scaling_factor,
    color=trajectory_projection_color
)
space_plot.plot(
    rotated_x/distance_scaling_factor,
    rotated_y/distance_scaling_factor,
    -projected_trajectory/distance_scaling_factor,
    color=trajectory_projection_color
)
                                                              # earth projection
earth_x = earth_radius/distance_scaling_factor * np.cos(theta)
earth_y = earth_radius/distance_scaling_factor * np.sin(theta)
earth_z = -display_max_distance/distance_scaling_factor * np.ones(len(theta))
space_plot.plot(earth_x, earth_y, earth_z, color=earth_projection_color)
space_plot.plot(earth_z, earth_x, earth_y, color=earth_projection_color)
space_plot.plot(earth_y, -earth_z, earth_x, color=earth_projection_color)

# ------------------------------------------------------------------------------
# Longitude and latitude
#
print(INDENT + 'longitudes and latitudes')
                                                    # equirectangular projection
longitude = np.arctan2(rotated_y, rotated_x)
latitude = np.arctan(
    rotated_z / np.sqrt(np.square(rotated_x)+np.square(rotated_y))
)
long_lat_plot = pyplot.subplot(312)
long_lat_plot.plot(angles_t*to_deg, longitude*to_deg)
long_lat_plot.plot(angles_t*to_deg, latitude*to_deg)
                                                              # grids and labels
long_lat_plot.set_xlim(0, 360)
long_lat_plot.xaxis.set_major_locator(ticker.MultipleLocator(30))
long_lat_plot.set_ylim(-180, 180)
long_lat_plot.yaxis.set_major_locator(ticker.MultipleLocator(60))
long_lat_plot.grid()
long_lat_plot.set(
    xlabel='ellipse angle [°]',
    ylabel='longitude and latitude [°]',
    title='Longitude, latitude'
)

# ------------------------------------------------------------------------------
# Equirectangular projection
#
print(INDENT + 'equirectangular projection')
                                                    # equirectangular projection
longitude = np.unwrap(np.arctan2(rotated_y, rotated_x))
latitude = np.arctan(
    rotated_z / np.sqrt(np.square(rotated_x)+np.square(rotated_y))
)
equirectangular_plot = pyplot.subplot(313)
equirectangular_plot.plot(longitude*to_deg, latitude*to_deg)
                                                              # grids and labels
equirectangular_plot.xaxis.set_major_locator(ticker.MultipleLocator(30))
equirectangular_plot.set_ylim(-90, 90)
equirectangular_plot.yaxis.set_major_locator(ticker.MultipleLocator(30))
equirectangular_plot.grid()
equirectangular_plot.set(
    xlabel='longitude [°]',
    ylabel='latitude [°]',
    title='Equirectangular projection in earth-centered inertial coordinates'
)
                                                     # write coordinates to file
print()
print('Writing coordinates to file')
CSV_file_spec = script_pathname + '/issEllipse.csv'
CSV_file = open(CSV_file_spec, 'w')
with CSV_file:
    writer = csv.writer(CSV_file)
    for index in range(len(time)):
        writer.writerow([
            time[index],
            rotated_x[index],
            rotated_y[index],
            rotated_z[index]
        ])
CSV_file.close

# ==============================================================================
# Display results
#
print()
print('Rendering')
                                                     # screen and file rendering
pyplot.savefig(script_pathname + '/issEllipse-2.png')
pyplot.show()
