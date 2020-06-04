TRAIN_DATA = [
    ('Devora is a two-rowed winter feed barley.', {'entities': [(0, 6, 'CVAR'), (12, 21, 'TRAT'), (22, 28, 'TRAT'), (29, 33, 'TRAT'), (34, 40, 'CROP')]}),
    ('It was released by the Oregon AES in 1991.', {'entities': [(23, 33, 'ORG'), (37, 41, 'DATE')]}),
    ('It was selected from the cross Ohio 67-23/Lakeland.', {'entities': [(31, 50, 'PED')]}),
    ('Its experimental designation was ORFB 77796.', {'entities': [(33, 43, 'ALAS')]}),
    ('It is small headed, early maturing with medium height, good lodging resistance, and excellent winter hardiness (similar to Boyer).', {'entities': [(12, 18, 'TRAT'), (26, 34, 'TRAT'), (47, 53, 'TRAT'), (60, 78, 'TRAT'), (94, 110, 'TRAT'), (123, 128, 'CVAR')]}),
    ('At the time of evaluation it was tolerant to BYD, moderately susceptible to scald, and susceptible to stripe rust.', {'entities': [(33, 41, 'PPTD'), (45, 48, 'PATH'), (50, 72, 'PPTD'), (76, 81, 'PATH'), (87, 98, 'PPTD'), (102, 113, 'PATH')]}),
    ('HESK  Hesk is a six-rowed winter feed barley.', {'entities': [(6, 10, 'CVAR'), (16, 25, 'TRAT'), (26, 32, 'TRAT'), (33, 37, 'TRAT'), (38, 44, 'CROP')]}),
    ('It was released by the Oregon AES in 1980.', {'entities': [(23, 33, 'ORG'), (37, 41, 'DATE')]}),
    ('It was selected from the cross Ione/Luther.', {'entities': [(31, 42, 'PED')]}),
    ('It was released by Cebeco Seeds, the Netherlands.', {'entities': [(19, 31, 'ORG'), (37, 48, 'GPE')]}),
    ('It has medium-late season maturity, medium height, good lodging resistance, and fair winter hardiness.', {'entities': [(26, 34, 'TRAT'), (43, 49, 'TRAT'), (56, 74, 'TRAT'), (85, 101, 'TRAT')]}),
    ('Spikes are nearly lax and erect.', {'entities': [(0, 6, 'PLAN')]}),
    ('Rachis edge hairs are long.', {'entities': [(0, 17, 'PLAN')]}),
    ('Awns are rough and medium long.', {'entities': [(0, 4, 'PLAN')]}),
    ('Glumes are covered with short hairs.', {'entities': [(0, 6, 'PLAN'), (30, 35, 'PLAN')]}),
    ('The glume awn is nearly equal to glume length.', {'entities': [(4, 13, 'PLAN'), (33, 45, 'TRAT')]}),
    ('Hulls are adhering and smooth.', {'entities': [(0, 5, 'PLAN')]}),
    ('The kernel is medium size and medium long.', {'entities': [(4, 10, 'PLAN')]}),
    ('Aleurone is colorless, occasionally light blue.', {'entities': [(0, 8, 'PLAN')]}),
    ('Rachilla hairs are long.', {'entities': [(0, 14, 'PLAN')]}),
    ('Kernel veins are prominent, with several barbs on lateral veins.', {'entities': [(0, 12, 'PLAN'), (50, 63, 'PLAN')]}),
    ('The crease is narrow, V-shaped.', {'entities': [(4, 10, 'PLAN')]}),
    ('At the time of evaluation it was susceptible to scald, BYD, covered smut, and stripe rust.', {'entities': [(33, 44, 'PPTD'), (48, 53, 'PATH'), (55, 58, 'PATH'), (60, 72, 'PATH'), (78, 89, 'PATH')]}),
    ('HOODY  Hoody is a six-rowed winter (hooded) forage barley.', {'entities': [(7, 12, 'CVAR'), (18, 27, 'TRAT'), (28, 34, 'TRAT'), (44, 50, 'TRAT'), (51, 57, 'CROP')]}),
    ('It was released by the Oregon AES in 1995.', {'entities': [(23, 33, 'ORG'), (37, 41, 'DATE')]}),
    ('It was selected from a three-way cross, [Dicktoo/Cascade//Hiproly (winter hardy/winter-adapted//spring-high lysine)]', {'entities': [(41, 65, 'PED')]}),
    ('Its experimental designation was Fbw1001hdd.', {'entities': [(33, 43, 'ALAS')]}),
    ('It is moderately winter hardy and has good BYD tolerance.', {'entities': [(17, 29, 'TRAT'), (43, 56, 'TRAT')]}),
    ('It is tall with medium maturity and fair straw strength.', {'entities': [(6, 10, 'TRAT'), (23, 31, 'TRAT'), (41, 55, 'TRAT')]}),
    ('The spike is mid-dense.', {'entities': [(4, 9, 'PLAN')]}),
    ('The rachis is short and straight.', {'entities': [(4, 10, 'PLAN')]}),
    ('The collar is closed to V-shaped.', {'entities': [(4, 10, 'PLAN')]}),
    ('The glume is normal with a hooded awn.', {'entities': [(4, 9, 'PLAN')]}),
    ('The rachis edge has short hairs.', {'entities': [(4, 15, 'PLAN'), (26, 31, 'PLAN')]}),
    ('It is medium-late maturing and mid-tall with good straw strength.', {'entities': [(18, 26, 'TRAT'), (50, 64, 'TRAT')]}),
    ('The kernel is covered.', {'entities': [(4, 10, 'PLAN')]}),
    ('Lemma nerves appear smooth.', {'entities': [(0, 12, 'PLAN')]}),
    ('Rachilla hairs are short and abortive.', {'entities': [(0, 14, 'PLAN')]}),
    ('The hull is white.', {'entities': [(4, 8, 'PLAN')]}),
    ('The aleurone is white.', {'entities': [(4, 12, 'PLAN')]}),
    ('It is moderately resistant to scald, moderately susceptible to net blotch, and susceptible to stripe rust and leaf rust.', {'entities': [(6, 26, 'PPTD'), (30, 35, 'PATH'), (37, 59, 'PPTD'), (63, 73, 'PATH'), (79, 90, 'PPTD'), (94, 105, 'PATH'), (110, 119, 'PATH')]}),
    ('HUNDRED  Hundred is a six-rowed winter feed barley.', {'entities': [(9, 16, 'CVAR'), (22, 31, 'TRAT'), (32, 38, 'TRAT'), (39, 43, 'TRAT'), (44, 50, 'CROP')]}),
    ('It was released by the Washington Agricultural Research Center and Idaho and Oregon AESs in 1989.', {'entities': [(23, 62, 'ORG'), (67, 88, 'ORG'), (92, 96, 'DATE')]}),
    ('At the time of evaluation it was resistant to net blotch, stripe rust, and leaf rust.', {'entities': [(33, 42, 'PPTD'), (46, 56, 'PATH'), (58, 69, 'PATH'), (75, 84, 'PATH')]}),
    ('Its experimental designations were WA 066739 and WA1574-77.', {'entities': [(35, 44, 'ALAS'), (49, 58, 'ALAS')]}),
    ('It is a semi-dwarf with medium height and medium late maturity.', {'entities': [(8, 18, 'TRAT'), (31, 37, 'TRAT'), (54, 62, 'TRAT')]}),
    ('It is slightly shorter than Boyer, similar in maturity and lodging resistance, with very good winter-hardiness.', {'entities': [(15, 22, 'TRAT'), (28, 33, 'CVAR'), (46, 54, 'TRAT'), (59, 77, 'TRAT'), (94, 110, 'TRAT')]}),
    ('It has club-shaped erect spikes with long rough awns.', {'entities': [(25, 31, 'PLAN'), (48, 52, 'PLAN')]}),
    ('The relatively small, globose kernels have semi-smooth, tightly adhering hulls with white aleurone, short rachilla hairs, and prominent veins.', {'entities': [(30, 37, 'PLAN'), (73, 78, 'PLAN'), (90, 98, 'PLAN'), (106, 120, 'PLAN'), (136, 141, 'PLAN')]}),
    ('The crease is narrow at the base and flaring toward the awn.', {'entities': [(4, 10, 'PLAN'), (56, 59, 'PLAN')]}),
    ('At the time of evaluation it was more resistant to scald, Cephalosporium stripe and powdery mildew than Kamiak, Boyer and Showin, moderately resistant to BYD, and susceptible to stripe rust.', {'entities': [(38, 47, 'PPTD'), (51, 56, 'PATH'), (58, 79, 'PATH'), (84, 98, 'PATH'), (104, 110, 'CVAR'), (112, 117, 'CVAR'), (122, 128, 'CVAR'), (130, 150, 'PPTD'), (154, 157, 'PATH'), (163, 174, 'PPTD'), (178, 189, 'PATH')]}),
    ('KAMIAK  Kamiak is a six-rowed winter feed barley.', {'entities': [(8, 14, 'CVAR'), (20, 29, 'TRAT'), (30, 36, 'TRAT'), (37, 41, 'TRAT'), (42, 48, 'CROP')]}),
    ('It was released by the Washington, Idaho and Oregon AESs in 1971.', {'entities': [(23, 56, 'ORG'), (60, 64, 'DATE')]}),
    ('Gwen is a six-rowed winter feed barley.', {'entities': [(0, 4, 'CVAR'), (10, 19, 'TRAT'), (20, 26, 'TRAT'), (27, 31, 'TRAT'), (32, 38, 'CROP')]}),
    ('It was selected from the cross Mosar x E82011-8805 x Magie', {'entities': [(31, 58, 'PED')]}),
    ('It was selected from the cross Luther/Hudson//Alpine/Svalof//White Winter/Triple Bearded Mariout-305.', {'entities': [(31, 100, 'PED')]}),
    ('Crop Science 31(1): 227 (1991)', {'entities': [(0, 30, 'JRNL')]})
]