.PHONY: all clean

all: subst.sed mof_GMX.top

1.pdb: c1_MFM-300_Al_labeled_res.pdb
	cat c1_MFM-300_Al_labeled_res.pdb | awk '$$1=="ATOM" && ($$5!=17) {next} {print}' > 1.pdb

2.pdb: 1.pdb
	pdb4amber -i 1.pdb -o 2.pdb

3.mol2: 2.pdb
	antechamber -i 2.pdb -fi pdb -o 3.mol2 -fo mol2 -nc -8 -du no -a 2.pdb -fa pdb -ao name 

frcmod: 3.mol2
	parmchk2 -i 3.mol2 -f mol2 -o frcmod

frcmod_full: 3.mol2
	parmchk2 -i 3.mol2 -f mol2 -o frcmod_full -a Y

subst.sed: frcmod_full gen_gaff_subst.py
	./gen_gaff_subst.py frcmod_full > subst.sed 
	
prmtop: 3.mol2 leap.cmd frcmod frcmod_full
	tleap -s -f leap.cmd

mof_GMX.top: prmtop inpcrd
	acpype.py -x inpcrd -p prmtop -b mof --gmx45

clean:
	-@rm -f 1.pdb 2.pdb 3.mol2 
	-@rm -f stdout_* 2_nonprot.pdb 2_renum.txt 2_sslink
	-@rm -f ANTECHAMBER* ATOMTYPE.INF
	-@rm -f sqm.* parmed.log
	-@rm -f frcmod frcmod_full inpcrd prmtop leap.log
	-@rm -f mof_GMX.* md.mdp em.mdp
	-@rm -f subst.sed

