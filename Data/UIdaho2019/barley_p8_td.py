TRAIN_DATA = [
    ('In 2019, Thunder yields were comparable to KWS Scala, Sunstar Pride and better than Wintmalt, but with a tendency to lodge.', {'entities': [(3, 7, 'DATE'), (9, 16, 'CVAR'), (17, 23, 'TRAT'), (43, 52, 'CVAR'), (54, 67, 'CVAR'), (84, 92, 'CVAR'), (117, 122, 'TRAT')]}),
    ('Upspring (05ARS748-270)  Upspring is a hulless, high beta-glucan (7% BG)', {'entities': [(0, 8, 'CVAR'), (10, 22, 'ALAS'), (25, 33, 'CVAR'), (39, 46, 'TRAT'), (53, 64, 'TRAT')]}),
    ('Wintmalt test weight was below average,', {'entities': [(0, 8, 'CVAR'), (9, 20, 'TRAT')]}),
    ('heading was 1 day later than average, but plumps were excellent.', {'entities': [(0, 7, 'TRAT'), (42, 48, 'TRAT')]}),
    ('Soft White Alturas (IDO526)  a low-protein soft white spring wheat released by Idaho AES and USDA-ARS in 2002.', {'entities': [(0, 4, 'TRAT'), (5, 10, 'TRAT'), (11, 18, 'CVAR'), (20, 26, 'ALAS'), (31, 42, 'TRAT'), (43, 47, 'TRAT'), (48, 53, 'TRAT'), (54, 60, 'TRAT'), (61, 66, 'CROP'), (79, 88, 'ORG'), (93, 101, 'ORG'), (105, 109, 'DATE')]}),
    ('Alturas has a partial waxy endosperm which may make it vulnerable to low falling numbers.', {'entities': [(0, 7, 'CVAR'), (27, 36, 'PLAN'), (73, 88, 'TRAT')]}),
    ('Alturas is adapted to both irrigated and dryland conditions, is average in yield (above average under irrigation Table 41), with average test weight, heading date and height.', {'entities': [(0, 7, 'CVAR'), (75, 80, 'TRAT'), (137, 148, 'TRAT'), (150, 162, 'TRAT'), (167, 173, 'TRAT')]}),
    ('Alturas is susceptible to the current races of stripe rust and is moderately susceptible to Fusarium head blight (FHB).', {'entities': [(0, 7, 'CVAR'), (11, 22, 'PPTD'), (47, 58, 'PATH'), (66, 88, 'PATH'), (92, 112, 'PATH'), (114, 117, 'PATH')]}),
    ('AP Coachman (08PN2001-07) -  dryland soft white spring from AgriPro / Syngenta Cereals with a release targeted for 2020.', {'entities': [(0, 11, 'CVAR'), (13, 24, 'ALAS'), (29, 36, 'TRAT'), (37, 41, 'TRAT'), (42, 47, 'TRAT'), (48, 54, 'TRAT'), (60, 67, 'ORG'), (70, 86, 'ORG'), (115, 119, 'DATE')]}),
    ('AP Coachman was tested in 2019 in one dryland location (Soda Springs, Table 47) and yielded very well (90 bu/A) competing with Tekoa and Seahawk.', {'entities': [(0, 11, 'CVAR'), (26, 30, 'DATE'), (56, 68, 'ORG'), (84, 91, 'TRAT'), (127, 132, 'CVAR'), (137, 144, 'CVAR')]}),
    ('It was three inches taller than average, with average protein', {'entities': [(20, 26, 'TRAT'), (54, 61, 'TRAT')]}),
    ('winter barley variety and the latest food barley released from USDA-ARS breeding program in conjunction with the University of Idaho AES.', {'entities': [(0, 6, 'TRAT'), (7, 13, 'CROP'), (37, 41, 'TRAT'), (42, 48, 'CROP'), (63, 88, 'ORG'), (113, 136, 'ORG')]}),
    ('but it had low test weight.', {'entities': [(15, 26, 'TRAT')]}),
    ('AP Coachman has resistance to current races of stripe rust, Hessian fly, and good (MR) resistance to Fusarium head blight.', {'entities': [(0, 11, 'CVAR'), (16, 26, 'PPTD'), (47, 58, 'PATH'), (60, 71, 'PATH'), (87, 97, 'PPTD'), (101, 121, 'PATH')]}),
    ('Louise (WA7921)  soft white spring wheat released in 2004 from Washington State   and used as a long-term check for soft white spring wheat.', {'entities': [(0, 6, 'CVAR'), (8, 14, 'ALAS'), (17, 21, 'TRAT'), (22, 27, 'TRAT'), (28, 34, 'TRAT'), (35, 40, 'CROP'), (53, 57, 'DATE'), (63, 79, 'ORG'), (116, 120, 'TRAT'), (121, 126, 'TRAT'), (127, 133, 'TRAT'), (134, 139, 'CROP')]}),
    ('Louise is a later maturity, tall wheat with below average yields and high lodging potential under irrigated conditions.', {'entities': [(0, 6, 'CVAR'), (18, 26, 'TRAT'), (28, 32, 'TRAT'), (33, 38, 'CROP'), (58, 64, 'TRAT'), (74, 91, 'TRAT')]}),
    ('Louise performed well under dryland conditions, being the highest yielding soft white spring variety in Soda Springs area (Table 41).', {'entities': [(0, 6, 'CVAR'), (66, 74, 'TRAT'), (75, 79, 'TRAT'), (80, 85, 'TRAT'), (86, 92, 'TRAT'), (104, 116, 'GPE')]}),
    ('Louise is susceptible to stripe rust and FHB.', {'entities': [(0, 6, 'CVAR'), (10, 21, 'PPTD'), (25, 36, 'PATH'), (41, 44, 'PATH')]}),
    ('Melba (WA8193)', {'entities': [(0, 5, 'CVAR'), (7, 13, 'ALAS')]}),
    ('Melba is aclub wheat developed by USDA-ARS in Pullman and released in conjunction with the Washington AES in 2016.', {'entities': [(0, 5, 'CVAR'), (15, 20, 'CROP'), (34, 42, 'ORG'), (46, 53, 'GPE'), (91, 105, 'ORG'), (109, 113, 'DATE')]}),
    ('Melba is one of the first club wheats with good yield performance in southeast Idaho, similar to Seahawk and UI Stone (Table 40 and Chart 7).', {'entities': [(0, 5, 'CVAR'), (26, 30, 'TRAT'), (31, 37, 'CROP'), (48, 65, 'TRAT'), (79, 84, 'GPE'), (97, 104, 'CVAR'), (109, 117, 'CVAR')]}),
    ('Melba is average in height, five days later in heading than the soft white spring lines usually grown in the area, with low protein.', {'entities': [(0, 5, 'CVAR'), (20, 26, 'TRAT'), (47, 54, 'TRAT'), (64, 68, 'TRAT'), (69, 74, 'TRAT'), (75, 81, 'TRAT'), (124, 131, 'TRAT')]}),
    ('Melba is resistant to stripe rust and had a similar Seahawk.', {'entities': [(0, 5, 'CVAR'), (9, 18, 'PPTD'), (22, 33, 'PATH'), (52, 59, 'CVAR')]}),
    ('Ryan (WA8214)', {'entities': [(0, 4, 'CVAR'), (6, 12, 'ALAS')]}),
    ('Ryan is a partial waxy soft white spring wheat released from Washington State University, AES and USDA in 2016.', {'entities': [(0, 4, 'CVAR'), (18, 22, 'TRAT'), (23, 27, 'TRAT'), (28, 33, 'TRAT'), (34, 40, 'TRAT'), (41, 46, 'CROP'), (61, 93, 'ORG'), (98, 102, 'ORG'), (106, 110, 'DATE')]}),
    ('In the first year of testing (2018), Ryan averaged higher in yield than', {'entities': [(30, 34, 'DATE'), (37, 41, 'CVAR'), (61, 66, 'TRAT')]}),
    ('While agronomically similar to Buck, Upspring had slightly higher yields, headed three to six days later, had greater percentages of plump seed and had 2% higher grain protein (Table 26).', {'entities': [(31, 35, 'CVAR'), (37, 45, 'CVAR'), (66, 72, 'TRAT'), (74, 80, 'TRAT'), (118, 143, 'TRAT'), (162, 175, 'TRAT')]}),
    ('Seed germination may be low under dryland conditions.', {'entities': [(0, 16, 'TRAT')]}),
    ('Wintmalt  a shorter, two-rowed winter malt developed by KWS Lochow (Germany) and imported from Europe.', {'entities': [(0, 8, 'CVAR'), (21, 30, 'TRAT'), (31, 37, 'TRAT'), (38, 42, 'TRAT'), (56, 66, 'CVAR'), (68, 75, 'ORG'), (95, 101, 'ORG')]}),
    ('Wintmalt has good foliar disease resistance, is being produced in the PNW and is an AMBA approved malt variety.', {'entities': [(0, 8, 'CVAR'), (18, 32, 'PATH'), (33, 43, 'PPTD'), (70, 73, 'GPE'), (84, 88, 'ORG'), (98, 102, 'TRAT')]}),
    ('In the third-year summary (Table 26), Wintmalt lodging, protein and yields were at trial average.', {'entities': [(38, 46, 'CVAR'), (47, 54, 'TRAT'), (56, 63, 'TRAT'), (68, 74, 'TRAT')]})
]
