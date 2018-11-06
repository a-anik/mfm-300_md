#!/usr/bin/env python

import argparse
from math import pi
from pymatgen.io.cif import CifParser, CifWriter
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer


if __name__ == '__main__':
    
    argp = argparse.ArgumentParser(description='Refines .cif cell')
    argp.add_argument('-t', '--trans', nargs=3, type=float, metavar=(0,0,0), default=(0,0,0), help='vector of translation')
    argp.add_argument('-r', '--rotate', nargs=1, type=float, metavar=0, default=None, help='rotation around Z-axis')
    argp.add_argument('-p', '--prec', dest='precision', type=float, default=1e-2, help='precision for symmetry determination')
    argp.add_argument('-f', '--filled', action='store_true', help='save filled cell with P1 symmetry')
    argp.add_argument('infile', help='input .cif file')
    argp.add_argument('outfile', help='output .cif file')
    args = argp.parse_args()

    cifp = CifParser(args.infile)

    # read first structure from the original .cif file, translate it and determine symmetry
    struct1 = cifp.get_structures(primitive=False)[0]
    if args.rotate:
        print(args.rotate)
        struct1.rotate_sites(theta=args.rotate[0]*pi/180.)
    struct1.translate_sites(list(range(len(struct1))), list(args.trans))

    sa1 = SpacegroupAnalyzer(struct1, symprec=args.precision)
    print("initial space group: ", sa1.get_space_group_number())

    # refine, standartize
    struct2 = sa1.get_refined_structure()
    sa2 = SpacegroupAnalyzer(struct2, symprec=args.precision)
    print("space group after refinement: ", sa2.get_space_group_number())

    ##sa1.get_symmetrized_structure()
    ##print(sa1.get_symmetry_dataset())

    # save resulting structure to .cif with original symmetry or P1 symmetry
    if not args.filled:
        w = CifWriter(struct2, symprec=args.precision)
        w.write_file(args.outfile)
    else:
        w_full = CifWriter(struct2, symprec=None)
        w_full.write_file(args.outfile)

