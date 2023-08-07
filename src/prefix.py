context_length = 4000 # Value set by openAI. At the moment you cannot change this value

variety_name_key = "variety name"

missing_symbol = "?"

beforeInstruction = """Below are instances showing how to extract information from a given [Text]. The symbol ? is used to represent missing information. \n"""

exampleDelimiter = """\n###\n\n"""

afterInstruction =  """Using the above instances as examples of how to extract information, and ? to represent missing values, extract: Variety Name,  Variety Aliases, Crop Name, Germplasm Characteristics, Crop Variety Class, Journal References, Pathogens, Pedigrees, Traits, Plant Predisposition to Diseases, Revision Date, Trial Date, Release Date and Trial Evaluation Location  from the following [Text]: \n"""

sample_output = """[Text]: Mokua is a six-rowed winter feed barley. It was released by the Arizona AES in 2006. It is a doubled-haploid line produced from the cross I1162-19/J-126//WA1245///Steptoe. Its experimental designation was ORW-6. It is medium height (averages about 41 inches, slightly taller than Kold) and medium early maturing with fair straw strength. It has rough awns and a semi-compact spike. At the time of evaluation it was resistant to stripe rust and moderately susceptible to scald, net blotch, and BYD. It was evaluated as Entry 964 in the UC Regional Cereal Testing program from 1997-2006 for fall planting in the intermountain region of northern California and in 2008 for fall planting in the Central Valley of California. Arizona AES (2006)
Variety Name: Mokua
Variety Aliases: ORW-6, Entry 964 
Crop Name: Barley 
Germplasm Characteristics: Doubled-haploid line 
Crop Variety Class: Six-rowed winter feed barley 
Journal References: ?
Pathogens: Stripe rust, scald, net blotch, BYD
Pedigrees: I1162-19/J-126//WA1245///Steptoe 
Traits: Medium height # medium early maturing # fair straw strength # rough awns # semi-compact spike. 
Plant Predisposition to Diseases: Resistant to stripe rust # moderately susceptible to scald # moderately susceptible to net blotch #moderately susceptible to BYD. 

Revision Date: September 2011
Trial Date: 1997-2006 
Release Date: 2006
Trial Evaluation Location: Arizona # Central Valley of California
"""


exampleOne = """[Text]: Ishi is a six-rowed spring feed barley. Its occurrence and resistance stability were studied along with a susceptible control over four years (2005-08). Its experimental designations were UC 1047 and UCD PYT99 A-13. Ishi has the sdw1 gene and is short statured, averaging 84.6 cm, and is similar to UC 937 and 3.6 cm taller than UC 933, averaged over 32 location-years in Central Valley and Central Coast environments. For lodging resistance (fair) it was superior to UC 937 but similar to UC 933 over 20 environments where lodging occurred. For days to heading it averaged 4 days earlier than UC 937 and 3 days later than UC 933, but all three cultivars were similar for time to maturity (medium late). It is heterogeneous for rough and smooth awns, having less than one-percent smooth awned plants. The spike is waxy and semi-erect. The kernels are covered and the aleurone is non-blue. Grains are long (>10mm) and wrinkled, with hairs on the ventral furrow. Rachilla hairs are long. At the time of release Ishi was resistant to scald and powdery mildew, moderately resistant to stripe rust, BYD and net blotch, and moderately susceptible to leaf rust. It subsequently became moderately susceptible to net blotch. It was evaluated as Entry 1047 in the UC Regional Cereal Testing program from 2000 present for late fall planting in the Central Valley and the south-central coastal region of California and for spring planting in the intermountain area of northern California. Crop Science 46:1396 (2006) 
Variety Name: Ishi 
Variety Aliases: UC 1047 # UCD PYT99 A-13 # Entry 1047 
Crop Name: Barley 
Germplasm Characteristics: sdw1 gene 
Crop Variety Class: Six-rowed spring feed barley 
Journal References: Crop Science 46:1396 (2006) 
Pathogens: Scald # powdery mildew # stripe rust # BYD # net blotch # leaf rust 
Pedigrees: ?
Traits: Short statured # fair lodging resistance # medium late time to maturity # heterogeneous for rough and smooth awns # waxy and semi-erect spike # covered kernels # non-blue aleurone # long (>10mm) and wrinkled grains # hairs on the ventral furrow # long rachilla hairs. 
Plant Predisposition to Diseases: Resistant to scald and powdery mildew # moderately resistant to stripe rust, BYD and net blotch # moderately susceptible to leaf rust # moderately susceptible to net blotch.
Revision Date: ?
Trial Date: 2005-08
Release Date: ?
Trial Evaluation Location: Central Valley and Central Coast environments.
"""

exampleTwo = """[Text]: Rohan is a six-rowed winter feed barley. It was released by the USDA-ARS and the Idaho AES in 1991 (Revised September 2011). It was  selected from the cross Steveland/Luther//Wintermalt. Its experimental designation was 79Ab812. It has rough awns,  good winter hardiness, and is medium height with intermediate lodging resistance. Spikes are short and dense. Kernels have white aleurone and short rachilla hairs.  It has malt protein levels similar to Merit and Harrington, high levels of enzymes like Merit, and higher levels of extract and better malt modification than B1202. It is susceptible to stripe rust, scald, and snow mold, and moderately susceptible to BYD. It was evaluated as Entry 697 in the UC Regional Cereal Testing program from 1982-2006 for fall planting in the intermountain region of northern California. It was tested at trial locations in northern California.  Crop Science 32(3):828 (1992).

Masara is a six-rowed winter feed/malt barley. It is a doubled haploid. Its experimental  designation was STAB 113. Masara is a facultative cultivar: it has a “winter” allele at the Vrn-H1 locus on chromosome 5H but lacks the repressor encoded by the Vrn-H2 locus on 4H. It is a standard height selection (averages about 42 inches in plant height, with fair straw strength) with rough awns and a semi-compact spike. The grain has white aleurone. Masara has high test weight and showed promise as malting barley in repeated micro-malting tests, but it was ultimately not approved by the American Malting Barley Association (AMBA). It has a lower grain protein and enzyme level than is desired for production of lighter beers. At the time of evaluation it was resistant to  stripe rust and susceptible to scald. Bulk seeds of Masara were grown  at Fort Collins, concurrent with replicated yield trials in eastern Colorado. Masara was cross made in 1993. 

Variety Name: Rohan
Variety Aliases: 79Ab812 # Entry 697
Crop Name: Barley 
Germplasm Characteristics: ? 
Crop Variety Class: Six-rowed winter feed barley 
Journal References: Crop Science 32(3):828 (1992).
Pathogens: Stripe rust # scald # snow mold # BYD 
Pedigrees: Steveland/Luther//Wintermalt
Traits: Rough awns # white aleurone # short rachilla hairs # high levels of enzymes # higher levels of extract # better malt modification # short spikes #  dense spikes # good winter hardiness # medium height # intermediate lodging resistance.
Plant Predisposition to Diseases: Susceptible to stripe rust, scald, and snow mold # moderately susceptible to BYD
Revision Date: September 2011
Trial Date: 1982-2006
Release Date: 1991
Trial Evaluation Location: Northern California

Variety Name: Masara
Variety Aliases: STAB 113 # Entry 1129
Crop Name: Barley
Germplasm Characteristics: doubled haploid # has a “winter” allele at the Vrn-H1 locus on chromosome 5H # lacks the repressor encoded by the Vrn-H2 locus on 4H
Crop Variety Class: Six-rowed winter feed/malt barley 
Journal References: ?
Pathogens: Stripe rust, scald
Pedigrees: ? 
Traits:  standard height selection # fair straw strength # rough awns # semi-compact spike # white aleurone # high test weight # lower grain protein # lower enzyme level. 
Plant Predisposition to Diseases: Resistant to stripe rust # susceptible to scald 
Revision Date: ?
Trial Date: ?
Release Date: 1993
Trial Evaluation Location: Fort Collins # Eastern Colorado
"""


exampleThree = """[Text]: Lang-MN, the newest hard red spring wheat variety released by the University of Minnesota. Released in January 2017, Lang-MN is a well-balanced, high yielding spring wheat variety well suited for much of the spring wheat-growing region. It possesses a good disease resistance package with an excellent rating for resistance to scab, stripe and stem rust. Plus it has moderate resistance to leaf rust and bacterial leaf streak. 
Variety Name: Lang-MN 
Variety Aliases: ?
Crop Name: wheat 
Germplasm Characteristics: ?
Crop Variety Class:  hard red spring wheat 
Journal References: ?
Pathogens: scab #  stripe rust # stem rust #  bacterial leaf streak
Pedigrees: ?
Traits: well-balanced # high yielding 
Plant Predisposition to Diseases: excellent resistance to scab  # excellent resistance to stripe rust  # excellent resistance to stem rust  # moderate resistance to leaf rust # moderate resistance bacterial leaf streak
Revision Date: ?
Trial Date: ?
Release Date: 2017
Trial Evaluation Location: ?
"""


prompt_prefix = beforeInstruction + exampleOne + exampleDelimiter + exampleTwo + exampleDelimiter + exampleThree + exampleDelimiter + afterInstruction