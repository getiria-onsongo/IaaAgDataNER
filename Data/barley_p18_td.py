TRAIN_DATA = [
    ('Fiesta is a six-rowed spring feed barley.', {'entities': [(0, 6, 'CVAR'), (12, 21, 'TRAT'), (22, 28, 'TRAT'), (29, 33, 'TRAT'), (34, 40, 'CROP')]}),
    ('Kernels are mid-long to long with long rachilla hairs, semi-wrinkled hulls, and white aleurone.', {'entities': [(0, 7, 'PLAN'), (39, 53, 'PLAN'), (69, 74, 'PLAN'), (86, 94, 'PLAN')]}),
    ('At the time of evaluation Fiesta was resistant to BYD, and susceptible to moderately susceptible to net blotch, leaf rust, stripe rust, scald and powdery mildew.', {'entities': [(26, 32, 'CVAR'), (37, 46, 'PPTD'), (50, 53, 'PATH'), (59, 70, 'PPTD'), (74, 96, 'PPTD'), (100, 110, 'PATH'), (112, 121, 'PATH'), (123, 134, 'PATH'), (136, 141, 'PATH'), (146, 160, 'PATH')]}),
    ('FOSTER  Foster is a six-rowed spring malting and feed barley.', {'entities': [(8, 14, 'CVAR'), (20, 29, 'TRAT'), (30, 36, 'TRAT'), (37, 44, 'TRAT'), (49, 53, 'TRAT'), (54, 60, 'CROP')]}),
    ('It was released by North Dakota AES in 1995.', {'entities': [(19, 35, 'ORG'), (39, 43, 'DATE')]}),
    ('It was selected from the cross Robust/6/Glenn/4/Nordic//Dickson/Trophy/3/Azure/5/Glenn/Karl.', {'entities': [(31, 91, 'PED')]}),
    ('Its experimental designation was ND11055.', {'entities': [(33, 40, 'ALAS')]}),
    ('It has midseason maturity', {'entities': [(17, 25, 'TRAT')]}),
    ('(heads 1 day earlier than Robust), is mid-tall (4 cm shorter than Robust), and has moderately strong straw.', {'entities': [(26, 32, 'CVAR'), (38, 46, 'TRAT'), (53, 60, 'TRAT'), (66, 72, 'CVAR'), (101, 106, 'PLAN')]}),
    ('Foster has semi-smooth awns.', {'entities': [(0, 6, 'CVAR'), (23, 27, 'PLAN')]}),
    ('The spike is medium lax, medium long, and semi-erect.', {'entities': [(4, 9, 'PLAN')]}),
    ('Kernels are covered.', {'entities': [(0, 7, 'PLAN')]}),
    ('Rachilla hairs are long.', {'entities': [(0, 14, 'PLAN')]}),
    ('Aleurone is white.', {'entities': [(0, 8, 'PLAN')]}),
    ('Central and lateral veins are moderately prominent.', {'entities': [(12, 25, 'PLAN')]}),
    ('There are no barbs on lateral veins.', {'entities': [(13, 18, 'PLAN'), (22, 35, 'PLAN')]}),
    ('The crease is V-shaped, narrow at the base.', {'entities': [(4, 10, 'PLAN'), (38, 42, 'PLAN')]}),
    ('Lateral kernels are moderately twisted.', {'entities': [(0, 15, 'PLAN')]}),
    ('Percent grain protein is up to 1.5 percentage units lower than Robust.', {'entities': [(0, 21, 'TRAT'), (63, 69, 'CVAR')]}),
    ('Foster has more plump kernels and similar malt extract and enzymatic activity as the six-rowed industry standard Morex.', {'entities': [(0, 6, 'CVAR'), (22, 29, 'PLAN'), (42, 54, 'TRAT'), (59, 77, 'TRAT'), (113, 118, 'CVAR')]}),
    ('At the time of release it was resistant to spot blotch and stem rust (except race QCC), moderately susceptible to net blotch and BYD, and susceptible to loose smut, scald, stripe rust, and to several Septoria sp and Fusarium spp that attack barley in the Midwest.', {'entities': [(30, 39, 'PPTD'), (43, 54, 'PATH'), (59, 68, 'PATH'), (88, 110, 'PPTD'), (114, 124, 'PATH'), (129, 132, 'PATH'), (138, 149, 'PPTD'), (153, 163, 'PATH'), (165, 170, 'PATH'), (172, 183, 'PATH'), (200, 211, 'PATH'), (216, 228, 'PATH')]}),
    ('Galena is a two-rowed spring malting barley.', {'entities': [(0, 6, 'CVAR'), (12, 21, 'TRAT'), (22, 28, 'TRAT'), (29, 36, 'TRAT'), (37, 43, 'CROP')]}),
    ('It was released by Coors Brewing Company in 1993.', {'entities': [(19, 40, 'ORG'), (44, 48, 'DATE')]}),
    ('It was selected from the cross Triumph/Crystal.', {'entities': [(31, 46, 'PED')]}),
    ('It has medium late maturity (1 day earlier than Triumph and 1 day later than Crystal), and short to medium length strong straw.', {'entities': [(19, 27, 'TRAT'), (48, 55, 'CVAR'), (77, 84, 'CVAR'), (121, 126, 'PLAN')]}),
    ('Spikes are semi-lax and nodding.', {'entities': [(0, 6, 'PLAN')]}),
    ('Rachis edges are hairy.', {'entities': [(0, 12, 'PLAN')]}),
    ('Awns are rough.', {'entities': [(0, 4, 'PLAN')]}),
    ('The glume is half the length of the lemma.', {'entities': [(4, 9, 'PLAN'), (36, 41, 'PLAN')]}),
    ('Long hairs completely cover the glume.', {'entities': [(5, 10, 'PLAN'), (32, 37, 'PLAN')]}),
    ('Glume awns are equal in length to the glume.', {'entities': [(0, 10, 'PLAN'), (38, 43, 'PLAN')]}),
    ('The hull is finely wrinkled.', {'entities': [(4, 8, 'PLAN')]}),
    ('The aleurone is colorless.', {'entities': [(4, 12, 'PLAN')]}),
    ('Rachilla hairs are long.', {'entities': [(0, 14, 'PLAN')]}),
    ('Lateral veins are moderately prominent.', {'entities': [(0, 13, 'PLAN')]}),
    ('There are no barbs on lateral veins.', {'entities': [(13, 18, 'PLAN'), (22, 35, 'PLAN')]}),
    ('Fiesta is a semi-dwarf with stiff straw (good lodging resistance) and medium early to early maturity.', {'entities': [(12, 22, 'TRAT'), (28, 39, 'TRAT'), (46, 64, 'TRAT'), (92, 100, 'TRAT')]}),
    ('The crease is narrow, slightly V-shaped from the base.', {'entities': [(4, 10, 'PLAN'), (49, 53, 'PLAN')]}),
    ('At the time of evaluation it was moderately susceptible to stripe rust and susceptible to scald and BYD.', {'entities': [(33, 55, 'PPTD'), (59, 70, 'PATH'), (75, 86, 'PPTD'), (90, 95, 'PATH'), (100, 103, 'PATH')]}),
    ('Gallatin is a two-rowed spring feed barley.', {'entities': [(0, 8, 'CVAR'), (14, 23, 'TRAT'), (24, 30, 'TRAT'), (31, 35, 'TRAT'), (36, 42, 'CROP')]}),
    ('It was jointly released by the USDA-ARS and the Montana and Idaho AESs in 1986.', {'entities': [(31, 39, 'ORG'), (48, 70, 'ORG'), (74, 78, 'DATE')]}),
    ('It was selected from the cross Summit/Hector.', {'entities': [(31, 44, 'PED')]}),
    ('Its experimental designation was MT 313104.', {'entities': [(33, 42, 'ALAS')]}),
    ('It has midseason maturity (1 day earlier in heading than Hector).', {'entities': [(17, 25, 'TRAT'), (44, 51, 'TRAT'), (57, 63, 'CVAR')]}),
    ('It is mid-tall with fair straw strength (3 cm shorter with much stiffer straw compared to Hector).', {'entities': [(6, 14, 'TRAT'), (25, 39, 'TRAT'), (72, 77, 'PLAN'), (90, 96, 'CVAR')]}),
    ('Spikes are semi-nodding before maturity with rough awns.', {'entities': [(0, 6, 'PLAN'), (51, 55, 'PLAN')]}),
    ('Kernels are white, midsized with short rachilla hairs and adhering, finely wrinkled hulls.', {'entities': [(0, 7, 'PLAN'), (39, 53, 'PLAN'), (84, 89, 'PLAN')]}),
    ('Veins are moderately prominent.', {'entities': [(0, 5, 'PLAN')]}),
    ('There are no barbs on lateral veins.', {'entities': [(13, 18, 'PLAN'), (22, 35, 'PLAN')]}),
    ('The crease is narrow at the base, tending to flare at the beard end.', {'entities': [(4, 10, 'PLAN'), (28, 32, 'PLAN'), (58, 63, 'PLAN')]}),
    ('Gallatin has slightly higher test weight with a similar percentage of plump kernels compared to Hector.', {'entities': [(0, 8, 'CVAR'), (29, 40, 'TRAT'), (56, 83, 'TRAT'), (96, 102, 'CVAR')]}),
    ('At the time of evaluation it was moderately resistant to net blotch and susceptible to scald.', {'entities': [(33, 53, 'PPTD'), (57, 67, 'PATH'), (72, 83, 'PPTD'), (87, 92, 'PATH')]}),
    ('The spike is strap-shaped, erect but not dense, with rachis edges covered with hairs.', {'entities': [(4, 9, 'PLAN'), (53, 65, 'PLAN'), (79, 84, 'PLAN')]}),
    ('Garnet is a two-rowed spring feed and malting barley.', {'entities': [(0, 6, 'CVAR'), (12, 21, 'TRAT'), (22, 28, 'TRAT'), (29, 33, 'TRAT'), (38, 45, 'TRAT'), (46, 52, 'CROP')]}),
    ('It was released by the USDA-ARS and the Idaho AES in 1999.', {'entities': [(23, 31, 'ORG'), (40, 49, 'ORG'), (53, 57, 'DATE')]}),
    ('Its experimental designation was 86Ab2317.', {'entities': [(33, 41, 'ALAS')]}),
    ('Glumes are more than one-half the length of the lemma with rough awns that are more than equal to the length of the glumes.', {'entities': [(0, 6, 'PLAN'), (48, 53, 'PLAN'), (65, 69, 'PLAN'), (116, 122, 'PLAN')]}),
    ('Lemma awns are long and rough with few teeth and no hairs.', {'entities': [(0, 10, 'PLAN'), (39, 44, 'PLAN'), (52, 57, 'PLAN')]}),
    ('Crop Science 37:1018 (1997)', {'entities': [(0, 27, 'JRNL')]}),
    ('Crop Science 27:815 (1987)', {'entities': [(0, 26, 'JRNL')]}),
    ('It was selected from the cross Harrington/78Ab6871(Crystal).', {'entities': [(31, 59, 'PED')]})
]
