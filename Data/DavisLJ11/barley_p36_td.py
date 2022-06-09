TRAIN_DATA = [
    ('36  evaluation it was resistant to scald, net blotch, and powdery mildew, moderately susceptible to BYD, and susceptible to loose smut and leaf rust.', {'entities': [(22, 31, 'PPTD'), (35, 40, 'PATH'), (42, 52, 'PATH'), (58, 72, 'PATH'), (74, 96, 'PPTD'), (100, 103, 'PATH'), (109, 120, 'PPTD'), (124, 134, 'PATH'), (139, 148, 'PATH')]}),
    ('At the time of evaluation it was moderately susceptible to leaf rust, net blotch, powdery mildew, and bacterial leaf blight, and susceptible to stem rust, scald, and BYD.', {'entities': [(33, 55, 'PPTD'), (59, 68, 'PATH'), (70, 80, 'PATH'), (82, 96, 'PATH'), (102, 123, 'PATH'), (129, 140, 'PPTD'), (144, 153, 'PATH'), (155, 160, 'PATH'), (166, 169, 'PATH')]}),
    ('Westbred Gustoe is a six-rowed spring feed barley.', {'entities': [(0, 15, 'CVAR'), (21, 30, 'TRAT'), (31, 37, 'TRAT'), (38, 42, 'TRAT'), (43, 49, 'TRAT')]}),
    ('It was released by Western Plant Breeders in 1982.', {'entities': [(19, 41, 'ORG'), (45, 49, 'DATE')]}),
    ('Its experimental designation was WPB 79-22.', {'entities': [(33, 42, 'ALAS')]}),
    ('Westbred Gustoe is a semi-dwarf with fair straw strength.', {'entities': [(0, 15, 'CVAR'), (21, 31, 'TRAT'), (42, 56, 'TRAT')]}),
    ('It is late in maturity and has a semi-prostrate growth habit in the Southwest when planted in November to February.', {'entities': [(14, 22, 'TRAT'), (48, 60, 'TRAT')]}),
    ('It heads about 2 days later than Steptoe when planted in the spring at Tulelake.', {'entities': [(3, 8, 'TRAT'), (33, 40, 'CVAR')]}),
    ('The spike is medium in length, parallel, mid-dense, and erect at maturity.', {'entities': [(4, 9, 'PLAN')]}),
    ('The basal rachis internode is straight and the rachis edges are covered with hairs.', {'entities': [(4, 26, 'PLAN'), (47, 59, 'PLAN'), (77, 82, 'PLAN')]}),
    ('The lemma awn is long and rough.', {'entities': [(4, 13, 'PLAN')]}),
    ('The glume awn is longer than the glume and is rough.', {'entities': [(4, 13, 'PLAN'), (33, 38, 'PLAN')]}),
    ('The glume is one-half the length of the lemma.', {'entities': [(4, 9, 'PLAN'), (40, 45, 'PLAN')]}),
    ('The rachilla hairs are long.', {'entities': [(4, 18, 'PLAN')]}),
    ('Kernels are mid-long with semi-wrinkled hulls and blue aleurone.', {'entities': [(0, 7, 'PLAN'), (40, 45, 'PLAN'), (55, 63, 'PLAN')]}),
    ('The collars are closed.', {'entities': [(4, 11, 'PLAN')]}),
    ('The leaves and spikes have a slight waxy coating.', {'entities': [(4, 10, 'PLAN'), (15, 21, 'PLAN')]}),
    ('Westbred Barcott is a six-rowed spring feed barley.', {'entities': [(0, 16, 'CVAR'), (22, 31, 'TRAT'), (32, 38, 'TRAT'), (39, 43, 'TRAT'), (44, 50, 'TRAT')]}),
    ('At the time of evaluation it was moderately resistant to BYD, moderately susceptible to scald and net blotch, and susceptible to leaf rust, stripe rust and powdery mildew.', {'entities': [(33, 53, 'PPTD'), (57, 60, 'PATH'), (62, 84, 'PPTD'), (88, 93, 'PATH'), (98, 108, 'PATH'), (114, 125, 'PPTD'), (129, 138, 'PATH'), (140, 151, 'PATH'), (156, 170, 'PATH')]}),
    ('Westbred Sprinter is a six-rowed facultative feed barley.', {'entities': [(0, 17, 'CVAR'), (23, 32, 'TRAT'), (33, 44, 'TRAT'), (45, 49, 'TRAT'), (50, 56, 'TRAT')]}),
    ('It was released by Western Plant Breeders in 1986.', {'entities': [(19, 41, 'ORG'), (45, 49, 'DATE')]}),
    ('It has late season maturity (7 days later than Westbred 501 and 3-5 days later than Schuyler), semi-dwarf height (medium short) with stiff straw, and excellent lodging resistance.', {'entities': [(19, 27, 'TRAT'), (47, 59, 'CVAR'), (84, 92, 'CVAR'), (95, 105, 'TRAT'), (121, 126, 'TRAT'), (139, 144, 'PLAN'), (160, 178, 'TRAT')]}),
    ('It is awned and has white aleurone.', {'entities': [(6, 11, 'PLAN'), (26, 34, 'PLAN')]}),
    ('At the time of evaluation it was moderately resistant to scald, net blotch, stripe rust, powdery mildew, and bacterial leaf blight, and susceptible to leaf rust, stem rust and BYD.', {'entities': [(33, 53, 'PPTD'), (57, 62, 'PATH'), (64, 74, 'PATH'), (76, 87, 'PATH'), (89, 103, 'PATH'), (109, 130, 'PATH'), (136, 147, 'PPTD'), (151, 160, 'PATH'), (162, 171, 'PATH'), (176, 179, 'PATH')]}),
    ('It was released by Western Plant Breeders.', {'entities': [(19, 41, 'ORG')]}),
    ('Westford is a six-rowed spring forage (hooded) barley.', {'entities': [(0, 8, 'CVAR'), (14, 23, 'TRAT'), (24, 30, 'TRAT'), (31, 37, 'TRAT'), (39, 45, 'TRAT'), (47, 53, 'TRAT')]}),
    ('It was released by Western Plant Breeders.', {'entities': [(19, 41, 'ORG')]}),
    ('Its experimental designation was BFC 79-18.', {'entities': [(33, 42, 'ALAS')]}),
    ('It is late maturing and tall with good straw strength.', {'entities': [(11, 19, 'TRAT'), (24, 28, 'TRAT'), (39, 53, 'TRAT')]}),
    ('At the time of evaluation it was resistant to scald, net blotch, and powdery mildew, and susceptible to BYD and stripe rust.', {'entities': [(33, 42, 'PPTD'), (46, 51, 'PATH'), (53, 63, 'PATH'), (69, 83, 'PATH'), (89, 100, 'PPTD'), (104, 107, 'PATH'), (112, 123, 'PATH')]}),
    ('Winter Tennessee is a six-rowed spring feed barley.', {'entities': [(0, 16, 'CVAR'), (22, 31, 'TRAT'), (32, 38, 'TRAT'), (39, 43, 'TRAT'), (44, 50, 'TRAT')]}),
    ('It was released by the California AES in 1916.', {'entities': [(23, 37, 'ORG'), (41, 45, 'DATE')]}),
    ('It has erect early season growth, and mid-season to late maturity.', {'entities': [(26, 32, 'TRAT'), (57, 65, 'TRAT')]}),
    ('It is mid-tall with moderately weak straw.', {'entities': [(6, 14, 'TRAT'), (36, 41, 'PLAN')]}),
    ('Basal rachis internodes are straight.', {'entities': [(0, 23, 'PLAN')]}),
    ('Spikes are lax, short to mid-long, parallel, slightly waxy and slightly nodding.', {'entities': [(0, 6, 'PLAN')]}),
    ('Lemma awns are long and rough.', {'entities': [(0, 10, 'PLAN')]}),
    ('Glume awns are rough and equal in length to glumes.', {'entities': [(0, 10, 'PLAN'), (44, 50, 'PLAN')]}),
    ('Glumes are half the length of lemmas and covered with short hairs.', {'entities': [(0, 6, 'PLAN'), (30, 36, 'PLAN'), (60, 65, 'PLAN')]}),
    ('The rachilla is short-haired.', {'entities': [(4, 12, 'PLAN')]}),
    ('Hulls are slightly wrinkled to semi-wrinkled.', {'entities': [(0, 5, 'PLAN')]}),
    ('Aleurone is blue.', {'entities': [(0, 8, 'PLAN')]}),
    ('Veins on kernels are moderately prominent and', {'entities': [(0, 5, 'PLAN'), (9, 16, 'PLAN')]})
]
