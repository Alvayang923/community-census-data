# scrape from Web, output CSV files, and save to the same path
import pandas as pd
import re

def get_estimate(col1):
    estimate = re.split('!!', col1, 1)[0].lower()
    return estimate

def get_label(col2):
    labels = re.split('!!', col2, 1)[1]
    return labels

def create_label(zbp_url='https://api.census.gov/data/2017/zbp/variables.html', \
                acs_url='https://api.census.gov/data/2019/acs/acs5/profile/variables.html'):
    """
    A function to output availble variables and labels from ZBP & ACS API with data scraped from Census websites.
    """
    var_bp = pd.read_html(zbp_url)[0]

    #create a new column differentiating absolute number or percent for converting report levels
    var_bp = var_bp[var_bp['Attributes'].notnull()][['Name','Label']].assign(estimate = 'estimate')
    var_bp = var_bp.reset_index().loc[0:9,:]
    var_bp.iat[-1,3] = 'percent'
    var_bp = var_bp.rename(columns={'Label':'labels'})

    var_acs = pd.read_html(acs_url)[0]
    var_acs = var_acs[var_acs['Attributes'].notnull()][['Name','Label']].reset_index().loc[0:1349,:]

    #use RegEx to capture the pattern identifying absolute number or percent for converting report levels     
    var_acs['labels'] = var_acs['Label'].apply(get_label)
    var_acs['estimate'] = var_acs['Label'].apply(get_estimate)

    var_acs = var_acs.iloc[:,var_acs.columns!='Label']

    label_csv = pd.concat([var_acs, var_bp]).drop_duplicates()

    return(label_csv)


def create_codebook(state_url='https://www.nrcs.usda.gov/wps/portal/nrcs/detail/?cid=nrcs143_013696' ,\
    zip_url='https://udsmapper.org/wp-content/uploads/2021/09/ZiptoZcta_Crosswalk_2021.xlsx'):
    """
    A function to create a crosswalk of ZIP-ZCTA-State Code with data scraped from some websites.
    """
    df = pd.read_html(state_url)[0]
    state = df.drop(df.tail(1).index).rename(columns={'Postal Code':'STATE','FIPS':'STATE_CODE'}) # drop last row

    crosswalk = pd.read_excel(zip_url, dtype = str).iloc[:,[0,2,4]].rename(columns={'ZIP_CODE':'ZIP'})

    codebook = pd.merge(crosswalk, state, on="STATE", how="left").iloc[:,[0,1,2,4]].dropna() 
    codebook['STATE_CODE'] = codebook['STATE_CODE'].astype(int)

    return(codebook)

