#!/usr/bin/env python

import argparse
import MDAnalysis as mda
from MDAnalysis.topology.guessers import guess_bonds
from MDAnalysis.core.topologyattrs import Bonds
import networkx as nx
from networkx.algorithms import isomorphism
import numpy as np
import collections
import ase.io


def chem_formula(species):
    """Simple chemical formula: list of atom types -> XNYNZN"""
    counter = collections.Counter(species)
    species_with_cnt = [k + str(counter[k]) for k in sorted(counter.keys())]
    formula = ''.join(species_with_cnt)
    return formula


def reorder_mof_by_res(fname, metal_name='Al', metal_radius=1.9, verbose=False):
    """Build bonds network from PDB file.
       Find connected components. Reorder atoms by residue types."""

    mda.core.flags['use_pbc'] = True
    u = mda.Universe(fname, guess_bonds=False)

    # guess bonds using periodic box
    metal_type = u.select_atoms('name ' + metal_name)[0].type
    rvdw = {metal_type: metal_radius}
    all_bonds = guess_bonds(u.atoms, u.atoms.positions, box=u.dimensions, vdwradii=rvdw)
    u.add_TopologyAttr(Bonds(all_bonds))
    bonds_ME_O = u.bonds.atomgroup_intersection(u.select_atoms('name ' + metal_name))

    if verbose:
        print(u.atoms.names)
        print(u.atoms.types)
        print('All bonds:', u.bonds)
        print('ME-O bonds:', bonds_ME_O)

    # create graph of bonds
    G = nx.Graph()
    G.add_edges_from(u.bonds.indices)
    G.remove_edges_from(bonds_ME_O.indices)
    for i in G.nodes:
        G.nodes[i]['atom_name'] = u.atoms.names[i]   # set atom names as node attributes 

    # find residues as connected components of the graph after removal of some bonds
    comps = nx.connected_components(G)
    formula2resname = {'H1O1': 'OH', metal_type+'1': 'Me', 'C16H6O8': 'LIG'}
    resmap = {resname: [] for resname in formula2resname.values()}   # resname => list_of_graph_components_of_that_type 

    for res in comps:
        res_atoms = list(res)
        res_formula = chem_formula(u.atoms.types[res_atoms])
        res_name = formula2resname[res_formula]
        resmap[res_name].append(res)

    if verbose:
        print("Atom names: ", u.atoms.names[G.nodes()])
        print("G.nodes: ", G.nodes)
        print("G.edges: ", G.edges)
        print("Connected components: ", {res_name: len(resmap[res_name]) for res_name in resmap})
        print(nx.info(G))

    # reorder atoms to residues: group by residues, fix order within residue type
    resid = 1
    all_reordered_atoms = list()
    for res_name in ['Me', 'OH', 'LIG']:
        comp_list = resmap[res_name]
        G0 = G.subgraph(comp_list[0])  # set the first residue of a given type as a reference for atom order
        ref_ordered_nodes = sorted(G0.nodes(data='atom_name'), key=lambda x: x[1])  # sort 1-st residue atoms by atom_name
        ref_res = [x[0] for x in ref_ordered_nodes]  # ordered list of atoms numbers in the first residue

        for i, comp in enumerate(comp_list):
            if i == 0:
                res_ordered_atoms = ref_res
            else:
                G1 = G.subgraph(comp)
                GM = isomorphism.GraphMatcher(G0, G1, isomorphism.categorical_node_match('atom_name', ''))
                if GM.is_isomorphic():
                    res_ordered_atoms = [GM.mapping[a] for a in ref_res]
                else:
                    raise ValueError("Non isomorphic residue subgraph detected: {} {}".format(res_name, i))
            if verbose:
                print(resid, res_name, i, res_ordered_atoms)
            
            newres = u.add_Residue(resid=resid, resnum=resid, resname=res_name, icode='')
            u.atoms[res_ordered_atoms].residues = newres
            all_reordered_atoms += res_ordered_atoms
            resid += 1

    # check mapping and copy reordered atoms to the new universe
    assert(sorted(all_reordered_atoms) == list(range(len(u.atoms))))
    u2 = mda.Merge(u.atoms[all_reordered_atoms])
    assert(len(u2.segments) == 1)
    u2.segments[0].segid = ''
    u2.dimensions = u.dimensions
    
    return u2


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Find residues and regroup atoms in MOF file')
    parser.add_argument('infile', help='input .pdb file')
    parser.add_argument('outfile', help='output .pdb file')
    parser.add_argument('-m', '--metal', default='Al', help='metal atom name')
    parser.add_argument('-r', '--rvdw', type=float, default=2.0, help='metal atom vdw radius')
    parser.add_argument('-v', '--verbose', action='store_true', help='verbose output')
    args = parser.parse_args()

    u2 = reorder_mof_by_res(args.infile, metal_name=args.metal, metal_radius=args.rvdw, verbose=args.verbose)
    u2.atoms.write(args.outfile, bonds=None)
