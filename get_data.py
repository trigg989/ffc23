import pandas as pd
import requests
import numpy as np
import pandas_datareader as pdr
import quandl
import data_load as dl

quandl.ApiConfig.api_key = 'ZuSmYfp_Xc3cJ6a6Zyyz'
sd = '1970-01-01'
ed = '2019-12-31'
fred_recess_inds = ['USARECM' , 'USARECP', 'RECPROUSM156N', 'USRECM']
ice_data = ['BAMLCC0A0CMTRIV']
gold_data = ['GOLDPMGBD228NLBM']
yield_inds = ['T10Y2Y']
bbg_data = ['LBUSTRUU']

def get_data():
    #spx_dy = quandl.get('MULTPL/SP500_DIV_YIELD_MONTH', start_date=sd, end_date=ed)
    spx_pr = pd.DataFrame(pdr.DataReader('^GSPC', 'yahoo', start=sd)['Adj Close'])
    fred_ind = dl.get_fred_inds(fred_recess_inds, sd)
    #ice_tr = pdr.DataReader(ice_data, 'fred', start=sd)
    spf_df = dl.get_spf()
    inv_ind = dl.get_inv_ind(yield_inds,sd)
    #gld_df = pdr.DataReader(gold_data, 'fred', start=sd)
    bbg_df = pd.read_excel('https://github.com/trigg989/ffc23/raw/master/Data/recession%20hindsight.xlsx', sheet_name='Evan', index_col=0)
    gdp_df = dl.get_gdp_fcst()
    

    df = fred_ind.join(spf_df)
    df = df.join(spx_pr)
    #df = df.join(spx_dy)
    df = df.join(inv_ind)
    #df = df.join(ice_tr)
    #df = df.join(gld_df)
    df = df.join(bbg_df)
    df = df.join(gdp_df)
    df = df.fillna(method='ffill').dropna()
    df['date'] = df.index
    df.reset_index(inplace=True, drop=True)
    
    return df