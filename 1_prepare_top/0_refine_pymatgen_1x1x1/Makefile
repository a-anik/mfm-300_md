.PHONY: all clean

SCRIPT=./pymatgen_refine_cif.py

all: c1_MFM-300_Al_refined_type.cif _d1_MFM-300_Al_filledP1.cif \
    c2_MFM-300_In_refined_type.cif  _d2_MFM-300_In_filledP1.cif \
    c3_MFM-300_Ga_refined_type.cif  _d3_MFM-300_Ga_filledP1.cif 

b1_MFM-300_Al_refined.cif: a1_MFM-300_Al_pure.cif $(SCRIPT)
	$(SCRIPT) -t 0 0 0.5 a1_MFM-300_Al_pure.cif b1_MFM-300_Al_refined.cif

b2_MFM-300_In_refined.cif: a2_MFM-300_In_pure.cif $(SCRIPT)
	$(SCRIPT) -t 0 0 0  a2_MFM-300_In_pure.cif b2_MFM-300_In_refined.cif

b3_MFM-300_Ga_refined.cif: a3_MFM-300_Ga_pure.cif $(SCRIPT)
	$(SCRIPT) -t 0 0.0 0.5 a3_MFM-300_Ga_pure.cif b3_MFM-300_Ga_refined.cif

c1_MFM-300_Al_refined_type.cif: b1_MFM-300_Al_refined.cif
	cat $< | sed -f ./rename-Al.sed > $@

c2_MFM-300_In_refined_type.cif: b2_MFM-300_In_refined.cif
	cat $< | sed -f ./rename-In.sed > $@

c3_MFM-300_Ga_refined_type.cif: b3_MFM-300_Ga_refined.cif
	cat $< | sed -f ./rename-Ga.sed > $@

_d1_MFM-300_Al_filledP1.cif: a1_MFM-300_Al_pure.cif
	$(SCRIPT) --filled -t 0 0 0.5 $< $@

_d2_MFM-300_In_filledP1.cif: a2_MFM-300_In_pure.cif
	$(SCRIPT) --filled -t 0 0 0 $< $@

_d3_MFM-300_Ga_filledP1.cif: a3_MFM-300_Ga_pure.cif
	$(SCRIPT) --filled -t 0 0 0.5 $< $@

clean:
	-@rm -f c1_MFM-300_Al_refined_type.cif b1_MFM-300_Al_refined.cif _d1_MFM-300_Al_filledP1.cif
	-@rm -f c2_MFM-300_In_refined_type.cif b2_MFM-300_In_refined.cif _d2_MFM-300_In_filledP1.cif
	-@rm -f c3_MFM-300_Ga_refined_type.cif b3_MFM-300_Ga_refined.cif _d3_MFM-300_Ga_filledP1.cif
