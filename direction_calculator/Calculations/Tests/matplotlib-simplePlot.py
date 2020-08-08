#!/usr/bin/python3
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

# ------------------------------------------------------------------------------
# Adapted from https://matplotlib.org/3.3.0/gallery/lines_bars_and_markers/
#   simple_plot.html#sphx-glr-gallery-lines-bars-and-markers-simple-plot-py
#
                                                             # data for plotting
t = np.arange(0.0, 2.0, 0.01)
s = 1 + np.sin(2 * np.pi * t)
                                                                       # drawing
fig, ax = plt.subplots()
ax.plot(t, s)
                                                              # labels and grids
ax.set(xlabel='time (s)', ylabel='voltage (mV)',
       title='About as simple as it gets, folks')
ax.grid()
                                                     # screen and file rendering
fig.savefig("matplotlib-simplePlot.png")
plt.show()
