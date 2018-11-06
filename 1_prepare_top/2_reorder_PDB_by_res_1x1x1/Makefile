.PHONY: all clean

SCRIPT=./reorder_by_res_MFM-300.py
OUT1 := 1_MFM-300_Al
OUT2 := 2_MFM-300_In
OUT3 := 3_MFM-300_Ga

all: c$(OUT1)_labeled_res.pdb c$(OUT2)_labeled_res.pdb c$(OUT3)_labeled_res.pdb

b$(OUT1)_reordered.pdb: a$(OUT1)_labeled.pdb
	$(SCRIPT) -v --metal=Al $< $@ | tee log$(OUT1).log

c$(OUT1)_labeled_res.pdb: b$(OUT1)_reordered.pdb
	cat $< | awk -f fix_pdb_elem.awk > $@


b$(OUT2)_reordered.pdb: a$(OUT2)_labeled.pdb
	$(SCRIPT) -v --metal=In $< $@ | tee log$(OUT2).log

c$(OUT2)_labeled_res.pdb: b$(OUT2)_reordered.pdb
	cat $< | awk -f fix_pdb_elem.awk > $@

b$(OUT3)_reordered.pdb: a$(OUT3)_labeled.pdb
	$(SCRIPT) -v --metal=Ga $< $@ | tee log$(OUT3).log

c$(OUT3)_labeled_res.pdb: b$(OUT3)_reordered.pdb
	cat $< | awk -f fix_pdb_elem.awk > $@

clean:
	-@rm -f b$(OUT1)_* c$(OUT1)_* log$(OUT1)*
	-@rm -f b$(OUT2)_* c$(OUT2)_* log$(OUT2)*
	-@rm -f b$(OUT3)_* c$(OUT3)_* log$(OUT3)*
