from community_ry2403 import community_ry2403

import pytest 
import pandas as pd

def test_search():

    area_code = ['79925','10025']
    geography = 'Zip'
    year=2019
    variable = ['ESTAB','EMP_N','PAYQTR1_N']
    industry=72
    
    api = community_ry2403.search()
    actual = api.business(area_code, geography ,year, variable,industry)

    assert type(actual)==pd.DataFrame,'test failed'


def test_variables():
    find = community_ry2403.variables()
    actual = find.find_variable('total households marry people percent')
    assert type(actual)==pd.DataFrame,'test failed'
