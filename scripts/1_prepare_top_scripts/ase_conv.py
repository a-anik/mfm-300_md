#!/usr/bin/env python

import argparse
import ase.io
import ase.spacegroup

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert file using ase')
    parser.add_argument('infile', help='input file')
    parser.add_argument('outfile', help='output file')
    parser.add_argument('-s', '--symprec', type=float, default=1e-2, help='symmetry detection tolerance')
    parser.add_argument('-v', '--verbose', action='store_true', help='print symmetry information')
    args = parser.parse_args()

    a = ase.io.read(args.infile)

    if args.verbose:
        print(a)
        sg = ase.spacegroup.get_spacegroup(a, symprec=args.symprec, method='spglib')
        print(sg)
        #ua = sg.unique_sites(a.get_scaled_positions())
        #print(ua)

    ase.io.write(args.outfile, a)
