#!/usr/bin/env python

import argparse
import numpy as np
import MDAnalysis as mda
from collections import defaultdict

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Generates file with name->charges substitutions')
    parser.add_argument('fname', help='MOF PDB file')
    parser.add_argument('cname', help='file with REPEAT charges')
    args = parser.parse_args()

    u = mda.Universe(args.fname, guess_bonds=False)
    charges = defaultdict(set)
    with open(args.cname, 'r') as f:
        for line in f:
            fld = line.split()
            if len(fld) == 4 and fld[0] == 'RESP':
                i = int(fld[1])
                charge = float(fld[3])
                aname = u.atoms[i-1].name
                charges[aname].add(charge)

    for aname in sorted(charges.keys()):
        if len(charges[aname]) != 1:
            raise ValueError('Multilple charges encountered for atom type {}'.format(aname))
        print('s/charge@{:3s}/{:10.6f}/'.format(aname, charges[aname].pop()))

