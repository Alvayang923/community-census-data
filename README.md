Final Project of Modern Data Struture (GR5072)
=============
community_ry2403
=============

A Python package for aggregating community-level Census Data.

Install from: https://test.pypi.org/project/community-ry2403/


Introduction
------------

This library provides a Python interface for the [ACS API](https://www.census.gov/data/developers/data-sets/acs-5year.html), [CBP API](https://www.census.gov/data/developers/data-sets/cbp-nonemp-zbp/cbp-api.html)  and [ZCBP API](https://www.census.gov/data/developers/data-sets/cbp-nonemp-zbp/zbp-api.html).      


ACS API data are reported on ZIP Code Tabulation Areas(ZCTA) level while others are reported on Zip Code level.      

The package allows users to get data from API and provides some tools for converting the report level.   


Methology
------------
How to convert?
* For census data (from ACS)
    - If report level is ZCTA, keep the original value.
    - If report level is ZIP, 
        - for percent data, use the original value within the correspondent ZCTA area, 
        - for absolute number, use the mean estimate within correspondent ZCTA area.

* For business data (from CBP,ZCBP)
    - If report level is ZIP, keep the original value.
    - If report level is ZCTA, 
        - for percent data, use the mean estimate within the correspondent ZIP areas, 
        - for absolute number, use the sum estimate within correspondent ZIP areas.


Installing
----------

It works with Python versions from 3.9+.

You can install using:

```shell
    pip install -i https://test.pypi.org/simple/ community-ry2403
```



Running Tests
-------------

```shell
poetry add --dev pytest
poetry run pytest
```



Basic Tutorial 
--------------


### search possible variables

```python
from community_ry2403.community_ry2403 import variables
#Initialize the class variables
f = variables()   
f.find_variable(keyword='total households by marry')
```

### Get the crosswalk of ZCTA-ZIP-State

```python
from community_ry2403.community_ry2403 import get_code
get_code(area_code=['10025','10036'],level='zip')
```

### Query data from ACS & CBP & ZCBP API

```python
from community_ry2403.community_ry2403 import census_data        
from community_ry2403.community_ry2403 import business_data        

v1=['DP02_0001E','DP02_0002E','DP02_0003PE']
census_data(year=2019,variable=v1,area_code=['10025','10036'])       

v2 = ['EMP','EMP_N','ESTAB','PAYANN','PAYANN_N','PAYQTR1']
business_data(year=2019,variable=v2,area_code=['10025','10036'],industry=72)

```

### Query data with customized report level
```python
from community_ry2403.community_ry2403 import search
# Initialize the api
api = search()  
v=['DP02_0001E','DP02_0002E','DP02_0003PE']
api.census(area_code=['10025','10036'],geography='zip',year=2019, variable=v)
```

