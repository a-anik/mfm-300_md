#!/usr/bin/env python

import argparse
import MDAnalysis as mda
import numpy as np
import time
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Histograms of angles with axes')
    parser.add_argument('-s', dest='topfile', nargs='?', default='conf.gro', help='topology file (.gro)')
    parser.add_argument('-f', dest='trajfile', nargs='?', default='traj.xtc', help='trajectory file')
    parser.add_argument('-mof', dest='moffile', nargs='?', default='../top/start_conf.gro', help='mof configuration for xy limits')
    parser.add_argument('-mofsel', dest='mofsel', nargs='?', default='resname MOF and name C1 and prop x > 11 and prop x < 26 and prop y > 11 and prop y < 26', help='mof channel edges selection')
    parser.add_argument('-ref', dest='refgrp', nargs='?', default='resname TMP and name O1', help='atom selection for histogram')
    parser.add_argument('-o', dest='outfile', nargs='?', default='hist2d_XY.png', metavar='hist2d_XY.png', help='output 2D histogram file')
    parser.add_argument('-rand', type=float, nargs='?', default=0.005, const=0.005, metavar='0.005', help='amplitude for randomizing coordinates')
    parser.add_argument('-bins', type=int, default=50, help='Number of bins')
    parser.add_argument('-dpi', type=int, default=100, help='figure dpi')
    args = parser.parse_args()

    # get channel limits from mof file
    u0 = mda.Universe(args.moffile)
    c1grp = u0.select_atoms(args.mofsel)
    c1pos = c1grp.positions
    c1range = [[c1pos[:,0].min(), c1pos[:,0].max()], [c1pos[:,1].min(), c1pos[:,1].max()]]
    if (c1range[0][1] - c1range[0][0]) <= 0 or (c1range[1][1] - c1range[1][0]) <=0:
        raise ValueError("bad mof channel limits")
    print(c1range)
    
    u = mda.Universe(args.topfile, args.trajfile, refresh_offsets=False)
    ag = u.select_atoms(args.refgrp)

    t_list = []
    c_list = []
    start_time = time.time()
    for ts in u.trajectory:
        if args.rand > 0:
            ag.positions += args.rand * 2 * (np.random.random(ag.positions.shape) - 0.5)
        c = ag.center_of_geometry()
        c_list.append(c)
        t_list.append(ts.time)
    stop_time = time.time()
    print("Read {} steps in {:.2f} seconds.".format(len(t_list), stop_time-start_time))

    v = np.array(c_list)
    print(v.shape)
    print(v)

    size = c1range[0][1] - c1range[0][0]
    fig = plt.figure(frameon=False)
    fig.set_size_inches(size, size)
    ax = plt.Axes(fig, [0., 0., 1., 1.])
    ax.set_axis_off()
    ax.set_aspect('equal')
    fig.add_axes(ax)
    hist, xedges, yedges, im = ax.hist2d(v[:,0], v[:,1], bins=args.bins, range=c1range, normed=True, cmap=plt.cm.viridis)
    #plt.colorbar(im, ax=ax)
    #plt.savefig(args.outfile, bbox_inches='tight', pad_inches=0, dpi=100)
    plt.savefig(args.outfile, dpi=args.dpi)

