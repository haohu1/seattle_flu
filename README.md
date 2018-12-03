Here are a few code snippets (in Python 2.7) to:

(1) Pull a list of single family addresses in King County, Washington State from the King County all addresses shapefile
- further improvements: the address list also contains commercial addresses, so we can map the distribution of residential/commercial within each census tract

(2) Add Census Tract FIPS code to each address by querying census tract shapefile
- Alternatively, there are few services at census.gov / FCC to get FIPS code. However in this case an offline solution is better given the large number of addresses (~500k)

(3) Download Census Tract-level demographic data from census.gov API
- demographic data can be pulled easily from either American Community Survey (ACS) or 2010 Census for selected census tracts

(4) Generate a "fake" dataset based on S-I-R epidemic model with Census Tract-level details
 - address was randomly chosen from the list of single family addresses in King County
 - age and gender was randomly chosen based on the distribution in the census tract
 - infection time was from the epidemic model
