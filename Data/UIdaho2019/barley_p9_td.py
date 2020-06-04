TRAIN_DATA = [
    (' other soft white spring wheat varieties over four irrigated locations, but in 2019 (Table 42) irrigated yields were below average and similar to Louise.', {'entities': [(7, 11, 'TRAT'), (12, 17, 'TRAT'), (18, 24, 'TRAT'), (25, 30, 'CROP'), (79, 83, 'DATE'), (95, 111, 'TRAT'), (146, 152, 'CVAR')]}),
    ('Under dryland conditions, yield was similar to SY Saltese and WB6430', {'entities': [(26, 31, 'TRAT'), (47, 57, 'CVAR'), (62, 68, 'CVAR')]}),
    ('Plant height is a little above average and heading date 2-4 days later than average.', {'entities': [(0, 12, 'TRAT'), (43, 55, 'TRAT')]}),
    ('Seahawk may have a tendency to lodge under high production practices.', {'entities': [(0, 7, 'CVAR'), (31, 36, 'TRAT')]}),
    ('SY Saltese (SY3024-2)  a soft white spring wheat released in 2016 by Syngenta Cereals.', {'entities': [(0, 10, 'CVAR'), (12, 20, 'ALAS'), (25, 29, 'TRAT'), (30, 35, 'TRAT'), (36, 42, 'TRAT'), (43, 48, 'CROP'), (61, 65, 'DATE'), (69, 85, 'ORG')]}),
    ('SY Saltese has yield potential similar to Seahawk and UI Stone.', {'entities': [(0, 10, 'CVAR'), (15, 30, 'TRAT'), (42, 49, 'CVAR'), (54, 62, 'CVAR')]}),
    ('Averaged over three years and four irrigated locations, SY Saltese yielded 120 bu/A (see Table 40).', {'entities': [(56, 66, 'CVAR'), (67, 74, 'TRAT')]}),
    ('In 2019, SY Saltese yields were 7 bu below WB6121, and 3 bu/A greater than UI Stone (Table 42).', {'entities': [(3, 7, 'DATE'), (9, 19, 'CVAR'), (20, 26, 'TRAT'), (75, 83, 'CVAR')]}),
    ('SY Saltese also has good test weight and resistance to stripe rust (SR), but may be susceptible to currently developing SR races.', {'entities': [(0, 10, 'CVAR'), (25, 36, 'TRAT'), (41, 51, 'PPTD'), (55, 66, 'PATH'), (68, 70, 'PATH'), (84, 95, 'PPTD'), (99, 128, 'PATH')]}),
    ('SY Saltese may lodge under higher production situations and is susceptible to FHB.', {'entities': [(0, 10, 'CVAR'), (15, 20, 'TRAT'), (63, 74, 'PPTD'), (78, 81, 'PATH')]}),
    ('SY Saltese is also susceptible to Hessian fly.', {'entities': [(0, 10, 'CVAR'), (19, 30, 'PPTD'), (34, 45, 'PATH')]}),
    ('Tekoa (WA8189)  a Washington State University 2016 release, Tekoa is a soft white spring wheat released for higher rainfall areas and will do well under irrigated conditions (Table 40).', {'entities': [(0, 5, 'CVAR'), (7, 13, 'ALAS'), (18, 45, 'ORG'), (46, 50, 'DATE'), (60, 65, 'CVAR'), (71, 75, 'TRAT'), (76, 81, 'TRAT'), (82, 88, 'TRAT'), (89, 94, 'CROP')]}),
    ('Tekoa did not yield as well in areas where irrigation was restricted at the end of the growing season.', {'entities': [(0, 5, 'CVAR'), (14, 19, 'TRAT')]}),
    ('In 2018 and 2019, Tekoa yields were at trial average.', {'entities': [(3, 7, 'DATE'), (12, 16, 'DATE'), (18, 23, 'CVAR'), (24, 30, 'TRAT')]}),
    ('Tekoa is adapted to low pH soils where aluminum toxicity can occur.', {'entities': [(0, 5, 'CVAR'), (9, 32, 'TRAT')]}),
    ('Tekoa has good test weight, is a little later in maturity (heading date) than average and average for plant height.', {'entities': [(0, 5, 'CVAR'), (15, 26, 'TRAT'), (49, 57, 'TRAT'), (59, 71, 'TRAT'), (102, 114, 'TRAT')]}),
    ('Tekoa is resistant to stripe rust, Hessian fly, and moderately resistant to FHB, similar to Seahawk.', {'entities': [(0, 5, 'CVAR'), (9, 18, 'PPTD'), (22, 33, 'PATH'), (35, 46, 'PATH'), (52, 72, 'PPTD'), (76, 79, 'PATH'), (92, 99, 'CVAR')]}),
    ('UI Cookie (IDO1405S)  a soft white spring wheat released in 2019 by the University of Idaho Ag Experiment Station.', {'entities': [(0, 9, 'CVAR'), (11, 19, 'ALAS'), (24, 28, 'TRAT'), (29, 34, 'TRAT'), (35, 41, 'TRAT'), (42, 47, 'CROP'), (60, 64, 'DATE'), (72, 113, 'ORG')]}),
    ('Three-year irrigated averages (Table 47) show UI Cookie above trial average for yield, lower for test weight and higher for grain protein.', {'entities': [(46, 55, 'CVAR'), (80, 85, 'TRAT'), (97, 108, 'TRAT'), (124, 137, 'TRAT')]}),
    ('UI Cookie has good end-use quality, similar or better resistance to FHB than UI Stone, better resistance to stripe rust and improved threshability.', {'entities': [(0, 9, 'CVAR'), (19, 34, 'TRAT'), (54, 64, 'PPTD'), (68, 71, 'PATH'), (77, 85, 'CVAR'), (94, 104, 'PPTD'), (108, 119, 'PATH'), (133, 146, 'TRAT')]}),
    ('UI Pettit (IDO632)  is a soft white spring wheat released in 2006 through the Idaho AES.', {'entities': [(0, 9, 'CVAR'), (11, 17, 'ALAS'), (25, 29, 'TRAT'), (30, 35, 'TRAT'), (36, 42, 'TRAT'), (43, 48, 'CROP'), (61, 65, 'DATE'), (78, 87, 'ORG')]}),
    ('Yields and test weight are lower than average.', {'entities': [(0, 6, 'TRAT'), (11, 22, 'TRAT')]}),
    ('Ryan has Hessian fly resistance, tolerance to low acid / high aluminum soils, and HTAP (high temperature adult plant) resistance to stripe rust.', {'entities': [(0, 4, 'CVAR'), (9, 20, 'PATH'), (21, 31, 'PPTD'), (118, 128, 'PPTD'), (132, 143, 'PATH')]}),
    ('UI Pettit is short and heads 3-5 days earlier than Alturas.', {'entities': [(0, 9, 'CVAR'), (13, 18, 'TRAT'), (23, 28, 'TRAT'), (51, 58, 'CVAR')]}),
    ('UI Pettit is very susceptible to current races of stripe rust and to FHB.', {'entities': [(0, 9, 'CVAR'), (13, 29, 'PPTD'), (33, 61, 'PATH'), (69, 72, 'PATH')]}),
    ('UI Stone (IDO599) - a soft white spring wheat released by Idaho AES in 2012', {'entities': [(0, 8, 'CVAR'), (10, 16, 'ALAS'), (22, 26, 'TRAT'), (27, 32, 'TRAT'), (33, 39, 'TRAT'), (40, 45, 'CROP'), (58, 67, 'ORG'), (71, 75, 'DATE')]}),
    (', UI Stone has high yield potential, consistently greater than UI Pettit and similar to Alturas (Table 40).', {'entities': [(2, 10, 'CVAR'), (20, 35, 'TRAT'), (63, 72, 'CVAR'), (88, 95, 'CVAR')]}),
    ('UI Stone was selected for good end-use quality and reduced FHB susceptibility (carries the Fhb1 resistance gene).', {'entities': [(0, 8, 'CVAR'), (31, 46, 'TRAT'), (59, 62, 'PATH'), (63, 77, 'PPTD')]}),
    ('In 2019, UI Stone yielded similar to Seahawk and about 10 bu/A below WB6121 (Table 42).', {'entities': [(3, 7, 'DATE'), (9, 17, 'CVAR'), (18, 25, 'TRAT'), (37, 44, 'CVAR')]}),
    ('Ryan was early to heading, similar to UI Pettit, was shorter than average, had good test weight and resistance to lodging.', {'entities': [(0, 4, 'CVAR'), (18, 25, 'TRAT'), (38, 47, 'CVAR'), (53, 60, 'TRAT'), (84, 95, 'TRAT'), (100, 121, 'TRAT')]}),
    ('Seahawk (WA8162)  a soft white spring wheat released from Washington State  ram in 2014 adapted to dryland and irrigated production areas.', {'entities': [(0, 7, 'CVAR'), (9, 15, 'ALAS'), (20, 24, 'TRAT'), (25, 30, 'TRAT'), (31, 37, 'TRAT'), (38, 43, 'CROP'), (58, 74, 'ORG'), (83, 87, 'DATE')]}),
    ('Seahawk has resistance to Hessian fly, is very resistant to stripe rust, and one of the least susceptible soft white spring wheats to FHB.', {'entities': [(0, 7, 'CVAR'), (12, 22, 'PPTD'), (26, 37, 'PATH'), (42, 56, 'PPTD'), (60, 71, 'PATH'), (88, 105, 'PPTD'), (106, 110, 'TRAT'), (111, 116, 'TRAT'), (117, 123, 'TRAT'), (124, 130, 'CROP'), (134, 137, 'PATH')]}),
    ('Yield and test weight has been one the highest of all currently available soft white springs, with similar to UI Stone and WB6430', {'entities': [(0, 5, 'TRAT'), (10, 21, 'TRAT'), (74, 78, 'TRAT'), (79, 84, 'TRAT'), (85, 92, 'TRAT'), (110, 118, 'CVAR'), (123, 129, 'CVAR')]})
]