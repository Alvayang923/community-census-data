汇总社区级统计数据的Python包
------------
 <br />
 
A Python package for aggregating community-level census data

 <br />
 
简介 Introduction 
------------

该包基于美国统计局发布的社区级数据API 美国社区调查[（ACS）](https://www.census.gov/data/developers/data-sets/acs-5year.html), 郡商业模式[（CBP）](https://www.census.gov/data/developers/data-sets/cbp-nonemp-zbp/cbp-api.html)及邮政编码区域商业模式[（ZCBP）](https://www.census.gov/data/developers/data-sets/cbp-nonemp-zbp/zbp-api.html).  
ACS API基于美国邮政编码表数据集区（ZCTA）而其余API基于美国邮政服务5位数邮政编码（ZIP Codes） （[二者差异](https://www.census.gov/programs-surveys/geography/guidance/geo-areas/zctas.html#:~:text=ZIP%20Code%20Tabulation%20Areas%20(ZCTAs)%20are%20generalized%20areal%20representations%20of,station%20associated%20with%20mailing%20addresses.)）

通过此包，可以实现对于API的数据查询及数据汇报级别的转换。


This library provides a Python interface for the American Community Survey [(ACS)](https://www.census.gov/data/developers/data-sets/acs-5year.html), County Business Patterns [(CBP)](https://www.census.gov/data/developers/data-sets/cbp-nonemp-zbp/cbp-api.html)  and ZIP Codes Business Patterns [(ZBP)](https://www.census.gov/data/developers/data-sets/cbp-nonemp-zbp/zbp-api.html).          

ACS API data are reported on ZIP Code Tabulation Areas(ZCTA) level while others are reported on United States Postal Service ZIP Code level （[the difference between ZIP Codes and ZCTAs](https://www.census.gov/programs-surveys/geography/guidance/geo-areas/zctas.html#:~:text=ZIP%20Code%20Tabulation%20Areas%20(ZCTAs)%20are%20generalized%20areal%20representations%20of,station%20associated%20with%20mailing%20addresses.)）

The package allows users to get data from API and provides some tools for converting the report level.   




数据转换方式 Methology 
------------
* 对于ACS数据
    - 若数据汇总单位为ZCTA，保留原值。
    - 若数据汇总单位为ZIP Codes， 
        - 对于百分比数据，使用对应ZCTA区域的原值, 
        - 对于绝对值数据，使用对应ZCTA区域数据的平均值作为估计。

* 对于商业数据（CBP，ZCBP）
    - 若数据汇总单位为ZIP Codes，保留原值。
    - 若数据汇总单位为ZCTA， 
        - 对于百分比数据，使用对应ZIP Code区域数据的平均值作为估计。
        - 对于绝对值数据，使用对应ZIP Code区域数据之和作为估计。


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


安装方式 Installing 
----------
适用于Python 3.9版本以上，安装语句：

It works with Python versions from 3.9+. You can install using:



```shell
    pip install -i https://test.pypi.org/simple/ community-ry2403
```

测试 Running Tests 
-------------

```shell
poetry add --dev pytest
poetry run pytest
```


基本指引 Basic Tutorial 
--------------


### 模糊搜索变量名 
### Search possible variables 

```python
from community_ry2403.community_ry2403 import variables
#Initialize the class variables
f = variables()   
f.find_variable(keyword='total households by marry')
```

### 查询ZCTA-ZIP-州的对应关系 
### Get the crosswalk of ZCTA-ZIP-State 

```python
from community_ry2403.community_ry2403 import get_code
get_code(area_code=['10025','10036'],level='zip')
```

### 数据查询
### Query data from ACS & CBP & ZCBP API

```python
from community_ry2403.community_ry2403 import census_data        
from community_ry2403.community_ry2403 import business_data        

v1=['DP02_0001E','DP02_0002E','DP02_0003PE']
census_data(year=2019,variable=v1,area_code=['10025','10036'])       

v2 = ['EMP','EMP_N','ESTAB','PAYANN','PAYANN_N','PAYQTR1']
business_data(year=2019,variable=v2,area_code=['10025','10036'],industry=72)

```

### 使用指定汇报级别查询数据 
### Query data with customized report level 
```python
from community_ry2403.community_ry2403 import search
# Initialize the api
api = search()  
v=['DP02_0001E','DP02_0002E','DP02_0003PE']
api.census(area_code=['10025','10036'],geography='zip',year=2019, variable=v)
```









