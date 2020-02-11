import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
import requests
import warnings
import pandas_datareader as pdr
warnings.filterwarnings('ignore', message='Unverified HTTPS request')

##Function to get SPF Recess indicator data

def get_spf():
    
    #Trading dates
    
    spx = yf.Ticker('^GSPC')
    hist = spx.history(period='max')
    hist['date'] = hist.index
    hist['quarter'] = hist['date'].dt.quarter
    hist['year'] = hist['date'].dt.year
    dates = hist.groupby(['year', 'quarter']).agg({'date':'max'}).reset_index()
    
    #Get spf data and merge in trading dates

        
    spf_df = pd.read_excel('https://github.com/trigg989/ffc23/raw/master/Data/Median_RECESS_Level.xlsx')
    spf_df.columns = [col.lower() for col in spf_df.columns.to_list()]
    spf_df = spf_df.merge(dates, left_on = ['year', 'quarter'], right_on = ['year', 'quarter'])
    
    spf_df = spf_df.set_index(spf_df['date'])
    spf_df = spf_df[['recess1','recess2','recess3','recess4','recess5']]
    
    return spf_df

def get_fred_inds(inds,sd):
    
    #Trading dates
    
    spx = yf.Ticker('^GSPC')
    hist = spx.history(period='max')
    hist['date'] = hist.index
    hist['month'] = hist['date'].dt.month
    hist['year'] = hist['date'].dt.year
    dates = hist.groupby(['year', 'month']).agg({'date':'max'}).reset_index()
    
    #Get oecd data
    
    oecd_ind = pdr.DataReader(inds, 'fred', start=sd)
    oecd_ind['month'] = oecd_ind.index.month
    oecd_ind['year'] = oecd_ind.index.year
    oecd_ind = oecd_ind.merge(dates, left_on = ['year', 'month'], right_on = ['year', 'month'])
    oecd_ind.dropna(inplace=True)
    
    oecd_ind = oecd_ind.set_index(oecd_ind['date'])
    oecd_ind = oecd_ind[inds]
    
    return oecd_ind

def get_inv_ind(yield_inds,sd):
    
    #Trading dates
    
    spx = yf.Ticker('^GSPC')
    hist = spx.history(period='max')
    hist['date'] = hist.index
    hist['month'] = hist['date'].dt.month
    hist['year'] = hist['date'].dt.year
    dates = hist.groupby(['year', 'month']).agg({'date':'max'}).reset_index()
    
    
    
    inv_ind = pdr.DataReader(yield_inds, 'fred', start=sd)
    
    inv_ind['month'] = inv_ind.index.month
    inv_ind['year'] = inv_ind.index.year
    inv_ind = inv_ind.groupby(['month','year']).agg({'T10Y2Y':'min'}).reset_index()
    
    inv_ind = inv_ind.merge(dates, left_on = ['year', 'month'], right_on = ['year', 'month'])
    inv_ind.dropna(inplace=True)
    
    inv_ind = inv_ind.set_index(inv_ind['date'])
    inv_ind = inv_ind[yield_inds]
    
    return inv_ind

def get_gdp_fcst():
    
    #Trading dates
    
    spx = yf.Ticker('^GSPC')
    hist = spx.history(period='max')
    hist['date'] = hist.index
    hist['month'] = hist['date'].dt.month
    hist['year'] = hist['date'].dt.year
    dates = hist.groupby(['year', 'month']).agg({'date':'max'}).reset_index()
    
    #Get spf data and merge in trading dates

        
    gdp_df = pd.read_excel('https://github.com/trigg989/ffc23/raw/master/Data/oecd_gdp_growth.xlsx')
    gdp_df.columns = [col.lower() for col in gdp_df.columns.to_list()]
    gdp_df.set_index('date', inplace=True)
    gdp_df['month'] = gdp_df.index.month
    gdp_df['year'] = gdp_df.index.year
    gdp_df = gdp_df.merge(dates, left_on = ['year', 'month'], right_on = ['year', 'month'])
    gdp_df.dropna(inplace=True)
    
    gdp_df.set_index(gdp_df['date'], inplace=True)
    gdp_df = gdp_df[['oecd_us_gdp', 'oecd_gbp_gdp']]
    
    return gdp_df