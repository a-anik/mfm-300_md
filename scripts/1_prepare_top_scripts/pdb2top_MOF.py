#!/usr/bin/env python

import argparse
import warnings
import MDAnalysis as mda
from numpy import rad2deg
import MDAnalysis.topology.core as topcore
from MDAnalysis.core.topologyattrs import Bonds, Angles, Dihedrals, Impropers


def build_mof_top(fname, rvdw, find_impropers=None):
    """Build periodic MOF topology from PDB file."""

    mda.core.flags['use_pbc'] = True
    u = mda.Universe(fname, guess_bonds=False)

    # set atom types from PDB atom names for proper bond typing
    u.atoms.types = u.atoms.names

    # guess bonds using periodic box
    all_bonds = topcore.guess_bonds(u.atoms, u.atoms.positions, vdwradii=rvdw, box=u.dimensions)
    u.add_TopologyAttr(Bonds(all_bonds))

    # guess angles
    all_angles = topcore.guess_angles(u.atoms.bonds)
    u.add_TopologyAttr(Angles(all_angles))

    # guess dihedrals
    all_dihedrals = topcore.guess_dihedrals(u.atoms.angles)
    u.add_TopologyAttr(Dihedrals(all_dihedrals))

    # guess impropers
    impropers = topcore.guess_improper_dihedrals(u.atoms.angles)
    u.add_TopologyAttr(Impropers(impropers))

    return u


def canon_bondstr(t):
    """Return canonical string representaion for bond, angle, etc.
    It has the form of AtomName1-AtomName2-...
    Use reverse order if it is lexicographically smaller."""
    if tuple(t[::-1]) < tuple(t):
        t = t[::-1]

    return '-'.join(t)


def canon_improper_ag(u, d):
    """Return four atoms of improper angle in special order. Central atom is always the first,
    two atoms in the middle of the group are ordered by type name."""
    # find central atom: after MDAnalysis guess_impropers it is either the first or the last atom
    neigs0 = [b.partner(d[0]) for b in d[0].bonds]
    neigs3 = [b.partner(d[3]) for b in d[3].bonds]
    central_is_first = (d[1] in neigs0) and (d[2] in neigs0) and (d[3] in neigs0)
    central_is_last  = (d[0] in neigs3) and (d[1] in neigs3) and (d[2] in neigs3)
    if central_is_first == central_is_last:
        raise ValueError('Error while searching for central atom of improper dihedral {}'.format(d))

    if central_is_first:
        ag = d[:]     # keep order
    else:
        ag = d[::-1]  # reverse order
    if ag[1].type > ag[2].type:
        ag = [ag[0], ag[2], ag[1], ag[3]] # sort two central atoms by their type name

    return ag


def print_atoms(u, keep_resname=False):
    print('[ moleculetype ]')
    print('; Name       nrexcl')
    print('MOF    3')
    print()
    print('; %d atoms of %d types' % (len(u.atoms), len(set(u.atoms.types))))
    print('[ atoms ]')
    print(';   nr       type  resnr residue  atom   cgnr     charge       mass')
    resname = 'MOF'
    for a in u.atoms:
        if keep_resname:
            resname = a.resname
        print("%6d %10s %5d %6s %6s %7d" % (a.id, a.name + '_mof', a.resnum, resname, a.name, a.id))
    print()


def print_bonds(u, print_values=False):
    print('; %d bonds of %d types' % (len(u.bonds), len(u.bonds.types())))
    print(';', ', '.join([canon_bondstr(t) for t in u.bonds.types()]))
    print('[ bonds ]')
    print(';  ai    aj  funct    b0        kb')
    
    values = u.bonds.values(pbc=True)
    for b, val in zip(u.bonds, values):
        btype = 'gb_mof_' + canon_bondstr(b.type)
        valstr = ''
        if print_values:
            valstr = "%7.4f" % val
        print("%5s %5s      %-20s ; %-4s %-4s %s" % (b[0].id, b[1].id, btype, b[0].name, b[1].name, valstr))
    print()


def print_pairs(u):
    # find 1-4 pairs
    pairs_all = set([tuple(sorted([i1, i4])) for i1, i2, i3, i4 in u.dihedrals.to_indices()])
    exclusions = set([tuple(sorted([i1, i3])) for i1, i2, i3 in u.angles.to_indices()])
    pairs14 = pairs_all - exclusions

    print('; %d pairs' % (len(pairs14)))
    print('[ pairs ]')
    print(';  ai    aj   funct')
    for i1, i2 in sorted(pairs14):
        print("%5d %5d %5d    ; %-3s %-3s" % (i1+1, i2+1, 1, u.atoms[i1].name, u.atoms[i2].name))
    print()


def print_angles(u, print_values=False):
    print('; %d angles of %d types' % (len(u.angles), len(u.angles.types())))
    print(';', ', '.join([canon_bondstr(t) for t in u.angles.types()]))
    print('[ angles ]')
    print(';  ai    aj    ak   funct      phi0      fc')
    values = u.angles.values(pbc=True)
    for a, val in zip(u.angles, values):
        atype = 'ga_mof_' + canon_bondstr(a.type)
        valstr = ''
        if print_values:
            valstr = "%9.4f" % rad2deg(val)
        print("%5s %5s %5s       %-20s ; %-4s %-4s %-4s %s" % (a[0].id, a[1].id, a[2].id, atype, a[0].name, a[1].name, a[2].name, valstr))
    print()


def print_dihedrals(u, print_values=False):
    print('; originally %d diherals of %d types' % (len(u.dihedrals), len(u.dihedrals.types())))
    print('[ dihedrals ]')
    print(';  ai    aj    ak    al   funct   phi0        fc    mult')
    values = u.dihedrals.values(pbc=True)
    for d, val in zip(u.dihedrals, values):
        dtype = 'gd_mof_' + canon_bondstr(d.type)
        valstr = ''
        if print_values:
            valstr = "%9.4f" % rad2deg(val)
        print("%5s %5s %5s %5s     %-20s ; %-3s %-3s %-3s %-3s %s" % (d[0].id, d[1].id, d[2].id, d[3].id,
                                                                   dtype, d[0].name, d[1].name, d[2].name, d[3].name, valstr))
    print()


def print_impropers(u, print_values=False):
    print('; originally %d impropers' % (len(u.impropers)))
    print('[ dihedrals ]')
    print(';  ai    aj    ak    al   funct    phi0         fc')
    values = u.impropers.values(pbc=True)
    for d_guessed, val in zip(u.impropers, values):
        d = canon_improper_ag(u, d_guessed)
        dtypestr = 'gi_mof_' + '-'.join([a.type for a in d])
        valstr = ''
        if print_values:
            valstr = "%9.4f" % rad2deg(val)
        print("%5s %5s %5s %5s    %-20s ; %-3s %-3s %-3s %-3s %s" % (d[0].id, d[1].id, d[2].id, d[3].id,
                                                                  dtypestr, d[0].name, d[1].name, d[2].name, d[3].name, valstr))
    print()


if __name__ == '__main__':

    tested_MDAnalysis_version = '0.18.0'
    parser = argparse.ArgumentParser(description='Generates GROMACS topology include file from MOF PDB structure file.',
                                     formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('fname', default='conf.pdb', metavar='conf.pdb', nargs='?', help='MOF PDB file')
    parser.add_argument('-r', '--rvdw', nargs='?', default='rvdw.dat', help='vdW radii database')
    parser.add_argument('-od', '--outpdb', required=False, help='output structure with bonds')
    parser.add_argument('-np', '--no-pairs', action='store_true', help='do not output [ pairs ] section for 1-4 interactions')
    parser.add_argument('-nv', '--no-values', action='store_true', help='print values for bonds, angles, dihedrals')
    parser.add_argument('-k', '--keepres', action='store_true', help='keep residue names from PDB file')
    args = parser.parse_args()

    if mda.version.__version__ != tested_MDAnalysis_version:
        warnings.warn("This scripts was only tested with MDAnalysis version {}.".format(tested_MDAnalysis_version))

    rvdw = {}
    with open(args.rvdw, 'r') as f:
        for line in f:
            (name, radius) = line.split()
            rvdw[name] = float(radius)

    u = build_mof_top(args.fname, rvdw)

    if args.outpdb:
        with mda.Writer(args.outpdb) as W:
                W.write(u)
    
    print_values = not args.no_values
    print('; Generated by pdb2top_MOF.py script from {} file.\n'.format(args.fname))
    print_atoms(u, args.keepres)
    print_bonds(u, print_values)
    if not args.no_pairs:
        print_pairs(u)
    print_angles(u, print_values)
    print_dihedrals(u, print_values)
    print_impropers(u, print_values)
