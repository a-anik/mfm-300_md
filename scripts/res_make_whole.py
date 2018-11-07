#!/usr/bin/env python

import argparse
import MDAnalysis as mda
import MDAnalysis.topology.core as topcore
from MDAnalysis.core.topologyattrs import Bonds

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Make residues whole')
    parser.add_argument('infile', help='input file')
    parser.add_argument('outfile', help='output file')
    args = parser.parse_args()

    mda.core.flags['use_pbc'] = True
    rvdw = {'Al': 2.0, 'In': 2.0, 'Ga': 2.0, 'LP': 0.0}
    u = mda.Universe(args.infile, guess_bonds=False)
    # guess bonds using periodic box
    all_bonds = topcore.guess_bonds(u.atoms, u.atoms.positions, vdwradii=rvdw, box=u.dimensions)
    u.add_TopologyAttr(Bonds(all_bonds))

    for r in u.atoms.residues:
        mda.lib.mdamath.make_whole(r.atoms)

    u.atoms.write(args.outfile)
    #with mda.Writer(args.outfile) as W:
    #        W.write(u)
