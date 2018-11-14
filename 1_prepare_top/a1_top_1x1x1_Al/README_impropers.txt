Different packages have different sorting rules for atoms of an improper angle.
We need stable and unambigous ordering for impropertypes substitutions.

[MDAnalysis]
def guess_improper_dihedrals(angles):
    """Given a list of Angles, find all improper dihedrals that exist between atoms.

    Works by assuming that if (1,2,3) is an angle, and 2 & 4 are bonded, then (2, 1, 3, 4) must be an improper dihedral.
    ie the improper dihedral is the angle between the planes formed by (1, 2, 3) and (1, 3, 4)

    Returns: List of tuples defining the improper dihedrals.  Suitable for use in u._topology
    """

[Gromacs]
dihedrals type 4 (periodic) 
impropers : angle between (i j k) and (j k l)  - harmonic

[amber]
central atom is the third in the definition, (phase = 180, periodicity 2), others - alphabetic order
 1 2 c 3     , central is bonded to all others


[pdb2top_MOF.py]
def canon_improper_ag(u, d):
    """Return four atoms of improper angle in special order. Central atom is always the first,
    two atoms in the middle of the group are ordered by type name."""
