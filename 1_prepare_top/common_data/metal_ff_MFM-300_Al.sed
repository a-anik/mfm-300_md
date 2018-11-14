# non-bonded
s/nb@Al@/  0.400815   2.11292  ; from UFF /

# bonds
s/b@Al-O @/   0.19300   bKb/
s/b@Al-O1@/   0.19300   bKb/
s/b@Al-O2@/   0.19300   bKb/
s/bKb/300000.000/

# angles
s/a@Al-O -Al@/    121.93      aKb/ 
s/a@Al-O -H @/    119.04      aKb/
s/a@Al-O1-C5@/    132.30      aKb/ 
s/a@Al-O2-C5@/    131.35      aKb/ 
s/a@O -Al-O @/     99.53      aKb/ 
s/a@O -Al-O1@/     90.00      aKb/ 
s/a@O -Al-O2@/angle_undef/
s/a@O1-Al-O1@/    180.00      aKb/
s/a@O1-Al-O2@/     90.00      aKb/
s/a@O2-Al-O2@/     80.35      aKb/
s/aKb/550.000/
s/angle_undef/      0.0         0.0  / 

# dihedrals
s/d@H -O -Al-O @/    287.72       20.000     2/

s/d@H -O -Al-O1@/dihedral_undef/
s/d@H -O -Al-O2@/dihedral_undef/
s/d@Al-O -Al-O @/dihedral_undef/
s/d@Al-O -Al-O1@/dihedral_undef/
s/d@Al-O -Al-O2@/dihedral_undef/
s/d@Al-O1-C5-C3@/dihedral_undef/
s/d@Al-O1-C5-O2@/dihedral_undef/
s/d@Al-O2-C5-C3@/dihedral_undef/
s/d@Al-O2-C5-O1@/dihedral_undef/
s/d@C5-O1-Al-O @/dihedral_undef/
s/d@C5-O1-Al-O1@/dihedral_undef/
s/d@C5-O1-Al-O2@/dihedral_undef/
s/d@C5-O2-Al-O @/dihedral_undef/
s/d@C5-O2-Al-O1@/dihedral_undef/
s/d@C5-O2-Al-O2@/dihedral_undef/
s/dihedral_undef/      0.0         0.0       0/

# impropers
s/i@O -Al-Al-H @/improper_flat/
s/i@O -Al-H -Al@/improper_flat/
s/i@Al-O -O -O2@/improper_flat/
s/i@Al-O -O1-O1@/improper_flat/
s/i@Al-O1-O2-O1@/improper_flat/
s/i@Al-O2-O2-O @/improper_flat/

# unused impropers
s/i@Al-O -O -O1@/improper_undef/
s/i@Al-O -O1-O @/improper_undef/
s/i@Al-O -O1-O2@/improper_undef/
s/i@Al-O -O2-O @/improper_undef/
s/i@Al-O -O2-O1@/improper_undef/
s/i@Al-O -O2-O2@/improper_undef/
s/i@Al-O1-O1-O @/improper_undef/
s/i@Al-O1-O1-O2@/improper_undef/
s/i@Al-O1-O2-O @/improper_undef/
s/i@Al-O1-O2-O2@/improper_undef/
s/i@Al-O2-O2-O1@/improper_undef/

s/improper_flat/    180.00       15.000     2/
s/improper_undef/      0.0         0.0       0/
