TRAIN_DATA = [
    ('32  moderately resistant to leaf rust and net blotch, and susceptible to BYD, scald, and powdery mildew.', {'entities': [(4, 24, 'PPTD'), (28, 37, 'PATH'), (42, 52, 'PATH'), (58, 69, 'PPTD'), (73, 76, 'PATH'), (78, 83, 'PATH'), (89, 103, 'PATH')]}),
    ('At the time of evaluation it was moderately resistant to net blotch, leaf rust, and BYD, moderately susceptible to powdery mildew, and susceptible to scald.', {'entities': [(33, 53, 'PPTD'), (57, 67, 'PATH'), (69, 78, 'PATH'), (84, 87, 'PATH'), (89, 111, 'PPTD'), (115, 129, 'PATH'), (135, 146, 'PPTD'), (150, 155, 'PATH')]}),
    ('Sunbar Brand 550 is a two-rowed spring feed barley.', {'entities': [(0, 16, 'CVAR'), (22, 31, 'TRAT'), (32, 38, 'TRAT'), (39, 43, 'TRAT'), (44, 50, 'CROP')]}),
    ('Sunbar Brand 560 is a two-rowed spring feed barley.', {'entities': [(0, 16, 'CVAR'), (22, 31, 'TRAT'), (32, 38, 'TRAT'), (39, 43, 'TRAT'), (44, 50, 'CROP')]}),
    ('Co. It is medium maturing and medium tall, with fair straw strength.', {'entities': [(17, 25, 'TRAT'), (37, 41, 'TRAT'), (53, 67, 'TRAT')]}),
    ('It was released by Sunderman Breeding Co. in 1995.', {'entities': [(19, 40, 'ORG'), (45, 49, 'DATE')]}),
    ('It was selected from the cross Eight Twelve/Steptoe.', {'entities': [(31, 51, 'PED')]}),
    ('Its experimental designation was SDM 208B.', {'entities': [(33, 41, 'ALAS')]}),
    ('It has intermediate height and good straw strength.', {'entities': [(20, 26, 'TRAT'), (36, 50, 'TRAT')]}),
    ('At the time of evaluation it was moderately resistant to BYD and susceptible to stripe rust.', {'entities': [(33, 53, 'PPTD'), (57, 60, 'PATH'), (65, 76, 'PPTD'), (80, 91, 'PATH')]}),
    ('Sunbar Brand 401 is a six-rowed spring feed barley.', {'entities': [(0, 16, 'CVAR'), (22, 31, 'TRAT'), (32, 38, 'TRAT'), (39, 43, 'TRAT'), (44, 50, 'CROP')]}),
    ('Sunstar Prince is a six-rowed spring feed barley.', {'entities': [(0, 14, 'CVAR'), (20, 29, 'TRAT'), (30, 36, 'TRAT'), (37, 41, 'TRAT'), (42, 48, 'CROP')]}),
    ('It was released by Sunderman Breeding Co. in 1995.', {'entities': [(19, 40, 'ORG'), (45, 49, 'DATE')]}),
    ('It was selected from the cross Eight Twelve/Steptoe.', {'entities': [(31, 51, 'PED')]}),
    ('Its experimental designation was SDM 306B.', {'entities': [(33, 41, 'ALAS')]}),
    ('It has medium maturity, medium height (several inches shorter than Steptoe) with fair straw strength (stronger straw than Steptoe).', {'entities': [(14, 22, 'TRAT'), (31, 37, 'TRAT'), (54, 61, 'TRAT'), (67, 74, 'CVAR'), (86, 100, 'TRAT'), (102, 110, 'TRAT'), (122, 129, 'CVAR')]}),
    ('At the time of evaluation it was susceptible to BYD and stripe rust.', {'entities': [(33, 44, 'PPTD'), (48, 51, 'PATH'), (56, 67, 'PATH')]}),
    ('SUTTER  Sutter is a six-rowed spring feed barley.', {'entities': [(8, 14, 'CVAR'), (20, 29, 'TRAT'), (30, 36, 'TRAT'), (37, 41, 'TRAT'), (42, 48, 'CROP')]}),
    ('It was released by Northrup-King & Co. in 1980.', {'entities': [(19, 37, 'ORG'), (42, 46, 'DATE')]}),
    ('It was released by the University of California AES in 1971.', {'entities': [(37, 51, 'ORG'), (55, 59, 'DATE')]}),
    ('It is tall with moderately strong straw and long, medium-dense erect heads.', {'entities': [(6, 10, 'TRAT'), (34, 39, 'PLAN'), (69, 74, 'PLAN')]}),
    ('Early growth is semi-prostrate.', {'entities': [(16, 30, 'TRAT')]}),
    ('It is late maturing', {'entities': [(11, 19, 'TRAT')]}),
    ('It is rough awned and', {'entities': [(12, 17, 'PLAN')]}),
    ('kernels are moderately large with colorless aleurone and long rachilla with short hairs.', {'entities': [(0, 7, 'PLAN'), (44, 52, 'PLAN'), (62, 70, 'PLAN'), (82, 87, 'PLAN')]}),
    ('It is similar to Winter Tennessee in ability to tolerate cold, wet soils.', {'entities': [(17, 33, 'CVAR'), (48, 72, 'TRAT')]}),
    ('At the time of evaluation it was resistant to BYD (carries the Yd2 gene from CIho 1237), and moderately resistant to scald, powdery mildew, leaf rust and net blotch.', {'entities': [(33, 42, 'PPTD'), (46, 49, 'PATH'), (93, 113, 'PPTD'), (117, 122, 'PATH'), (124, 138, 'PATH'), (140, 149, 'PATH'), (154, 164, 'PATH')]}),
    ('TANGO  Tango is a six-rowed spring feed barley.', {'entities': [(7, 12, 'CVAR'), (18, 27, 'TRAT'), (28, 34, 'TRAT'), (35, 39, 'TRAT'), (40, 46, 'CROP')]}),
    ('It was released by the Oregon AES in 2000.', {'entities': [(23, 33, 'ORG'), (37, 41, 'DATE')]}),
    ('Its experimental designations were SR58-4 and OR2967007.', {'entities': [(35, 41, 'ALAS'), (46, 55, 'ALAS')]}),
    ('It is early maturing, mid-tall, with fair straw strength (the same height, lodging reaction and maturity as Steptoe).', {'entities': [(12, 20, 'TRAT'), (22, 30, 'TRAT'), (42, 56, 'TRAT'), (67, 73, 'TRAT'), (75, 91, 'TRAT'), (108, 115, 'CVAR')]}),
    ('a sister line of Orca, is Calicuchima-sib/Bowman.', {'entities': [(17, 21, 'CVAR'), (26, 48, 'PED')]}),
    ('Tango has long and smooth awns, white aleurone and short', {'entities': [(0, 5, 'CVAR'), (26, 30, 'PLAN'), (38, 46, 'PLAN')]}),
    ('Its experimental designation was NK214W.', {'entities': [(33, 39, 'ALAS')]}),
    ('It has medium maturity, short stature, very good straw strength and characteristics similar to Kombyne.', {'entities': [(14, 22, 'TRAT'), (30, 37, 'TRAT'), (49, 63, 'TRAT'), (95, 102, 'CVAR')]}),
    ('It has white aleurone.', {'entities': [(13, 21, 'PLAN')]}),
    ('It was selected from the cross MINN 64-98-8/NU//CM67.', {'entities': [(31, 52, 'PED')]}),
    ('It was developed by Northrup-King & Co.', {'entities': [(20, 38, 'ORG')]}),
    ('Sunstar Double is a six-rowed facultative (winter/spring) feed barley.', {'entities': [(0, 14, 'CVAR'), (20, 29, 'TRAT'), (30, 41, 'TRAT'), (58, 62, 'TRAT'), (63, 69, 'CROP')]}),
    ('It was selected from the cross CIho 1237/2*Winter Tennessee.', {'entities': [(31, 59, 'PED')]}),
    ('Crop Science 13:285 (1973)', {'entities': [(0, 26, 'JRNL')]}),
    ('It was selected from the cross Orca-sib/2*Steptoe.', {'entities': [(31, 49, 'PED')]})
]
