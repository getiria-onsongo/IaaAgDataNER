context_length = 4000 # Value set by openAI. At the moment you cannot change this value

variety_name_key = "variety name"

missing_symbol = "?"

exampleDelimiter = """\n###\n\n"""

beforeInstruction = """Below are instances showing how to extract information from a given [Text]. The symbol """ + missing_symbol +  """ is used to represent missing information. The symbol # is used to separate instance. The symbol """ + exampleDelimiter + """ is used to separate examples. Please break out sentences describing multiple traits. For example 'Plants are medium large, upright with the tendency to spread' would be listed as  'medium large plant' #  'upright plant' #  'plant has a tendency to spread \n"""

afterInstruction =  """ Using the above instances as examples of how to extract information, and ? to represent missing values, extract: Variety Name,  Variety Aliases, Crop Name, Genotypic Information, Crop Variety Class, Pedigree, General Traits, Disease Traits, Revision Date, Trial Date, Release Date and Geographic Range from the following [Text]:
\n"""
sample_output = """[Text]: Mokua is a six-rowed winter feed barley. It was released by the Arizona AES in 2006. It is a doubled-haploid line produced from the cross I1162-19/J-126//WA1245///Steptoe. Its experimental designation was ORW-6. It is medium height (averages about 41 inches, slightly taller than Kold) and medium early maturing with fair straw strength. It has rough awns and a semi-compact spike. At the time of evaluation it was resistant to stripe rust and moderately susceptible to scald, net blotch, and BYD. It was evaluated as Entry 964 in the UC Regional Cereal Testing program from 1997-2006 for fall planting in the intermountain region of northern California and in 2008 for fall planting in the Central Valley of California. Arizona AES (2006)

Variety Name: Mokua
Variety Aliases: ORW-6, Entry 964 
Crop Name: Barley 
Genotypic Information: Doubled-haploid line 
Crop Variety Class: Six-rowed winter feed barley 
Pedigree: I1162-19/J-126//WA1245///Steptoe 
General Traits: Medium height # medium early maturing # fair straw strength # rough awns # semi-compact spike   
Disease Traits: Resistant to stripe rust #  moderately susceptible to scald # moderately susceptible to net blotch # moderately susceptible to BYD.
Revision Date: September 2011
Trial Date: 1997-2006 
Release Date: 2006
Geographic Range: Arizona # Central Valley of California
"""


exampleOne = """ [Text]: 
may 14, 2018

august 24, 2022

this article was posted in fact sheet.

----------------------------
| yukon gold (g6666-4y) |  | 
----------------------------

parentage – norgleam x w5279-4 (yellow-fleshed diploid hybrid of s. phureja)1

breeder – horticulture science department, ontario agricultural college and the university of guelph, ontario jointly released the line in 19811

maturity – mid-season

usage – fresh market

plant – medium large, upright with the tendency to spread; lower three-quarters of stems is purplish with the upper quarter faintly purple to green in color1,2

leaves – moderately shiny, olive green, stiffly pubescent2; a distinct terminal leaflet with four pairs of primary leaflets which are largest near the terminal leaf is typically observed, petioles extend downward1; secondary and primary leaflets numbers vary with less observed on lower than upper leaves2

flowers – violet to light-violet with yellow anthers; buds are light green to purplish-green1,2

tubers – oval shaped but slightly flattened; yellow-white skin with shallow, pink eyes that distinguish yukon gold from other yellow-skinned varieties, light-yellow tuber flesh1,2

strengths – resistant to mild mosaic; moderately resistant to potato leafroll virus; retains its yellow flesh when baked, boiled or fried1,2

weaknesses – susceptible to potato virus y, common scab, hollow heart, and internal necrosis; air pollution can be a problem in some growing areas1,2


last revised: 8/24/22

Variety Name: yukon gold
Variety Aliases: g6666-4y
Crop Name: potato
Genotypic Information: diploid hybrid  
Crop Variety Class: yellow fleshed
Pedigree: norgleam x w5279-4
General Traits: medium large plant # upright plant # plant has a tendency to spread # oval shaped tuber # slightly flattened tuber # violet to light-violet flowers # yellow anthers # yellow white tuber skin # shallow, pink eyes
Disease Traits:  moderately resistant to potato leafroll virus # resistant to mild mosaic # susceptible to common scab # susceptible to hollow heart # susceptible to internal necrosis # susceptible to potato virus y
Revision Date: 8/24/22
Trial Date: ?
Release Date: 1981
Geographic Range: Ontario
"""

exampleTwo = """ [Text]: blackberry 
(msz109-10pp) 

parentage: comn07-w112bg1 
x msu200-5pp 

strengths: blackberry is a tablestock variety with unique purple skin and a deep 
purple flesh.  the tubers have an attractive, uniform, round shape and a purple 
flesh with common scab resistance and low incidence of internal defects.  yield 
can be high under irrigated conditions.  blackberry will also chip-process out of the 
field. 

morphological characteristics: 
plant: full-sized vine, semi-erect with a balance between stems and foliage visible, 
and flowers. 

agronomic characteristics: 
maturity: mid-season. 
tubers: round tubers with unique purple skin and deep purple flesh.   
yield: average to above average yield. 
specific gravity: averages 1.070 in michigan. 
culinary quality: gourmet specialty with deep purple flesh and also chip-
processes. 
foliage: full-sized, semi-erect vine. 
diseases: good common scab resistance. 

Variety Name: blackberry
Variety Aliases: msz109-10pp
Crop Name: potato 
Genotypic Information: ? 
Crop Variety Class: tablestock   
Pedigree: comn07-w112bg1 x msu200-5pp 
General Traits: unique purple skin # deep purple flesh # attractive tubers # uniform tubers # round shape tubers # purple flesh # high yield under irrigation # full-sized vine plant # mid-season maturity # average to above average yield
Disease Traits: common scab resistance # low incidence of internal defects
Revision Date: ?
Trial Date: ?
Release Date: ? 
Geographic Range: ?
"""


exampleThree = """ [Text]: Lang-MN, the newest hard red spring wheat variety released by the University of Minnesota. Released in January 2017, Lang-MN is a well-balanced, high yielding spring wheat variety well suited for much of the spring wheat-growing region. It possesses a good disease resistance package with an excellent rating for resistance to scab, stripe and stem rust. Plus it has moderate resistance to leaf rust and bacterial leaf streak. 
Variety Name: Lang-MN 
Variety Aliases: ?
Crop Name: wheat 
Genotypic Information: ?
Crop Variety Class:  hard red spring wheat 
Pedigree: ?
General Traits: well-balanced # high yielding 
Disease Traits:  excellent resistance to scab  # excellent resistance to stripe rust  # excellent resistance to stem rust  # moderate resistance to leaf rust # moderate resistance bacterial leaf streak
Revision Date: ?
Trial Date: ?
Release Date: 2017
Geographic Range: ?
"""


exampleFour = """ [Text]:
improving your process, enhancing your products, increasing your profits

umn releases mn-rothsay wheat

posted on

june 20, 2022

mn-rothsay wheat. photo: dylan vanboxtel. © regents of the university of minnesota.

the university of minnesota has released a new hard red spring wheat variety called ‘mn-rothsay.’ the variety features excellent straw strength with a good combination of yield, protein, and disease resistance.

“mn-rothsay has straw strength comparable to linkert but has about 10 percent higher grain yield,” says jim anderson, university of minnesota wheat breeder in the department of agronomy and plant genetics. “the exceptional straw strength of linkert was largely responsible for its 5-year reign from 2016–2020 as the most popular variety in the state, so our expectation is that mn-rothsay’s higher grain yields, comparable or higher than other popular varieties, and improved disease resistance compared to linkert will be attractive to growers.”

in addition to high yields, the protein level of mn-rothsay is higher than other top yielding varieties along with good test weight and a good pre-harvest sprouting rating. mn-rothsay has moderate overall disease resistance, with a very good score for leaf and stem rust, and a good fusarium head blight (fhb) rating.

prior to being formally named, mn-rothsay was tested as mn15005-4. the line stood out in both state and regional trials including the uniform regional nurseries trials, where it finished second in grain yield out of 33 experimental entries in 2018, eighth out of 34 in 2019, and had the best straw strength of all entries in both years.

jochum wiersma, university of minnesota extension small grains specialist, stresses that, “the value growers place of straw strength cannot be overstated, making mn-rothsay the logical choice to replace linkert in the u’s line-up.”

mcia certified seed growers received allocations of foundation seed of mn-rothsay this spring. despite the tough weather this spring, seed growers are excited about the new variety and will have seed available for planting next year. look for a list of growers in the mcia directory this fall.

the new release is named in honor of the city of rothsay, minnesota, which is an area of the state with a long history of wheat production.

Variety Name: mn-rothsay 
Variety Aliases: mn15005-4
Crop Name: wheat
Genotypic Information: ? 
Crop Variety Class:  hard red spring wheat
Pedigree:  ?
General Traits: excellent straw strength # good pre-harvest sprouting rating # good test weight # higher grain yields # higher protein level
Disease Traits:  moderate resistance to fusarium head blight # moderate overall disease resistance # very good resistance to leaf rust # very good resistance to stem rust
Revision Date: June 20, 2022
Trial Date: 2016-2020
Release Date: ?
Geographic Range: ?
"""

prompt_prefix = beforeInstruction + exampleOne + exampleDelimiter + exampleTwo + exampleDelimiter + exampleThree + exampleDelimiter +  exampleFour + exampleDelimiter + afterInstruction

temp1 = """ [Text]: Ishi is a six-rowed spring feed barley. Its occurrence and resistance stability were studied along with a susceptible control over four years (2005-08). Its experimental designations were UC 1047 and UCD PYT99 A-13. Ishi has the sdw1 gene and is short statured, averaging 84.6 cm, and is similar to UC 937 and 3.6 cm taller than UC 933, averaged over 32 location-years in Central Valley and Central Coast environments. For lodging resistance (fair) it was superior to UC 937 but similar to UC 933 over 20 environments where lodging occurred. For days to heading it averaged 4 days earlier than UC 937 and 3 days later than UC 933, but all three cultivars were similar for time to maturity (medium late). It is heterogeneous for rough and smooth awns, having less than one-percent smooth awned plants. The spike is waxy and semi-erect. The kernels are covered and the aleurone is non-blue. Grains are long (>10mm) and wrinkled, with hairs on the ventral furrow. Rachilla hairs are long. At the time of release Ishi was resistant to scald and powdery mildew, moderately resistant to stripe rust, BYD and net blotch, and moderately susceptible to leaf rust. It subsequently became moderately susceptible to net blotch. It was evaluated as Entry 1047 in the UC Regional Cereal Testing program from 2000 present for late fall planting in the Central Valley and the south-central coastal region of California and for spring planting in the intermountain area of northern California. Crop Science 46:1396 (2006) 

Variety Name: Ishi 
Variety Aliases: UC 1047 # UCD PYT99 A-13 # Entry 1047 
Crop Name: Barley 
Genotypic Information: sdw1 gene 
Crop Variety Class: Six-rowed spring feed barley 
Pedigree: ?
General Traits: Short statured # medium late time to maturity # heterogeneous for rough and smooth awns # waxy and semi-erect spike # covered kernels # non-blue aleurone # long (>10mm) and wrinkled grains # hairs on the ventral furrow # long rachilla hair. 
Disease Traits: resistant to scald #  resistant to powdery mildew # moderately resistant to stripe rust # moderately resistant to BYD # moderately resistant to net blotch # moderately susceptible to leaf rust # moderately susceptible to net blotch.
Revision Date: ?
Trial Date: 2005-08
Release Date: ?
Geographic Range: Central Valley # south-central coastal region of California # Northern California."""

temp2 = """ [Text]: Masara is a six-rowed winter feed/malt barley. It is a doubled haploid. Its experimental  designation was STAB 113. Masara is a facultative cultivar: it has a “winter” allele at the Vrn-H1 locus on chromosome 5H but lacks the repressor encoded by the Vrn-H2 locus on 4H. It is a standard height selection (averages about 42 inches in plant height, with fair straw strength) with rough awns and a semi-compact spike. The grain has white aleurone. Masara has high test weight and showed promise as malting barley in repeated micro-malting tests, but it was ultimately not approved by the American Malting Barley Association (AMBA). It has a lower grain protein and enzyme level than is desired for production of lighter beers. At the time of evaluation it was resistant to  stripe rust and susceptible to scald. Bulk seeds of Masara were grown  at Fort Collins, concurrent with replicated yield trials in eastern Colorado. Masara was cross made in 1993.

Variety Name: Masara
Variety Aliases: STAB 113 # Entry 1129
Crop Name: Barley
Genotypic Information: doubled haploid # has a “winter” allele at the Vrn-H1 locus on chromosome 5H # lacks the repressor encoded by the Vrn-H2 locus on 4H
Crop Variety Class: Six-rowed winter feed/malt barley 
Pedigree: ? 
General Traits:  fair straw strength # rough awns # semi-compact spike # white aleurone # high test weight # lower grain protein # lower enzyme level 
Disease Traits:  resistant to stripe rust # susceptible to scald 
Revision Date: ?
Trial Date: ?
Release Date: 1993
Geographic Range: Fort Collins # Eastern Colorado
 """

temp3 = """ [Text]: Rohan is a six-rowed winter feed barley. It was released by the USDA-ARS and the Idaho AES in 1991 (Revised September 2011). It was  selected from the cross Steveland/Luther//Wintermalt. Its experimental designation was 79Ab812. It has rough awns,  good winter hardiness, and is medium height with intermediate lodging resistance. Spikes are short and dense. Kernels have white aleurone and short rachilla hairs.  It has malt protein levels similar to Merit and Harrington, high levels of enzymes like Merit, and higher levels of extract and better malt modification than B1202. It is susceptible to stripe rust, scald, and snow mold, and moderately susceptible to BYD. It was evaluated as Entry 697 in the UC Regional Cereal Testing program from 1982-2006 for fall planting in the intermountain region of northern California. It was tested at trial locations in northern California.  Crop Science 32(3):828 (1992).

Variety Name: Rohan
Variety Aliases: 79Ab812 # Entry 697
Crop Name: Barley 
Genotypic Information: ? 
Crop Variety Class: Six-rowed winter feed barley 
Pedigree: Steveland/Luther//Wintermalt
General Traits: Rough awns # white aleurone # short rachilla hairs # high levels of enzymes # higher levels of extract # better malt modification # short spikes #  dense spikes # good winter hardiness # medium height 
Disease Traits: susceptible to stripe rust # susceptible to  scald # susceptible to  snow mold # moderately susceptible to BYD
Revision Date: September 2011
Trial Date: 1982-2006
Release Date: 1991
Geographic Range: Northern California
"""