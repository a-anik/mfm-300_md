source leaprc.gaff
mods = loadAmberParams frcmod
LIG = loadMol2 3.mol2
saveAmberParm LIG prmtop inpcrd
quit
