## Final Project Proposal

#### Name of Project

A Python package for aggregating community-level Census Data

#### Type of project: 

API Client (A) 

#### Brief description of the purpose

Since the COVID-19 pandemic began, more researchers focus on ZIP Code-level data as many states are publishing ZIP Code-level data for cases and deaths. However, there are a number of challenges associated with using ZIP Codes as a unit of analysis. ZIP Codes were designed for delivering mail, not for studying populations. They vary tremendously in size, shape, and population. And they are actually not areas with defined boundaries. 

For this issue, the US Census Bureau creates a real approximation for ZIP Codes called ZIP Code Tabulation Areas (ZCTAs). In most instances the ZCTA code is the same as the ZIP Code for an area. While some ZCTA code has more than one Zip Code and there isn’t a ZCTA for every ZIP Code, which would be a challenge for collecting data and conducting community level research.

To deal with this problem and make it more convient to gain community-level data, this package will comprise several functionalities:

- provide a mapping function to convert ZIP code to ZCTA
- allow users to access community-level census data provided by US Census Bureau
- allow users to look up available variables in dataset with fuzzy search
- allow users to customize the report level either ZIP or ZCTA
- provide some summary statistics and visualization

#### Links to data sources / API etc

1. American Community Survey 5-Year Data, ACS (2009-2019) (ZCTA level)
* API Home Page: https://www.census.gov/data/developers/data-sets/acs-5year.html
* Example Calls:https://api.census.gov/data/2019/acs/acs5/profile/examples.html
* Authentication: This API is an open resource and does not require a key to access.
* There are more than 1000 variables: https://api.census.gov/data/2019/acs/acs5/profile/variables.html
* Data can be retrieved via a URL and returned in JSON format.
* Parameters 
  - get: specify the variables
  - for: specify the geography level
  - in: optional, specify the geography area   

  - Example: api.census.gov/data/2019/acs/acs5/profile?get=NAME,DP02_0001E&for=zip%20code%20tabulation%20area:00601&in=state:72
to gain the variable NAME & DP02_0001E for ZCTA 00601 in state 72


2. ZIP Codes Business Patterns, ZCBP (1994-2018)(Zip Code-Level)
Starting with reference year 2019, ZIP Code Business Patterns data will be available as part of the County Business Patterns (CBP) API.
* API Home Page: https://www.census.gov/data/developers/data-sets/cbp-nonemp-zbp/zbp-api.html
* Example Calls: https://api.census.gov/data/2018/zbp.html
* Authentication: This API is an open resource and does not require a key to access.
* Variables: https://api.census.gov/data/2018/zbp/variables.html
* Data can be retrieved via a URL and returned in JSON format.
* Parameters 
  - get: specify the variables
  - for: specify the geography level 

  - Example: api.census.gov/data/2018/zbp?get=ESTAB,EMPSZES&for=zipcode:20002&NAICS2017=72
to gain the variable ESTAB & EMPSZES for zipcode 20002 for the industry code NAICS2017 72

3. County Business Patterns, CBP (2009-2019)
* API Home Page: https://www.census.gov/data/developers/data-sets/cbp-nonemp-zbp/cbp-api.html
* Example Calls: https://api.census.gov/data/2019/cbp.html
* Authentication: This API is an open resource and does not require a key to access.
* Variables: https://api.census.gov/data/2019/cbp/variables.html
* Data can be retrieved via a URL and returned in JSON format.
* Parameters 
  - get: specify the variables
  - for: specify the geography level 

  - Example: api.census.gov/data/2019/cbp?get=ESTAB,LFO&for=zipcode:20002&NAICS2017=72
to gain the variable ESTAB & LFO for zipcode 20002 for the industry code NAICS2017 72, i.e Total number of establishments for all legal forms of organization, in California for Accommodation and food services industry.

#### Outline the technical steps / challenges you plan to address and include in your submission

* Query API to obtain data from ACS, CBP, and ZCBP with parameters specified
* Handle, parse, and transform JSON return into a dataframe 
* Web scrape the ZIP Code to ZCTA crosswalk from https://udsmapper.org/zip-code-to-zcta-crosswalk/ 
* Create a mapping function that links ZIP Code and ZCTA 
* Use Regex to search patterns in variables, allowing users to look up available variables in dataset with fuzzy search
* Provide summary statistics on the community-level data, and visualize the results
* Wrap up everything in a Python package

