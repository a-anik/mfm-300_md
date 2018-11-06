.PHONY: all clean

SCRIPT=./cif2pdb_labeled.py
OUT1 := 1_MFM-300_Al
OUT2 := 2_MFM-300_In
OUT3 := 3_MFM-300_Ga

OUTFILES:= b$(OUT1)_labeled.pdb b$(OUT2)_labeled.pdb b$(OUT3)_labeled.pdb

all: $(OUTFILES)

b$(OUT1)_labeled.pdb: a$(OUT1)_refined_type.cif
	$(SCRIPT) $< $@

b$(OUT2)_labeled.pdb: a$(OUT2)_refined_type.cif
	$(SCRIPT) $< $@

b$(OUT3)_labeled.pdb: a$(OUT3)_refined_type.cif
	$(SCRIPT) $< $@

clean:
	-@rm -f $(OUTFILES)
