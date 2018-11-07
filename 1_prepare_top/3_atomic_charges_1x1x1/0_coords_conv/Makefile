.PHONY: all clean

SCRIPT=./pdb2cp2k_coords.py
OUT1:= 1_MFM-300_Al
OUT2:= 2_MFM-300_In
OUT3:= 3_MFM-300_Ga

all: b$(OUT1)_coords.inc b$(OUT2)_coords.inc \
   b$(OUT3)_coords.inc

b$(OUT1)_coords.inc: a$(OUT1)_labeled_res.pdb
	$(SCRIPT) $< b$(OUT1)

b$(OUT2)_coords.inc: a$(OUT2)_labeled_res.pdb
	$(SCRIPT) $< b$(OUT2) 

b$(OUT3)_coords.inc: a$(OUT3)_labeled_res.pdb
	$(SCRIPT) $< b$(OUT3)

clean:
	-@rm -f "b$(OUT1)"_* "b$(OUT2)"_* "b$(OUT3)"_*
