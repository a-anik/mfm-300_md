#!/usr/bin/env python

import argparse
from collections import defaultdict
import numpy as np
import re

def ascending(t):
    x = tuple(t)
    if x[::-1] < x:
        x = x[::-1]
    return x

def dprint(d, btype, symtypemap, ffmap, print_values=False):
    header = {'atom': '[ atomtypes ]\n; name1 name2       mass         charge   ptype   sigma      epsilon',
              'bond': '; bond types                   func       b0          kb',
             'angle': '; angle types                  func       phi0        fc',
          'dihedral': '; dihedral types               func       phi0        fc    mult',
          'improper': '; improper dihedral types      func       phi0        fc'}
    func = {'atom':'', 'bond': '1', 'angle': '1', 'dihedral': '9', 'improper': '4'}
    print(header[btype])
 
    for i, key in enumerate(sorted(d.keys())):
        vals = np.array(d[key], dtype=float)
        if print_values:
            vlist = '@vals={}'.format(np.array_str(vals, max_line_width=1024))
        else:
            vlist = ''
        if len(symtypemap[key]) != 1:
            raise ValueError('Mapping bond_name->[atom_names] is not unique: {} {}'.format(key, symtypemap[key]))
        symtype = symtypemap[key].pop()
        if all(a in ffmap for a in symtype) and btype != 'improper': 
            fftype = ascending([ffmap[a] for a in symtype]) 
            ffstr = '-'.join(['{:2s}'.format(a) for a in fftype])   
        else:
            ffstr = '-'.join(['{:2s}'.format(a) for a in symtype])    # translate to ff names only if all atoms are known
        keystr='#define {:20s}'.format(key)
        funcstr = '{:>5s}  '.format(func[btype])
        if len(vals) != 0:
            avgstr = 'avg= {:12f}  +- {:12f}'.format(vals.mean(), vals.std())
        ffkey = btype[0]
        if btype == 'atom':
            atomname = '{:s}'.format(key[:-4])
            keystr = '{:8s}'.format(key)
            funcstr = '{:6s} mass@{:5s}   charge@{:5s}  {:>2s}  '.format(atomname, atomname, atomname, 'A')
            avgstr = ''
            ffkey = 'nb'
        
        print("{} {} {}@{}@ ; \'{}\'  {:3d}  {} {}".format(keystr, funcstr, ffkey, ffstr, ffstr, i+1, avgstr, vlist))
    print("")
    

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Collects atoms/bonds/angles types from .itp')
    parser.add_argument('fname', help='MOF topology include file')
    parser.add_argument('-f', '--ffmap', nargs='?', default='ff_atoms_map.dat', const='ff_atoms_map.dat', help='file with sym_atom_name->fftype atom mapping')
    parser.add_argument('-v', '--verbose', action='store_true', help='print list of values')
    args = parser.parse_args()

    btypes = ['atom', 'bond', 'angle', 'dihedral', 'improper']
    p = {k:re.compile(v) for k, v in zip(btypes, ['_mof ', 'gb_mof', 'ga_mof', 'gd_mof', 'gi_mof'])}
    vals = {k: defaultdict(list) for k in btypes}
    symtypes = {k: defaultdict(set) for k in btypes}   # symtype is ordered tuple of sym_atom_names

    with open(args.fname, 'r') as incfile:
        for line in incfile:
            f = line.split()
            if re.search(p['atom'], line):
                vals['atom'][f[1]] = []
                symtypes['atom'][f[1]].add((f[4],))
            elif re.search(p['bond'], line):
                vals['bond'][f[2]].append(float(f[-1])*0.1)  # angstrom to nm
                symtypes['bond'][f[2]].add(ascending((f[-3], f[-2])))
            elif re.search(p['angle'], line):
                vals['angle'][f[3]].append(float(f[-1]))
                symtypes['angle'][f[3]].add(ascending((f[-4], f[-3], f[-2])))
            elif re.search(p['dihedral'], line):
                vals['dihedral'][f[4]].append(float(f[-1]))
                symtypes['dihedral'][f[4]].add(ascending((f[-5],f[-4], f[-3], f[-2])))
            elif re.search(p['improper'], line):
                vals['improper'][f[4]].append(float(f[-1]))
                symtypes['improper'][f[4]].add(tuple((f[-5],f[-4], f[-3], f[-2])))

    ffmap = dict()
    with open(args.ffmap, 'r') as f:
        for line in f:
            sym_atom_name, fftype = line.split()
            ffmap[sym_atom_name] = fftype

    for t in btypes:
        dprint(vals[t], t, symtypes[t], ffmap, args.verbose)
    print('; END of atomtypes.itp')
