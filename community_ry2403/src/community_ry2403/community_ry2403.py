import os
import requests
import pandas as pd
import numpy as np
from fuzzywuzzy import fuzz

#------------------------------------------------------------------------------------- data prepared from web scraping
label_path = os.path.join(os.path.dirname(__file__), 'label_list.csv')
label_list = pd.read_csv(label_path)
codebook_path = os.path.join(os.path.dirname(__file__), 'codebook.csv')
codebook = pd.read_csv(codebook_path, dtype ='str')


#------------------------------------------------------------------------------------- functions prepared
# for fuzzy search
def get_ratio(str1,str2):
    return fuzz.token_set_ratio(str1,str2)


#prepare function:  convert report level (zip-zcta)
def get_code(area_code,level):
    """
    A function to get the crosswalk of ZCTA, ZIP, State, State Code, given a list of area codes.

    Parameters
    ----------
    area_code: a list of strings
        ZCTA or ZIP Code

    level: str
        ZIP or ZCTA; case-insensitive.

    Returns
    ----------
    A pandas dataframe containing the crosswalk of ZCTA, ZIP, State, State Code


    Examples
    ----------
    >>> get_code(area_code=['10025','10036'],level='zcta')

    [OUT] 
            ZIP	STATE	ZCTA	STATE_CODE
        3213	10025	NY	10025	36
        3224	10036	NY	10036	36
        3249	10108	NY	10036	36
        3250	10109	NY	10036	36
    """
    a = codebook.loc[ codebook[level.upper()].isin(area_code), :]
    return (a)


#prepare function: get business data from API
def business_data(year,variable,area_code,industry):
    """
    A function to get business data with from ZIP Code Business Pattern(ZCBP) API (ZIP Code level).

    Parameters
    ----------
    area_code: a list of strings
    ZIP code 
    year: int
    data reported year
    variable: a list of strings 
    variable codes of data

    Returns
    ----------
    A pandas dataframe containing the report level, the area code and values you looked up


    Examples
    ----------
    >>> v = ['EMP','EMP_N','ESTAB','PAYANN','PAYANN_N','PAYQTR1']
    >>> business_data(year=2019,variable=v,area_code=['10025','10036'],industry=72)

    [OUT] 
        EMP	EMP_N	ESTAB	PAYANN	PAYANN_N	PAYQTR1	NAICS2017	ZIP
        1	0	0	255	0	0	0	72	10025
        2	0	0	577	0	0	0	72	10036
    """
    try:
        dsource = 'zbp' if year <2018 else 'cbp'
        base_url = f'https://api.census.gov/data/{year}/{dsource}'

        zipcode = ','.join(area_code)
        cols = ','.join(variable)
        sector = str(industry)   #only allow single value

        search = requests.get(f'{base_url}?get={cols}&for=zipcode:{zipcode}&NAICS2017={sector}') 
        search.raise_for_status()
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        df = pd.DataFrame(search.json())
        df = df.rename(columns=df.iloc[0]).drop(df.index[0]).rename(columns={'zip code':'ZIP'}) # make the first row be the header
        
        cols = df.columns.drop('ZIP')
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')    # convert all columns except 'ZIP' to integer
        
        return(df)

# prepare function: get census data
def census_data(year,variable,area_code):
    """
    A function to get census data with from American Census Survey(ACS) API (ZCTA Code level).

    Parameters
    ----------
    area_code: a list of strings
    ZCTA code 
    year: int
    data reported year
    variable: a list of strings 
    variable codes of data

    Returns
    ----------
    A pandas dataframe containing the report level, the area code and values you looked up


    Examples
    ----------
    >>> v=['GEOCOMP','DP02_0001E','DP02_0002E','DP02_0003E']
    >>> census_data(2019,variable=v,area_code=['10025','10036'])

    [OUT] GEOCOMP	DP02_0001E	DP02_0002E	DP02_0003E	ZCTA
            1	0	17260	3111	719	    10025
            2	0	41355	14506	5309	10036
    """
    try:
        base_url = f'https://api.census.gov/data/{year}/acs/acs5/profile'

        zipcode = ','.join(area_code)
        cols = ','.join(variable)
        state = get_code(area_code,level='zcta')['STATE_CODE'].unique()[0]

        search = requests.get(f'{base_url}?get={cols}&for=zip%20code%20tabulation%20area:{zipcode}&in=state:{state}')
        search.raise_for_status()
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        df = pd.DataFrame(search.json())
        df = df.rename(columns=df.iloc[0]).drop(df.index[0]).iloc[:,0:len(variable)]     # make the first row be the header
        df['ZCTA'] = area_code
        
        cols = df.columns.drop('ZCTA')
        df[cols] = df[cols].apply(pd.to_numeric, errors='coerce')    # convert all columns except 'ZIP' to integer

        return(df)


#------------------------------------------------------------------------------------- class1: find avaible variables with fuzzy search
class variables(object):
    def __init__(self):
        pass

    def find_variable(self,keyword):
        """
        a class to find available variables from American Census Survey(ACS), Zip Code Businiss Pattern(ZCBP) and Community Business Pattern(CBP) API.

        Parameters
        ----------
        keyword : str
        A string that you wish to look up 

        Returns
        ----------
        Pandas dataframe
        A number of variables that you may intereseted in with labels and variable codes

        Examples
        ----------
        >>> find_variable('total households marry people percent')

        [OUT]   variable	label
            0	DP02_0001E	HOUSEHOLDS BY TYPE!!Total households
            1	DP02_0001PE	HOUSEHOLDS BY TYPE!!Total households
            2	DP02_0014E	HOUSEHOLDS BY TYPE!!Total households!!Househol...
            3	DP02_0014PE	HOUSEHOLDS BY TYPE!!Total households!!Househol...
            4	DP02_0015E	HOUSEHOLDS BY TYPE!!Total households!!Househol...
            5	DP02_0015PE	HOUSEHOLDS BY TYPE!!Total households!!Househol...
            6	DP02PR_0001E	HOUSEHOLDS BY TYPE!!Total households
            7	DP02PR_0001PE	HOUSEHOLDS BY TYPE!!Total households
            8	DP02PR_0014E	HOUSEHOLDS BY TYPE!!Total households!!Househol...
            9	DP02PR_0014PE	HOUSEHOLDS BY TYPE!!Total households!!Househol...
            10	DP02PR_0015E	HOUSEHOLDS BY TYPE!!Total households!!Househol...
            11	DP02PR_0015PE	HOUSEHOLDS BY TYPE!!Total households!!Househol...
    
        """
        assert type(keyword)==str, 'keyword should be a string'
        
        df = pd.DataFrame(columns=['variable','label'])
        label = label_list['labels']
        variable = label_list['Name']
        n = len(label)
        for i,doc in enumerate(label):
            score = get_ratio(keyword,doc)
            new_row = pd.Series({'variable':variable[i],'label':doc})
            if score > 70:
                df = df.append(new_row,ignore_index=True)
        return(df)


#-------------------------------------------------------------------------------------class2: get census & business data with customized report level
class search(object):
    def __init__(self):
        pass

    def census(self,area_code,geography,year, variable):
        """
        A function to get community census data with customized report level (ZIP / ZCTA) from American Census Survey(ACS) API.
        If report level is ZCTA, keep the original value.
        If report level is ZIP, for percent data, use the original value within the correspondent ZCTA area, 
        and for absolute data, use the mean estimate within correspondent ZCTA area.

        Parameters
        ----------
        area_code: a list of strings
        ZIP code or ZCTA code
        geography: str
        data reported level: ZIP or ZCTA; case-insensitive.
        year: int
        data reported year
        variable: a list of strings 
        variable codes of data

        Returns
        ----------
        A pandas dataframe containing the report level, the area code and values you looked up


        Examples
        ----------
        >>> area_code = ['10025','10036']
        >>> geography = 'Zip'
        >>> year = 2019
        >>> variable = ['DP02_0001E','DP02_0001PE']
        >>> census(area_code,geography,year, variable)

        [OUT] ZIP	DP02_0001E_ZIP	DP02_0001PE_ZIP
            0	10025	17260.0	17260
            1	10036	13785.0	41355
        """
        assert all(isinstance(item, str) for item in area_code), "area_code should be a list of strings"
        assert geography.lower() in(['zip','zcta']), f"Data can only be reported by ZCTA or ZIP level, but geography is {geography}."
        assert type(year)==int,'year should be an integer'
        assert all(isinstance(item, str) for item in variable), "variable should be a list of strings"

        need_convert = (geography.lower()=='zip')  
        v = variable
        
        if need_convert == False:
            ans = census_data(year=year,variable=v,area_code = area_code)    
            
        else :
        
            est = label_list.loc[label_list['Name'].isin(v) ,:].reset_index()

            codemap = get_code(area_code,level=geography)[['ZCTA','ZIP']]
            conv_code = list(codemap['ZCTA'])

            df1 = get_code(conv_code,level='ZCTA')[['ZCTA','ZIP']]
            num = df1.groupby('ZCTA').count().rename(columns={'ZIP':'NUM'})
            df2 = census_data(year=year,variable=v,area_code = conv_code)

            merge_data = df1.merge(df2,on="ZCTA", how="left").merge(num,on="ZCTA", how="left")

            for i,var in enumerate(v):
                if est['estimate'][i] == 'percent':
                    merge_data[f'{var}_ZIP'] = merge_data[f'{var}']
                else:
                    merge_data[f'{var}_ZIP'] = merge_data[f'{var}']/merge_data['NUM']
            
            ans = merge_data.loc[merge_data['ZIP'].isin(area_code) , merge_data.columns.str.contains('ZIP')]
        
        return (ans)     



    def business(self,area_code,geography,year, variable,industry):
        """
        A function to get community business data with customized report level (ZIP / ZCTA) from Zip Code Businiss Pattern(ZCBP) and Community Business Pattern(CBP) API.
        If report level is ZIP, keep the original value.
        If report level is ZCTA, for percent data, use the mean estimate within the correspondent ZIP areas, 
        and for absolute data, use the sum estimate within correspondent ZIP areas.

        Parameters
        ----------
        area_code: a list of strings
            ZIP code or ZCTA code
        geography: str
            data reported level: ZIP or ZCTA; case-insensitive.
        year: int
            data reported year
        variable: a list of strings 
            variable codes of data
        industry: int
            NAICS 2017 Code identifying which industry of business data you wish to get

        Returns
        ----------
        A pandas dataframe containing the report level, the area code and values you looked up


        Examples
        ----------
        >>> area_code = ['79925','10025']
        >>> geography = 'Zcta'
        >>> year = 2019
        >>> variable = ['ESTAB','EMP_N','PAYQTR1_N']
        >>> industry=72
        >>> business(area_code, geography ,year, variable, industry)

        [OUT] ZCTA	PAYQTR1_N_ZCTA	EMP_N_ZCTA	ESTAB_ZCTA
            0	10025	0	0	255
            1	79925	0	0	214
        """
        assert all(isinstance(item, str) for item in area_code), "area_code should be a list of strings"
        assert geography.lower() in(['zip','zcta']), f"Data can only be reported by ZCTA or ZIP level, but geography is {geography}."
        assert type(year)==int,'year should be an integer'
        assert all(isinstance(item, str) for item in variable), "variable should be a list of strings"
        assert type(industry)==int,'industry code should be an integer'

        need_convert = (geography.lower()=='zcta')  
        v = variable
        
        if need_convert == False:
            ans = business_data(year=year,variable=v,area_code = area_code,industry=industry)    
            
        else :
            est = label_list.loc[label_list['Name'].isin(v) ,:].reset_index()

            df1 = get_code(area_code,level='ZCTA')[['ZCTA','ZIP']]
            conv_code = list(df1['ZIP'])
            df2 = business_data(year=year,variable=v,area_code=conv_code,industry=industry)
            merge_data = df1.merge(df2,on="ZIP", how="right")

            a = merge_data.loc[:,merge_data.columns!='ZIP']
            ans = merge_data[['ZCTA']]

            for i,var in enumerate(v):
                if est['estimate'][i] == 'percent':
                    t = a.groupby(['ZCTA'])[[f'{var}']].mean().rename(columns={f'{var}':f'{var}_ZCTA'})
                else:
                    t = a.groupby(['ZCTA'])[[f'{var}']].sum().rename(columns={f'{var}':f'{var}_ZCTA'})
                ans = t.merge(ans,on='ZCTA',how='left')
        return(ans)