#!/usr/bin/env python

import argparse
import MDAnalysis as mda
import numpy as np
import time


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Histograms of angles with axes')
    parser.add_argument('-s', dest='topfile', nargs='?', default='conf.pdb', help='topology file (.pdb)')
    parser.add_argument('-f', dest='trajfile', nargs='?', default='traj.xtc', help='trajectory file')
    parser.add_argument('-o', dest='histfile', nargs='?', default='histCosXYZ.dat', metavar='histCosXYZ.dat', help='output histogram file')
    parser.add_argument('-oa', dest='anglesfile', nargs='?', default=None, const='anglesXYZ.dat', metavar='anglesXYZ.dat', help='output file with angles')
    parser.add_argument('-rand', type=float, nargs='?', default=0, const=0.005, metavar='0.005', help='amplitude for randomizing coordinates')
    parser.add_argument('-bins', type=int, default=50, help='Number of bins')
    args = parser.parse_args()

    u = mda.Universe(args.topfile, args.trajfile, refresh_offsets=False)

    oatom = u.select_atoms('name O1')[0]
    natom = u.select_atoms('name N1')[0]

    t_list = []
    rNO_list = []
    start_time = time.time()
    for ts in u.trajectory:
        r = oatom.position - natom.position
        if args.rand > 0:
            r += 2 * args.rand * 2 * (np.random.rand(3) - 0.5)
        rNO_list.append(r)
        t_list.append(ts.time)
    stop_time = time.time()
    print("Read {} steps in {:.2f} seconds.".format(len(rNO_list), stop_time-start_time))

    rNO = np.array(rNO_list)
    dNO = np.linalg.norm(rNO, axis=1).reshape(-1, 1)
    vNO = rNO / dNO  # unit vectors

    histCosX = np.histogram(vNO[:,0], range=[-1, 1], bins=args.bins, density=True)
    histCosY = np.histogram(vNO[:,1], range=[-1, 1], bins=args.bins, density=True)
    histCosZ = np.histogram(vNO[:,2], range=[-1, 1], bins=args.bins, density=True)

    bins = histCosX[1]
    bincenters = 0.5*(bins[1:]+bins[:-1])
    hist = np.array((bincenters, histCosX[0], histCosY[0], histCosZ[0])).T
    np.savetxt(args.histfile, hist, fmt="%g", delimiter=' ')

    if args.anglesfile:
        times = np.array(t_list).reshape(-1, 1)
        angles = np.rad2deg(np.arccos(vNO))
        hdr = 'time NO_X NO_Y NO_Z'
        np.savetxt(args.anglesfile, np.hstack((times, angles)), header=hdr, fmt="%.7g", delimiter=' ')
