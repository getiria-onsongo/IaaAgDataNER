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
('2   AC METCALFE  AC Metcalfe is a two-rowed spring malting barley.', {'entities': [(17, 28, 'CVAR'), (34, 43, 'TRAT'), (44, 50, 'TRAT'), (51, 58, 'TRAT'), (59, 65, 'CROP')]}),
    ('It was released by Agriculture and Agri-Food Canada in 1997.', {'entities': [(19, 51, 'ORG'), (55, 59, 'DATE')]}),
    ('It is mid-late season in maturity (similar to Klages and 3-5 days later than Steptoe).', {'entities': [(6, 21, 'TRAT'), (46, 52, 'CVAR'), (77, 84, 'CVAR')]}),
    ('It is medium height (2 inches shorter than Steptoe) and has moderately stiff straw.', {'entities': [(6, 19, 'TRAT'), (43, 50, 'CVAR'), (60, 82, 'TRAT')]}),
    ('It was selected from the cross AC Oxbow/Manley.', {'entities': [(31, 46, 'PED')]}),
    ('Awns are rough.', {'entities': [(0, 4, 'PLAN')]}),
    ('Glumes are covered with long hairs.', {'entities': [(0, 6, 'PLAN')]}),
    ('Hulls are adhering and wrinkled.', {'entities': [(0, 5, 'PLAN')]}),
    ('Aleurone is colorless.', {'entities': [(0, 8, 'PLAN')]}),
    ('Rachilla hairs are long.', {'entities': [(0, 14, 'PLAN')]}),
    ('Veins are well defined.', {'entities': [(0, 5, 'PLAN')]}),
    ('The kernel is plump and broad in relation to length.', {'entities': [(4, 10, 'PLAN')]}),
    ('At the time of evaluation Baronesse was moderately resistant to BYD, moderately susceptible to scald and net blotch, and susceptible to stripe rust, leaf rust, and powdery mildew.', {'entities': [(26, 35, 'CVAR'), (40, 60, 'PPTD'), (64, 67, 'PATH'), (69, 91, 'PPTD'), (95, 100, 'PATH'), (105, 115, 'PATH'), (121, 132, 'PPTD'), (136, 147, 'PATH'), (149, 158, 'PATH'), (164, 178, 'PATH')]}),
    ('Its experimental designations were TR 232 and WM8612-1.', {'entities': [(35, 41, 'ALAS'), (46, 54, 'ALAS')]}),
    ('CDC COPELAND CDC Copeland is a two-rowed spring malting barley.', {'entities': [(13, 25, 'CVAR'), (31, 40, 'TRAT'), (41, 47, 'TRAT'), (48, 55, 'TRAT')]}),
    ('It was developed by the Crop Development Center, University of Saskatoon and registered in Canada in 1999.', {'entities': [(24, 72, 'ORG'), (91, 97, 'GPE'), (101, 105, 'DATE')]}),
    ('Its experimental designation was TR150.', {'entities': [(33, 38, 'ALAS')]}),
    ('It is medium late maturing (3 days earlier than Manley, 1 day later than Harrington).', {'entities': [(6, 26, 'TRAT'), (48, 54, 'CVAR'), (73, 83, 'CVAR')]}),
    ('CDC Copeland averages 7 cm taller than Harrington and 5 cm taller than Manley, and has good resistance to lodging (much stronger straw than Harrington, slightly stronger straw than Manley).', {'entities': [(0, 12, 'CVAR'), (39, 49, 'CVAR'), (71, 77, 'CVAR'), (87, 113, 'TRAT'), (140, 150, 'CVAR'), (181, 187, 'CVAR')]}),
    ('It has higher test weight and plumper kernels than Manley, and kernel plumpness similar to Harrington.', {'entities': [(51, 57, 'CVAR'), (91, 101, 'CVAR')]}),
    ('It is widely adapted to western Canada and has excellent malting and brewing quality, particularly malt extract.', {'entities': [(24, 38, 'GPE'), (47, 64, 'TRAT'), (69, 84, 'TRAT')]}),
    ('Heads are dense and semi-nodding.', {'entities': [(0, 5, 'PLAN'), (20, 32, 'TRAT')]}),
    ('Awns are rough with weak anthocyanin in awn tips and equal to or longer than the spike.', {'entities': [(0, 4, 'PLAN'), (20, 48, 'TRAT'), (81, 86, 'PLAN')]}),
    ('Glumes and awns of the median spikelet are equal to the length of the grain.', {'entities': [(0, 6, 'PLAN'), (11, 15, 'PLAN'), (23, 38, 'PLAN'), (70, 75, 'PLAN')]}),
    ('The hull is adhering and the aleurone is colorless.', {'entities': [(4, 8, 'PLAN'), (29, 37, 'PLAN')]}),
    ('Rachilla hairs are long.', {'entities': [(0, 14, 'PLAN')]}),
    ('There is no pigment in the lemma nerves.', {'entities': [(27, 39, 'PLAN')]}),
    ('Kernels are plump, symmetrical, and broad in relation to length.', {'entities': [(0, 7, 'PLAN')]}),
    ('CDC Copeland has good resistance to wheat stem rust (better than Manley and Harrington), is moderately resistant to net blotch (similar to Manley), moderately susceptible to stripe rust, and susceptible to scald, Septoria leaf blotch (as are Manley and Harrington), and loose smut.', {'entities': [(0, 12, 'CVAR'), (17, 32, 'PPTD'), (36, 51, 'PATH'), (65, 71, 'CVAR'), (76, 86, 'CVAR'), (92, 112, 'PPTD'), (116, 126, 'PATH'), (139, 145, 'CVAR'), (148, 170, 'PPTD'), (174, 185, 'PATH'), (191, 202, 'PPTD'), (206, 211, 'PATH'), (213, 233, 'PATH'), (242, 248, 'CVAR'), (253, 263, 'CVAR'), (270, 280, 'PATH')]}),
    ('It is more susceptible to common root rot than Manley.', {'entities': [(11, 22, 'PPTD'), (26, 41, 'PATH'), (47, 53, 'CVAR')]}),
    ('It is tall (averages about 40 inches in plant height) with fair straw strength and is medium late maturing (about one day later than Harrington).', {'entities': [(6, 10, 'TRAT'), (59, 78, 'TRAT'), (86, 106, 'TRAT'), (133, 143, 'CVAR')]}),
    ('CELEBRATION Celebration is a six-rowed spring malting barley.', {'entities': [(12, 23, 'CVAR'), (29, 38, 'TRAT'), (39, 45, 'TRAT'), (46, 53, 'TRAT'), (54, 60, 'CROP')]}),
    ('It was developed Busch Agricultural Resources, Inc. and released in 2008.', {'entities': [(68, 72, 'DATE'), (17, 51, 'ORG')]}),
    ('It was derived from the cross 6B94-7378/C96-2292.', {'entities': [(30, 48, 'PED')]}),
    ('It is a Midwestern cultivar, well adapted for Minnesota, North Dakota, Idaho and Montana.', {'entities': [(46, 55, 'GPE'), (57, 69, 'GPE'), (71, 76, 'GPE'), (81, 88, 'GPE')]}),
    ('Celebration has medium-early maturity, medium-short height and excellent agronomic performance and malt quality.', {'entities': [(0, 11, 'CVAR'), (16, 37, 'TRAT'), (39, 58, 'TRAT'), (99, 111, 'TRAT')]}),
    ('It has a mid-lax head type, rough awns, short rachilla hairs, and colorless aleurone.', {'entities': [(17, 21, 'PLAN'), (34, 38, 'PLAN'), (46, 60, 'PLAN'), (76, 84, 'PLAN')]}),
    ('It has improved reaction to Fusarium head blight and consistently lower DON content than Legacy and Tradition.', {'entities': [(7, 24, 'PPTD'), (28, 48, 'PATH'), (89, 95, 'CVAR'), (100, 109, 'CVAR')]}),
    ('At the time of release it was moderately resistant to Septoria and net blotch.', {'entities': [(30, 50, 'PPTD'), (54, 62, 'PATH'), (67, 77, 'PATH')]}),
    ('COMMANDER  Commander is a six-rowed spring feed barley.', {'entities': [(11, 20, 'CVAR'), (26, 35, 'TRAT'), (36, 42, 'TRAT'), (43, 47, 'TRAT'), (48, 54, 'CROP')]}),
    ('At the time of release it was resistant to stripe rust, stem rust, loose smut, moderately resistant to the surface-borne smuts and the spot-form of net blotch (and had adult plant resistance to some net-form pathotypes), and susceptible to scald, leaf rust, speckled leaf blotch, common root rot, and BYD.', {'entities': [(30, 39, 'PPTD'), (43, 54, 'PATH'), (56, 65, 'PATH'), (67, 77, 'PATH'), (79, 99, 'PPTD'), (107, 126, 'PATH'), (135, 158, 'PATH'), (180, 190, 'PPTD'), (199, 218, 'PATH'), (225, 236, 'PPTD'), (240, 245, 'PATH'), (247, 256, 'PATH'), (258, 278, 'PATH'), (280, 295, 'PATH'), (301, 304, 'PATH')]}),
    ('It was released by World Wide Wheat.', {'entities': [(19, 35, 'ORG')]}),
    ('Its experimental designation was 7128.', {'entities': [(33, 37, 'ALAS')]}),
    ('It is a semi-dwarf with stiff straw (fair lodging resistance) and medium late season maturity.', {'entities': [(8, 18, 'TRAT'), (24, 35, 'TRAT'), (37, 60, 'TRAT'), (66, 93, 'TRAT')]}),
    ('At the time of evaluation it was moderately susceptible to BYD and susceptible to scald, net blotch, stripe rust, leaf rust, and powdery mildew.', {'entities': [(33, 55, 'PPTD'), (59, 62, 'PATH'), (67, 78, 'PPTD'), (82, 87, 'PATH'), (89, 99, 'PATH'), (101, 112, 'PATH'), (114, 123, 'PATH'), (129, 143, 'PATH')]}),
    ('BARONESSE  Baronesse is a two-rowed spring feed barley.', {'entities': [(11, 20, 'CVAR'), (36, 42, 'TRAT'), (43, 47, 'TRAT'), (48, 54, 'CROP')]}),
    ('It was developed in Germany and first marketed in the United States by Western Plant Breeders in 1991.', {'entities': [(20, 27, 'GPE'), (54, 67, 'GPE'), (71, 93, 'ORG'), (97, 101, 'DATE')]}),
    ('It was selected from the cross ([(Mentor x Minerva) x mutant of Vada] x [(Carlsberg x Union) x (Opavsky x Salle) x Ricardo]) x (Oriol x 6153 P40)', {'entities': [(31, 145, 'PED')]}),
    ('It was selected from the cross WM861-5/TR118.', {'entities': [(31, 44, 'PED')]}),
('Straw strength is similar to B1202 (fair).', {'entities': [(0, 14, 'TRAT'), (29, 34, 'CVAR')]}),
    ('It has malt protein levels similar to Merit and Harrington, high levels of enzymes like Merit, and higher levels of extract and better malt modification than B1202.', {'entities': [(38, 43, 'CVAR'), (88, 93, 'CVAR'), (48, 58, 'CVAR'), (60, 82, 'TRAT'), (99, 123, 'TRAT'), (128, 152, 'TRAT'), (158, 163, 'CVAR')]}),
    ('At the time of release, its resistance to scald was similar to B1202 and slightly better than Harrington (moderately susceptible), and its resistance to net blotch (net form) was slightly better than B1202 and Harrington (moderately resistant).', {'entities': [(28, 38, 'PPTD'), (139, 149, 'PPTD'), (42, 47, 'PATH'), (63, 68, 'CVAR'), (200, 205, 'CVAR'), (94, 104, 'CVAR'), (210, 220, 'CVAR'), (106, 128, 'PPTD'), (153, 163, 'PATH'), (222, 242, 'PPTD')]}),
    ('At the time of evaluation it was resistant to stripe rust.', {'entities': [(33, 42, 'PPTD'), (46, 57, 'PATH')]}),
    ('ISHI  Ishi is a six-rowed spring feed barley.', {'entities': [(6, 10, 'CVAR'), (16, 25, 'TRAT'), (26, 32, 'TRAT'), (33, 37, 'TRAT'), (38, 44, 'CROP')]}),
    ('It was released by the California AES in 2005.', {'entities': [(23, 37, 'ORG'), (41, 45, 'DATE')]}),
    ('It was selected from the cross UC 828/UC 960.', {'entities': [(31, 44, 'PED')]}),
    ('Its experimental designations were UC 1047 and UCD PYT99 A-13.', {'entities': [(35, 42, 'ALAS'), (47, 61, 'ALAS')]}),
    ('Ishi has the sdw1 gene and is short statured, averaging 84.6 cm, and is similar to UC 937 and 3.6 cm taller than UC 933, averaged over 32 location-years in Central Valley and Central Coast environments.', {'entities': [(0, 4, 'CVAR'), (5, 22, 'TRAT'), (30, 44, 'TRAT'), (83, 89, 'CVAR'), (113, 119, 'CVAR'), (156, 170, 'GPE'), (175, 188, 'GPE')]}),
    ('it was superior to UC 937 but similar to UC 933 over 20 environments where lodging occurred.', {'entities': [(19, 25, 'CVAR'), (41, 47, 'CVAR')]}),
    ('For days to heading it averaged 4 days earlier than UC 937 and 3 days later than UC 933, but all three cultivars were similar for time to maturity (medium late).', {'entities': [(4, 19, 'TRAT'), (52, 58, 'CVAR'), (81, 87, 'CVAR'), (130, 146, 'TRAT')]}),
    ('It is heterogeneous for rough and smooth awns, having less than one-percent smooth awned plants.', {'entities': [(41, 45, 'PLAN')]}),
    ('The spike is waxy and semi-erect.', {'entities': [(4, 9, 'PLAN')]}),
    ('The kernels are covered and the aleurone is non-blue.', {'entities': [(4, 11, 'PLAN'), (32, 40, 'PLAN')]}),
    ('Grains are long (>10mm) and wrinkled, with hairs on the ventral furrow.', {'entities': [(0, 6, 'PLAN'), (43, 48, 'PLAN'), (56, 70, 'PLAN')]}),
    ('Rachilla hairs are long.', {'entities': [(0, 14, 'PLAN')]}),
    ('At the time of release Ishi was resistant to scald and powdery mildew, moderately resistant to stripe rust, BYD and net blotch, and moderately susceptible to leaf rust.', {'entities': [(23, 27, 'CVAR'), (32, 41, 'PPTD'), (45, 50, 'PATH'), (55, 69, 'PATH'), (71, 91, 'PPTD'), (95, 106, 'PATH'), (108, 111, 'PATH'), (116, 126, 'PATH'), (132, 154, 'PPTD'), (158, 167, 'PATH')]}),
    ('It subsequently became moderately susceptible to net blotch.', {'entities': [(23, 45, 'PPTD'), (49, 59, 'PATH')]}),
    ('Conrad is a two-rowed spring malting barley.', {'entities': [(0, 6, 'CVAR'), (12, 21, 'TRAT'), (22, 28, 'TRAT'), (29, 36, 'TRAT'), (37, 43, 'CROP')]}),
    ('Meltan is a two-rowed spring feed barley.', {'entities': [(0, 6, 'CVAR'), (12, 21, 'TRAT'), (22, 28, 'TRAT'), (29, 33, 'TRAT'), (34, 40, 'CROP')]}),
    ('It was marketed by Adams Grain Company in California.', {'entities': [(19, 38, 'ORG'), (42, 52, 'GPE')]}),
    ('Plants are late maturing and moderately short (averaging about 32 inches in plant height) with fair straw strength.', {'entities': [(11, 24, 'TRAT'), (29, 45, 'TRAT'), (95, 114, 'TRAT')]}),
    ('At the time of evaluation it was resistant to leaf rust and powdery mildew, moderately resistant to stripe rust, and susceptible to scald, net blotch and BYD.', {'entities': [(33, 42, 'PPTD'), (46, 55, 'PATH'), (60, 74, 'PATH'), (76, 96, 'PPTD'), (100, 111, 'PATH'), (117, 128, 'PPTD'), (132, 137, 'PATH'), (139, 149, 'PATH'), (154, 157, 'PATH')]}),
    ('MERIT 57 Merit 57 is a two-rowed spring malting barley.', {'entities': [(9, 17, 'CVAR'), (23, 32, 'TRAT'), (33, 39, 'TRAT'), (40, 47, 'TRAT'), (48, 54, 'CROP')]}),
    ('It was released by Busch Agricultural Resources in 2009.', {'entities': [(19, 47, 'ORG'), (51, 55, 'DATE')]}),
    ('It was released by Busch Agricultural Resources in 2005.', {'entities': [(19, 47, 'ORG'), (51, 55, 'DATE')]}),
    ('It was selected from the backcross Merit//Merit/2B94-5744 made in 1996 in Fort Collins, Colorado.', {'entities': [(35, 57, 'PED'), (66, 70, 'DATE'), (74, 96, 'GPE')]}),
    ('It has high levels of enzymes, -amylase and diastatic power, similar to the cultivar Merit.', {'entities': [(7, 29, 'TRAT'), (31, 39, 'TRAT'), (44, 59, 'TRAT'), (85, 90, 'CVAR')]}),
    ('Overall malting profile is equivalent to or superior to Merit, with complete and balanced modification and superior levels of malt extract.', {'entities': [(56, 61, 'CVAR'), (116, 138, 'TRAT')]}),
    ('Merit 57 is rough awned and late maturing, with high yield potential.', {'entities': [(0, 8, 'CVAR'), (12, 23, 'TRAT'), (28, 41, 'TRAT'), (48, 68, 'TRAT')]}),
    ('It has intermediate plant height and straw strength, and slightly better lodging resistance than AC Metcalfe.', {'entities': [(20, 32, 'TRAT'), (37, 51, 'TRAT'), (73, 91, 'TRAT'), (97, 108, 'CVAR')]}),
    ('It has good resistance to shattering and fair to good tolerance of straw breakage and drought.', {'entities': [(12, 36, 'TRAT'), (54, 81, 'TRAT'), (86, 93, 'TRAT')]}),
    ('Merit 57 has denser pubescence on the blade of the flag leaf than Merit.', {'entities': [(0, 8, 'CVAR'), (13, 30, 'TRAT'), (51, 60, 'PLAN'), (66, 71, 'CVAR')]}),
    ('The anthocyanin coloration of the flag leaf auricles is weaker than Merit.', {'entities': [(4, 26, 'TRAT'), (34, 52, 'PLAN'), (68, 73, 'CVAR')]}),
    ('The spike emergence is earlier than Merit.', {'entities': [(4, 19, 'TRAT'), (36, 41, 'CVAR')]}),
    ('The tips of the lemma awns of Merit 57 have weaker anthocyanin coloration than Harrington.', {'entities': [(16, 26, 'PLAN'), (30, 38, 'CVAR'), (51, 73, 'TRAT'), (79, 89, 'CVAR')]}),
    ('It was selected from the cross B1215/B88-5336.', {'entities': [(31, 45, 'PED')]}),
    ('Merit 57 has a laxer spike than Merit.', {'entities': [(0, 8, 'CVAR'), (21, 26, 'PLAN'), (32, 37, 'CVAR')]}),
    ('The spike is shorter than Merit and Harrington.', {'entities': [(4, 9, 'PLAN'), (26, 31, 'CVAR'), (36, 46, 'CVAR')]}),
    ('The basal marking on the kernel of Merit 57 is horseshoe shaped while it is transverse creased in Harrington.', {'entities': [(4, 17, 'PLAN'), (25, 31, 'PLAN'), (35, 43, 'CVAR'), (98, 108, 'CVAR')]}),
    ('Merit 57 has a longer kernel than Harrington.', {'entities': [(0, 8, 'CVAR'), (22, 28, 'PLAN')]}),
    ('Merit 57 has better scald resistance than Merit.', {'entities': [(0, 8, 'CVAR'), (20, 25, 'PATH'), (26, 36, 'PPTD'), (42, 47, 'CVAR')]}),
    ('At the time of release Merit 57 was moderately susceptible to scald, net blotch, race MCC of stem rust, and spot blotch, and susceptible to BYD.', {'entities': [(23, 31, 'CVAR'), (36, 58, 'PPTD'), (62, 67, 'PATH'), (69, 79, 'PATH'), (81, 102, 'PATH'), (108, 119, 'PATH'), (125, 136, 'PPTD'), (140, 143, 'PATH')]}),
    ('MILLENNIUM  Millennium is a six-rowed spring feed barley.', {'entities': [(12, 22, 'CVAR'), (28, 37, 'TRAT'), (38, 44, 'TRAT'), (45, 49, 'TRAT'), (50, 56, 'CROP')]}),
    ('It was released by the Utah AES in 2000.', {'entities': [(23, 31, 'ORG'), (35, 39, 'DATE')]}),
    ('Its experimental designation was 2B96-5057.', {'entities': [(33, 42, 'ALAS')]}),
    ('Its experimental designations were UT94B1058-4603 and UT 4603.', {'entities': [(35, 49, 'ALAS'), (54, 61, 'ALAS')]}),
    ('It has consistently plump grain.', {'entities': [(26, 31, 'PLAN')]}),
    ('It has medium late maturity', {'entities': [(7, 27, 'TRAT')]}),
    ('Crop Science 46:1396 (2006)', {'entities': [(0, 27, 'JRNL')]}),
    ('It was selected from the cross WA Sel 3564/Unitan//UT Short2*2.', {'entities': [(31, 62, 'PED')]}),
    ('At the time of evaluation it was resistant to stripe rust and moderately susceptible to scald, net blotch, and BYD', {'entities': [(33, 42, 'PPTD'), (46, 57, 'PATH'), (62, 84, 'PPTD'), (88, 93, 'PATH'), (95, 105, 'PATH'), (111, 114, 'PATH')]})]
