# non-bonded
s/nb@In@/  0.397608   2.506216 ; from UFF /

# bonds
s/b@In-O @/   0.21500   bKb/
s/b@In-O1@/   0.21500   bKb/
s/b@In-O2@/   0.21500   bKb/
s/bKb/300000.000/

# angles
s/a@C5-O1-In@/    135.38      aKb/
s/a@C5-O2-In@/    131.61      aKb/
s/a@H -O -In@/    119.66      aKb/
s/a@In-O -In@/    120.68      aKb/
s/a@O -In-O @/     94.65      aKb/
s/a@O -In-O1@/     90.00      aKb/
s/a@O -In-O2@/angle_undef/
s/a@O1-In-O1@/    180.00      aKb/
s/a@O1-In-O2@/     90.00      aKb/
s/a@O2-In-O2@/     83.49      aKb/
s/aKb/550.000/
s/angle_undef/      0.0         0.0  / 

# dihedrals
s/d@H -O -In-O @/    288.84       20.000     2/

s/d@C3-C5-O1-In@/dihedral_undef/
s/d@C3-C5-O2-In@/dihedral_undef/
s/d@C5-O1-In-O @/dihedral_undef/
s/d@C5-O1-In-O1@/dihedral_undef/
s/d@C5-O1-In-O2@/dihedral_undef/
s/d@C5-O2-In-O @/dihedral_undef/
s/d@C5-O2-In-O1@/dihedral_undef/
s/d@C5-O2-In-O2@/dihedral_undef/
s/d@H -O -In-O1@/dihedral_undef/
s/d@H -O -In-O2@/dihedral_undef/
s/d@In-O -In-O @/dihedral_undef/
s/d@In-O -In-O1@/dihedral_undef/
s/d@In-O -In-O2@/dihedral_undef/
s/d@In-O1-C5-O2@/dihedral_undef/
s/d@In-O2-C5-O1@/dihedral_undef/
s/dihedral_undef/      0.0         0.0       0/

# impropers
s/i@O -H -In-In@/improper_flat/
s/i@O -In-In-H @/improper_flat/
s/i@In-O -O -O2@/improper_flat/# 'In-O -O -O2'   15  avg=     0.001825  +-     2.134773 
s/i@In-O -O1-O1@/improper_flat/# 'In-O -O1-O1'   17  avg=    -0.081653  +-     3.668928 
s/i@In-O1-O2-O1@/improper_flat/# 'In-O1-O2-O1'   25  avg=     0.000000  +-     3.154350 
s/i@In-O2-O2-O @/improper_flat/# 'In-O2-O2-O '   27  avg=     0.000000  +-     2.320957 

# unused impropers
s/i@In-O -O -O1@/improper_undef/# 'In-O -O -O1'   14  avg=     0.002687  +-    59.154576 
s/i@In-O -O1-O @/improper_undef/# 'In-O -O1-O '   16  avg=    -1.662334  +-    52.554716 
s/i@In-O -O1-O2@/improper_undef/# 'In-O -O1-O2'   18  avg=     0.354048  +-    37.268823 
s/i@In-O -O2-O @/improper_undef/# 'In-O -O2-O '   19  avg=    12.260772  +-    14.310222 
s/i@In-O -O2-O1@/improper_undef/# 'In-O -O2-O1'   20  avg=    15.719752  +-    73.278406 
s/i@In-O -O2-O2@/improper_undef/# 'In-O -O2-O2'   21  avg=   -72.289725  +-    74.780245 
s/i@In-O1-O1-O @/improper_undef/# 'In-O1-O1-O '   22  avg=    -0.001812  +-   130.039263 
s/i@In-O1-O1-O2@/improper_undef/# 'In-O1-O1-O2'   23  avg=     0.000063  +-    39.538538 
s/i@In-O1-O2-O @/improper_undef/# 'In-O1-O2-O '   24  avg=     0.000000  +-    39.173420 
s/i@In-O1-O2-O2@/improper_undef/# 'In-O1-O2-O2'   26  avg=     0.000000  +-    56.907590 
s/i@In-O2-O2-O1@/improper_undef/# 'In-O2-O2-O1'   28  avg=     0.000000  +-    51.626053 

s/improper_flat/    180.00       15.000     2/
s/improper_undef/      0.0         0.0       0/
