# ALAS=varietal_alias
# CROP=crop
# CVAR=crop_variety
# JRNL=journal_reference
# PATH=pathogen,
# PED=pedigree,
# PLAN=plant_anatomy
# PPTD=plant_predisposition_to_disease
# TRAT=trait

TRAIN_DATA = [
    ('Eight-Twelve is a six-rowed winter feed barley',{'entities': [(0, 12, 'CVAR'), (18, 27, 'TRAT'), (28, 39, 'TRAT'), (40, 46, 'CROP')]}),
    ('It was released by the USDA-ARS and the Idaho AES in 1991', {'entities': [(23, 31, 'ORG'), (40, 49, 'ORG'), (53, 57, 'DATE')]}),
    ('It was selected from the cross Steveland/Luther//Wintermalt', {'entities': [(31, 59, 'PED')]}),
    ('Its experimental designation was 79Ab812', {'entities': [(33, 40, 'ALAS')]}),
    ('It has rough awns, midseason maturity, good winter hardiness, and is medium height with intermediate lodging resistance', {'entities': [(13, 17,'PLAN'), (19, 37, 'TRAT'), (44, 60, 'TRAT'), (69, 82, 'TRAT'), (88,119, 'TRAT')]}),
    ('Spikes are short and dense', {'entities': [(0, 6, 'PLAN')]}),
    ('Kernels have white aleurone and short rachilla hairs', {'entities': [(0, 7,'PLAN'), (19, 27, 'PLAN'), (38, 52, 'PLAN')]}),
    ('It is susceptible to stripe rust, scald, and snow mold, and moderately susceptible to BYD', {'entities': [(6, 17, 'PPTD'), (21, 32, 'PATH'), (34, 39, 'PATH'), (45, 54, 'PATH'), (60, 82, 'PP2D'), (86, 89, 'PATH')]}),
    ('Crop Science 32(3):828 (1992)', {'entities': [(0, 12, 'JRNL')]}),
    ('Maja is a six-rowed winter feed/malt barley', {'entities': [(0, 4, 'CVAR'), (10, 19, 'TRAT'), (20, 31, 'TRAT'), (32, 36, 'TRAT'), (37, 43, 'CROP')]}),
    ('It was released by the Oregon AES in 2006 and licensed to AriSource (Burley, Idaho)', {'entities': [(23, 33, 'ORG'), (58, 67, 'DATE'), (69, 75,'GPE'), (77, 82, 'GPE')]}),
    ('It is a doubled haploid developed from the F1 of the cross of Strider/88Ab538.', {'entities': [(62, 77, 'PED')]}),
    ('Its experimental designation was STAB 113', {'entities': [(33, 41, 'ALAS')]}),
    ('Maja, like the 88Ab536 parent, is a facultative cultivar: it has a \"winter\" allele at the Vm-H1 locus on chromosome 5H but lacks the repressor encoded by the Vrn-H2 locus on 4H.', {'entities': [(0, 4, 'CVAR'), (15, 22,'CVAR'), (36, 47, 'TRAT')]}),
    ('It is a standard height selection (averages about 42 inches in plant height, with fair straw strength) with rough awns and a semi-compact spike', {'entities': [(8, 23, 'TRAT'), (63, 75, 'TRAT'), (87, 101,'TRAT'), (114, 118, 'PLAN'), (138, 143, 'PLAN')]}),
    ('The grain has white aleurone', {'entities': [(4, 9, 'PLAN'), (20, 28, 'PLAN')]}),
    ('Maja has high test weight and showed promise as malting barley in repeated micro-malting tests', {'entities': [(0, 4, 'CVAR'), (9, 25, 'TRAT'), (48, 62, 'TRAT')]}),
    ('At the time of evaluation it was resistant to stripe rust and susceptible to scald.', {'entities': [(33, 42, 'PPTD'), (46, 57, 'PATH'), (62, 73, 'PPTD'), (77, 82, 'PATH')]}),
    ('Strider is a six-rowed winter feed barley', {'entities': [(0, 7, 'CVAR'),(13, 22, 'TRAT'), (23, 34, 'TRAT'), (35, 41, 'CROP')]}),
    ('It was released by the Oregon AES in 1997', {'entities': [(23, 33, 'ORG'),(37, 41, 'DATE')]}),
    ('It is a doubled-haploid line produced from the cross I1162-19/J-126//WA1245///Steptoe', {'entities': [(53, 85, 'PED')]}),
    ('Its experimental designation was ORW-6', {'entities': [(33, 38, 'ALAS')]}),
    ('It is medium height (averages about 41 inches, slightly taller than Kold) and medium early maturing with fair straw strength', {'entities': [(6, 19, 'TRAT'), (68, 72, 'CVAR'), (85, 99, 'TRAT'), (105, 124, 'TRAT')]}),
    ('It has rough awns and a semi-compact spike', {'entities': [(13, 17, 'PLAN'), (37, 42, 'PLAN')]}),
    ('At the time of evaluation it was resistant to stripe rust and moderately susceptible to scald, net blotch and BYD', {'entities': [(33, 42, 'PPTD'), (46, 57, 'PATH'), (62, 84, 'PPTD'), (88, 93, 'PATH'), (95, 105, 'PATH'), (110, 113, 'PATH')]}),
    ('Strider is a six-rowed winter feed barley', {'entities': [(0, 7, 'CVAR'), (13, 22, 'TRAT'), (23, 29, 'TRAT'), (35, 41, 'CROP')]}),
    ('It was released by the Oregon AES in 1997', {'entities': [(23, 33, 'ORG'), (37, 41, 'DATE')]}),
    ('It is a doubled-haploid line produced from the cross I1162-19/J-126//WA1245///Steptoe', {'entities': [(8, 23, 'TRAT'), (53, 85, 'PED')]}),
    ('Its experimental designation was ORW-6', {'entities': [(33, 38, 'ALAS')]}),
    ('It is medium height (averages about 41 inches, slightly taller than Kold) and medium early maturing with fair straw strength', {'entities': [(6, 19, 'TRAT'), (68, 72, 'CVAR'), (78, 99, 'TRAT'), (105, 124, 'TRAT')]}),
    ('It has rough awns and a semi-compact spike', {'entities': [(13, 17, 'PLAN'), (37, 42, 'PLAN')]}),
    ('At the time of evaluation it was resistant to stripe rust and moderately susceptible to scald, net blotch, and BYD', {'entities': [(33, 42, 'PPTD'), (46, 57, 'PATH'), (62, 84, 'PPTD'), (88, 93, 'PATH'), (95, 105, 'PATH'), (111, 114, 'PATH')]})]
