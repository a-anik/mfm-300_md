#!/usr/bin/env python

import sys
import numpy as np

a = np.loadtxt(sys.argv[1], delimiter=' ')   # expects anglesXYZ.dat file: time, angleX, angleY, angleZ

x = np.cos(np.deg2rad(a[:,1]))
y = np.cos(np.deg2rad(a[:,2]))
phi = np.rad2deg(np.arctan2(x, y))

hist, bins = np.histogram(phi, range=[-180, 180], bins=72, density=True)
bincenters = 0.5*(bins[1:]+bins[:-1])

np.savetxt(sys.stdout, np.array((bincenters, hist)).T, fmt="%g", delimiter=' ')
