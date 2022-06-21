TRAIN_DATA = [
    ('17  is tall (similar in height to Stander and about 5 cm shorter than Robust) and has fair straw strength (straw strength superior to Robust, Stander and Foster).', {'entities': [(7, 11, 'TRAT'), (24, 30, 'TRAT'), (34, 41, 'CVAR'), (70, 76, 'CVAR'), (91, 105, 'TRAT'), (107, 121, 'TRAT'), (134, 140, 'CVAR'), (142, 149, 'CVAR'), (154, 160, 'CVAR')]}),
    ('It is medium late maturing (has a heading date similar to Robust).', {'entities': [(18, 26, 'TRAT'), (34, 46, 'TRAT'), (58, 64, 'CVAR')]}),
    ('Early 28 is a six-rowed spring feed barley.', {'entities': [(0, 8, 'CVAR'), (14, 23, 'TRAT'), (24, 30, 'TRAT'), (31, 35, 'TRAT'), (36, 42, 'CROP')]}),
    ('It was released by the University of Arizona.', {'entities': [(23, 44, 'ORG')]}),
    ('Its experimental designation was 80-MA-666-172.', {'entities': [(33, 46, 'ALAS')]}),
    ('It is very early maturing.', {'entities': [(17, 25, 'TRAT')]}),
    ('Early 32 is a six-rowed spring feed barley.', {'entities': [(0, 8, 'CVAR'), (14, 23, 'TRAT'), (24, 30, 'TRAT'), (31, 35, 'TRAT'), (36, 42, 'CROP')]}),
    ('It was released by the University of Arizona.', {'entities': [(23, 44, 'ORG')]}),
    ('Drummond has semi-smooth awns and its covered kernels have long rachilla hairs and a white aleurone.', {'entities': [(0, 8, 'CVAR'), (25, 29, 'PLAN'), (46, 53, 'PLAN'), (64, 78, 'PLAN'), (91, 99, 'PLAN')]}),
    ('Its experimental designation was 80-MA-666-173.', {'entities': [(33, 46, 'ALAS')]}),
    ('It is very early maturing and has medium-short plant height and poor straw strength.', {'entities': [(17, 25, 'TRAT'), (47, 59, 'TRAT'), (69, 83, 'TRAT')]}),
    ('At the time of evaluation it was moderately resistant to net blotch, moderately susceptible to leaf rust, and susceptible to scald, BYD, and powdery mildew.', {'entities': [(33, 53, 'PPTD'), (57, 67, 'PATH'), (69, 91, 'PPTD'), (95, 104, 'PATH'), (110, 121, 'PPTD'), (125, 130, 'PATH'), (132, 135, 'PATH'), (141, 155, 'PATH')]}),
    ('Ellinor is a two-rowed spring malting and feed barley.', {'entities': [(0, 7, 'CVAR'), (13, 22, 'TRAT'), (23, 29, 'TRAT'), (30, 37, 'TRAT'), (42, 46, 'TRAT'), (47, 53, 'CROP')]}),
    ('It was received for testing from Lynn Gallagher, UC Davis, in 1999.', {'entities': [(49, 57, 'ORG'), (62, 66, 'DATE')]}),
    ('It is late maturing and has medium plant height and fair straw strength.', {'entities': [(11, 19, 'TRAT'), (35, 47, 'TRAT'), (57, 71, 'TRAT')]}),
    ('At the time of evaluation it was moderately susceptible to BYD.', {'entities': [(33, 55, 'PPTD'), (59, 62, 'PATH')]}),
    ('Spikes are medium-lax, medium-long, and semi-erect.', {'entities': [(0, 6, 'PLAN')]}),
    ('Excel is a six-rowed spring malting barley.', {'entities': [(0, 5, 'CVAR'), (11, 20, 'TRAT'), (21, 27, 'TRAT'), (28, 35, 'TRAT'), (36, 42, 'CROP')]}),
    ('It was released by the Minnesota AES in 1990.', {'entities': [(23, 36, 'ORG'), (40, 44, 'DATE')]}),
    ('Its experimental designation was MN 52.', {'entities': [(33, 38, 'ALAS')]}),
    ('It is medium late maturing (similar to Robust) and is mid-tall (shorter than Morex or Robust) with fair straw strength (similar to Robust in lodging reaction).', {'entities': [(18, 26, 'TRAT'), (39, 45, 'CVAR'), (54, 62, 'TRAT'), (77, 82, 'CVAR'), (86, 92, 'CVAR'), (104, 118, 'TRAT'), (131, 137, 'CVAR'), (141, 148, 'TRAT')]}),
    ('Spikes are medium-lax, medium-long, and semi-erect.', {'entities': [(0, 6, 'PLAN')]}),
    ('Excel has smooth-awns, covered medium-sized kernels that have long hairs on the rachilla and a white aleurone.', {'entities': [(0, 5, 'CVAR'), (10, 21, 'PLAN'), (44, 51, 'PLAN'), (67, 72, 'PLAN'), (80, 88, 'PLAN'), (101, 109, 'PLAN')]}),
    ('Hulls are adhering and wrinkled.', {'entities': [(0, 5, 'PLAN')]}),
    ('It has more plump kernels and higher malt extract than the 6-rowed industry standard Morex.', {'entities': [(18, 25, 'PLAN'), (37, 49, 'TRAT'), (85, 90, 'CVAR')]}),
    ('Central and lateral veins are moderately prominent.', {'entities': [(12, 25, 'PLAN')]}),
    ('There are few to no barbs on lateral veins.', {'entities': [(20, 25, 'PLAN'), (29, 42, 'PLAN')]}),
    ('The crease is narrow at the base and flared toward the beard end.', {'entities': [(4, 10, 'PLAN'), (28, 32, 'PLAN'), (55, 60, 'PLAN')]}),
    ('Lateral kernels are moderately twisted.', {'entities': [(0, 15, 'PLAN')]}),
    ('Excel''s malting quality is similar or superior to Morex.', {'entities': [(0, 5, 'CVAR'), (8, 23, 'TRAT'), (50, 55, 'CVAR')]}),
    ('At the time of release it was resistant to stem rust (contains the T-gene for resistance) and spot blotch, moderately resistant to net blotch, and susceptible to loose smut.', {'entities': [(30, 39, 'PPTD'), (43, 52, 'PATH'), (94, 105, 'PATH'), (107, 127, 'PPTD'), (131, 141, 'PATH'), (147, 158, 'PPTD'), (162, 172, 'PATH')]}),
    ('Crop Science 31:227 (1991)    FARMINGTON  Farmington is a two-rowed spring feed barley.', {'entities': [(0, 26, 'JRNL'), (42, 52, 'CVAR'), (58, 67, 'TRAT'), (68, 74, 'TRAT'), (75, 79, 'TRAT'), (80, 86, 'CROP')]}),
    ('It was released by Washington State University Agricultural Research Center, Idaho and Oregon AESs, and USDA-ARS in 2001.', {'entities': [(19, 75, 'ORG'), (77, 98, 'ORG'), (104, 112, 'ORG'), (116, 120, 'DATE')]}),
    ('It was selected from the cross Klages/WA8189-69//Piroline SD Mutant/Valticky SD Mutant/3/Maresi.', {'entities': [(31, 95, 'PED')]}),
    ('Grain protein, wort protein, and the ratio of wort protein to total protein of Drummond are slightly lower', {'entities': [(0, 13, 'TRAT'), (15, 27, 'TRAT'), (37, 75, 'TRAT'), (79, 87, 'CVAR')]}),
    ('Its experimental designation was WA9504-94.', {'entities': [(33, 42, 'ALAS')]}),
    ('It has medium-short plant height (averages', {'entities': [(20, 32, 'TRAT')]}),
    ('60 cm compared to 68 cm for Baronesse) and good straw strength.', {'entities': [(28, 37, 'CVAR'), (48, 62, 'TRAT')]}),
    ('It has mid-season maturity, similar to Baronesse.', {'entities': [(18, 26, 'TRAT'), (39, 48, 'CVAR')]}),
    ('Spikes are lax and slightly nodding.', {'entities': [(0, 6, 'PLAN')]}),
    ('Awns are long and rough.', {'entities': [(0, 4, 'PLAN')]}),
    ('Kernels are covered, with white aleurone, long rachilla hairs, a narrow crease, prominent veins, and wrinkled lemma and palea on the distal half.', {'entities': [(0, 7, 'PLAN'), (32, 40, 'PLAN'), (47, 61, 'PLAN'), (72, 78, 'PLAN'), (90, 95, 'PLAN'), (110, 115, 'PLAN'), (120, 125, 'PLAN')]}),
    ('Kernels are plump and tapering at both ends.', {'entities': [(0, 7, 'PLAN')]}),
    ('At the time of release it was resistant to leaf rust and had partial resistance or tolerance to stripe rust.', {'entities': [(30, 39, 'PPTD'), (43, 52, 'PATH'), (61, 79, 'PPTD'), (83, 92, 'PPTD'), (96, 107, 'PATH')]}),
    ('that that of Morex.', {'entities': [(13, 18, 'CVAR')]}),
    ('Enzymatic activity of Drummond and Morex are similar.', {'entities': [(0, 18, 'TRAT'), (22, 30, 'CVAR'), (35, 40, 'CVAR')]}),
    ('At the time of release Drummond was resistant to spot blotch, moderately susceptible to stem rust (race Qcc), net blotch, and BYD, and susceptible to loose smut, scald, several Septoria sp and Fusarium spp that attack barley in the Midwest.', {'entities': [(23, 31, 'CVAR'), (36, 45, 'PPTD'), (49, 60, 'PATH'), (62, 84, 'PPTD'), (88, 97, 'PATH'), (110, 120, 'PATH'), (126, 129, 'PATH'), (135, 146, 'PPTD'), (150, 160, 'PATH'), (162, 167, 'PATH'), (177, 188, 'PATH'), (193, 205, 'PATH')]}),
    ('Crop Science 42: 664-665 (2002)', {'entities': [(0, 31, 'JRNL')]}),
    ('It was selected from the cross Cree/Bonanza//Manker/3/2*Robust.', {'entities': [(31, 62, 'PED')]}),
    ('Crop Science 42:2209-2210 (2002)', {'entities': [(0, 32, 'JRNL')]})
]