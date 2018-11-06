#!/usr/bin/env python

import argparse
import numpy as np
from CifFile import ReadCif
from ase.spacegroup import Spacegroup
import ase.io


def write_PDB(fileobj, atoms, labels, resname='MOF'):
    """Write atoms to PDB-file."""
    fileobj.write('MODEL     1\n')
    cellpar = atoms.get_cell_lengths_and_angles()
    space_group = 'P 1'
    format = 'CRYST1%9.3f%9.3f%9.3f%7.2f%7.2f%7.2f %-11s%4i\n'
    fileobj.write(format % (cellpar[0], cellpar[1], cellpar[2], cellpar[3], cellpar[4], cellpar[5], space_group, 1))
    #('ATOM  %5d %4s MOL     1    %8.3f%8.3f%8.3f%6.2f%6.2f          %2s  \n')
    #'ATOM  %(serial)5d %(name)-4s %(resName)-4s%(chainID)1s%(resSeq)4d%(iCode)1s   %(x)8.3f%(y)8.3f%(z)8.3f%(occupancy)6.2f%(tempFactor)6.2f      %(segID)-4s%(element)2s%(charge)2s'
    fmt = 'ATOM  {serial:5d} {name:^4s} {resname:<4s}{chainID:1s}{resSeq:4d}{iCode:1s}   {x:8.3f}{y:8.3f}{z:8.3f}{occupancy:6.2f}{tempFactor:6.2f}          {element:>2s}{charge:2s}\n'
    MAXNUM = 100000  # limit of 5 digit numbers for atom index
    symbols = atoms.get_chemical_symbols()
    natoms = len(symbols)
    p = atoms.get_positions()
    for i in range(natoms):
        px, py, pz = p[i]
        fileobj.write(fmt.format(serial=(i+1) % MAXNUM, name=labels[i], resname=resname, chainID='', resSeq=1, iCode='', x=px, y=py, z=pz, occupancy=1, tempFactor=0, element=symbols[i].upper(), charge=''))
    fileobj.write('ENDMDL\n')


if __name__ == '__main__':
    """Fill unit cell, save PDB with symmetry equivalent atoms having the same atom names"""
    parser = argparse.ArgumentParser(description='Fills unit cell acording to spacegroup keeping atom labels')
    parser.add_argument('infile', help='input .cif file')
    parser.add_argument('outfile', help='output .pdb file')
    parser.add_argument('-r', '--repeat', nargs=3, type=int, metavar=(1,1,1), default=(1,1,1), help='repeats for supercell')
    parser.add_argument('-p', '--prec', type=float, default=1e-3, help='symmetry precision')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    parser.add_argument('-c', '--cifout', nargs='?', const='_out_ase.cif', default=None, help='ASE cif output')
    args = parser.parse_args()

    # Read first structure from input .cif file using PyCifRW module
    # Do not use cif parser from ase.io because we need to keep atom labels
    cf = ReadCif(args.infile)
    cifblock1 = cf.keys()[0]
    mol1 = cf[cifblock1]
    sg_num = int(mol1['_symmetry_int_tables_number'])
    site_labels = mol1['_atom_site_label']
    site_symbols = mol1['_atom_site_type_symbol']
    site_sym_multiplicity = mol1['_atom_site_symmetry_multiplicity']
    basis_fract_coords = np.array([mol1['_atom_site_fract_x'], mol1['_atom_site_fract_y'], mol1['_atom_site_fract_z']]).astype(float).T
    cellpar = [float(mol1[key]) for key in ['_cell_length_a', '_cell_length_b', '_cell_length_c', '_cell_angle_alpha', '_cell_angle_beta', '_cell_angle_gamma']]

    # build symmetric copies of basis atoms according to space group
    sg = Spacegroup(sg_num)
    sites, kinds = sg.equivalent_sites(basis_fract_coords, onduplicates='error', symprec=args.prec)
    symbols = [site_symbols[i] for i in kinds]
    labels = [site_labels[i] for i in kinds]
    atoms = ase.Atoms(symbols, scaled_positions=sites, cell=cellpar, pbc=True)

    if args.verbose:
        print(sg)
        print(basis_fract_coords)
        print(site_labels)
        print(site_symbols)
        print(site_sym_multiplicity)
        print(cellpar)
        print(atoms)
        print(labels)

    if tuple(args.repeat) != (1, 1, 1):
        nreps = np.product(args.repeat)
        print("repeat", nreps)
        atoms = atoms.repeat(args.repeat)
        labels = labels * nreps

    with open(args.outfile, 'w') as f:
        write_PDB(f, atoms, labels)

    if args.cifout:
        ase.io.write(args.cifout, atoms)

