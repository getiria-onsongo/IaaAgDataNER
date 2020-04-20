TRAIN_DATA = [
    ('ROBUST  Robust is a six-rowed spring malting barley.', {'entities': [(8, 14, 'CVAR'), (20, 29, 'TRAT'), (30, 36, 'TRAT'), (37, 44, 'TRAT'), (45, 51, 'CROP')]}),
    ('The central vein is moderately prominent, lateral veins are less prominent and disappearing near the center of the kernel.', {'entities': [(4, 16, 'PLAN'), (42, 55, 'PLAN'), (115, 121, 'PLAN')]}),
    ('There are no barbs on the lateral veins.', {'entities': [(13, 18, 'PLAN'), (26, 39, 'PLAN')]}),
    ('The crease is V-shaped and narrow at the base.', {'entities': [(4, 10, 'PLAN'), (41, 45, 'PLAN')]}),
    ('Lateral kernels are moderately twisted, plump, wide at the center, and full on the crease side.', {'entities': [(0, 15, 'PLAN'), (83, 89, 'PLAN')]}),
    ('It is superior to Morex in grain yield, kernel plumpness and lodging resistance.', {'entities': [(18, 23, 'CVAR'), (27, 38, 'TRAT'), (40, 56, 'TRAT'), (61, 79, 'TRAT')]}),
    ('At the time of release it was highly resistant to stem rust and spot blotch and susceptible to loose smut.', {'entities': [(30, 46, 'PPTD'), (50, 59, 'PATH'), (64, 75, 'PATH'), (80, 91, 'PPTD'), (95, 105, 'PATH')]}),
    ('Rollo is a six-rowed spring feed barley.', {'entities': [(0, 5, 'CVAR'), (11, 20, 'TRAT'), (21, 27, 'TRAT'), (28, 32, 'TRAT'), (33, 39, 'CROP')]}),
    ('It was released by the Utah AES in 1991.', {'entities': [(23, 31, 'ORG'), (35, 39, 'DATE')]}),
    ('It was released by the Minnesota AES in 1983.', {'entities': [(23, 36, 'ORG'), (40, 44, 'DATE')]}),
    ('Its experimental designation was UT 1075.', {'entities': [(33, 40, 'ALAS')]}),
    ('It has midseason maturity and is similar to Steptoe in plant height, and lodging (susceptible).', {'entities': [(17, 25, 'TRAT'), (44, 51, 'CVAR'), (55, 67, 'TRAT'), (73, 80, 'TRAT')]}),
    ('Compared to Steptoe, its heads 3 days later, is equal in test weight and 1 cm shorter, but has stronger straw (30 vs. 51% lodging for Steptoe).', {'entities': [(12, 19, 'CVAR'), (25, 30, 'TRAT'), (57, 68, 'TRAT'), (78, 85, 'TRAT'), (104, 109, 'PLAN'), (122, 129, 'TRAT'), (134, 141, 'CVAR')]}),
    ('Spikes are erect with little or no overlap of the lateral kernels, and sparse hairs on the rachis edges.', {'entities': [(0, 6, 'PLAN'), (50, 65, 'PLAN'), (78, 83, 'PLAN'), (91, 103, 'PLAN')]}),
    ('Glumes are long, with hairs restricted to the middle, and have medium-to-long, semi-smooth glume awns.', {'entities': [(0, 6, 'PLAN'), (22, 27, 'PLAN'), (91, 101, 'PLAN')]}),
    ('Lemma awns are long and semi-smooth and have distinctly purple tips prior to maturity.', {'entities': [(0, 10, 'PLAN')]}),
    ('The seed is covered, mid-long, slightly wrinkled, with long rachilla hairs and a transverse crease at the base.', {'entities': [(4, 8, 'PLAN'), (60, 74, 'PLAN'), (81, 98, 'PLAN'), (106, 110, 'PLAN')]}),
    ('Aleurone color is white.', {'entities': [(0, 8, 'PLAN')]}),
    ('At the time of release it had field resistance to barley loose smut and covered smut and moderate resistance to powdery mildew.', {'entities': [(30, 46, 'PPTD'), (50, 67, 'PATH'), (72, 84, 'PATH'), (89, 108, 'PPTD'), (112, 126, 'PATH')]}),
    ('It was selected from the cross Morex/Manker.', {'entities': [(31, 43, 'PED')]}),
    ('It subsequently became susceptible to stripe rust.', {'entities': [(23, 34, 'PPTD'), (38, 49, 'PATH')]}),
    ('Russell is a six-rowed spring feed and malting barley.', {'entities': [(0, 7, 'CVAR'), (13, 22, 'TRAT'), (23, 29, 'TRAT'), (30, 34, 'TRAT'), (39, 46, 'TRAT'), (47, 53, 'CROP')]}),
    ('It was released by the USDA-ARS and the Idaho and Oregon AESs in 1985.', {'entities': [(23, 31, 'ORG'), (40, 61, 'ORG'), (65, 69, 'DATE')]}),
    ('It was selected from the cross Karla/ND1265.', {'entities': [(31, 43, 'PED')]}),
    ('Its experimental designation was 78Ab9009-5RC.', {'entities': [(33, 45, 'ALAS')]}),
    ('Plants are "Karla-type" with improved kernel plumpness, slightly shorter straw, and earlier heading.', {'entities': [(38, 54, 'TRAT'), (73, 78, 'PLAN'), (92, 99, 'TRAT')]}),
    ('It is susceptible to lodging, but lodges less than Steptoe.', {'entities': [(21, 28, 'TRAT'), (51, 58, 'CVAR')]}),
    ('Its experimental designation was M36.', {'entities': [(33, 36, 'ALAS')]}),
    ('It is superior in test weight and similar in height (mid-tall) and heading date to Steptoe (heads about 1 day earlier than Steptoe at Tulelake).', {'entities': [(18, 29, 'TRAT'), (45, 51, 'TRAT'), (53, 61, 'TRAT'), (67, 79, 'TRAT'), (83, 90, 'CVAR'), (92, 97, 'TRAT'), (123, 130, 'CVAR'), (134, 142, 'CVAR')]}),
    ('Spikes are relatively lax and mid-long.', {'entities': [(0, 6, 'PLAN')]}),
    ('Awns are smooth.', {'entities': [(0, 4, 'PLAN')]}),
    ('Glumes are covered with short hairs.', {'entities': [(0, 6, 'PLAN'), (30, 35, 'PLAN')]}),
    ('The hull is adhering and wrinkled.', {'entities': [(4, 8, 'PLAN')]}),
    ('The aleurone is colorless.', {'entities': [(4, 12, 'PLAN')]}),
    ('Rachilla hairs are short.', {'entities': [(0, 14, 'PLAN')]}),
    ('Veins are moderately prominent and there are numerous barbs on lateral veins.', {'entities': [(0, 5, 'PLAN'), (54, 59, 'PLAN'), (63, 76, 'PLAN')]}),
    ('The crease is narrow to closed at the base and flared toward the awn end.', {'entities': [(4, 10, 'PLAN'), (38, 42, 'PLAN'), (65, 68, 'PLAN')]}),
    ('Lateral kernels are relatively plump and slightly twisted.', {'entities': [(0, 15, 'PLAN')]}),
    ('At the time of evaluation it was susceptible to stripe rust, kernel blight (caused by Alternaria spp) and powdery mildew, and moderately susceptible to scald.', {'entities': [(33, 44, 'PPTD'), (48, 59, 'PATH'), (61, 74, 'PATH'), (86, 100, 'PATH'), (106, 120, 'PATH'), (126, 148, 'PPTD'), (152, 157, 'PATH')]}),
    ('Samish 23 is a two-rowed spring feed and malting barley.', {'entities': [(0, 9, 'CVAR'), (15, 24, 'TRAT'), (25, 31, 'TRAT'), (32, 36, 'TRAT'), (41, 48, 'TRAT'), (49, 55, 'CROP')]}),
    ('It was developed by Fossum Cereals in Washington.', {'entities': [(20, 34, 'ORG'), (38, 48, 'GPE')]}),
    ('It was selected from the cross 85Ab2323/Acclaim.', {'entities': [(31, 47, 'PED')]}),
    ('It is late maturing and short-statured with good straw strength.', {'entities': [(11, 19, 'TRAT'), (24, 38, 'TRAT'), (49, 63, 'TRAT')]}),
    ('At the time of evaluation it was resistant to stripe rust.', {'entities': [(33, 42, 'PPTD'), (46, 57, 'PATH')]}),
    ('It is smooth-awned with medium early maturity (matures 2-3 days earlier than Morex).', {'entities': [(6, 18, 'TRAT'), (37, 45, 'TRAT'), (77, 82, 'CVAR')]}),
    ('Sara is a six-rowed spring hooded feed barley.', {'entities': [(0, 4, 'CVAR'), (10, 19, 'TRAT'), (20, 26, 'TRAT'), (27, 33, 'TRAT'), (34, 38, 'TRAT'), (39, 45, 'CROP')]}),
    ('It was developed by the Oregon AES and exclusively released to Winema Elevators Inc. of Tulelake, CA in 2001.', {'entities': [(24, 34, 'ORG'), (63, 83, 'ORG'), (88, 100, 'GPE'), (104, 108, 'DATE')]}),
    ('It was selected from the cross Marco/Fragil//Cali92/3/Gloria-Bar/Come-b//Esperanza.', {'entities': [(31, 82, 'PED')]}),
    ('Sara is a stripe rust resistant hooded spring barley developed by Hugo Vivar (retired; CARDA/CIMMYT).', {'entities': [(0, 4, 'CVAR'), (10, 21, 'PATH'), (22, 31, 'PPTD'), (32, 38, 'TRAT'), (39, 45, 'TRAT'), (46, 52, 'CROP')]}),
    ('Plants are mid-tall with moderately strong straw.', {'entities': [(11, 19, 'TRAT'), (43, 48, 'PLAN')]}),
    ('Spikes are medium-lax, medium-long and semi-erect.', {'entities': [(0, 6, 'PLAN')]}),
    ('Kernels are covered, medium-large with short haired rachilla and white aleurone.', {'entities': [(0, 7, 'PLAN'), (52, 60, 'PLAN'), (71, 79, 'PLAN')]}),
    ('Crop Science 23:1216 (1983)', {'entities': [(0, 27, 'JRNL')]}),
    ('It was selected from the cross Bracken/UT75B65-532 (ID633019/Woodvale).', {'entities': [(31, 70, 'PED')]}),
    ('Crop Science 33:1412-1413 (1993)', {'entities': [(0, 32, 'JRNL')]}),
    ('Crop Science 28:574 (1988)', {'entities': [(0, 26, 'JRNL')]})
]
