#!/usr/bin/env python
# coding: utf-8

# ### Create dashboard

# In[ ]:


from get_data import get_data
import numpy as np
import pandas as pd 

import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html
import dash_table

import chart_studio.plotly as py
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.subplots import make_subplots


# In[ ]:


df = get_data()


# In[ ]:


external_css = ["https://fonts.googleapis.com/css?family=Overpass:300,300i",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/dab6f937fd5548cebf4c6dc7e93a10ac438f5efb/dash-technical-charting.css"]
    

app = dash.Dash(__name__, external_stylesheets = external_css)


# In[ ]:


app.layout = html.Div(
[

        html.Div([
            html.H1(
                'Cost of Type II Errors in Recession Forecasting',
                className='twelve columns',
                style={'text-align': 'center'}
                    ),
                ],
            className='row'
                ),

    
        html.Div([
            
            html.Div([
                html.Label('Stock fund:'),
                dcc.Dropdown(
                    id='stock_dropdown',
                    options=[{'label': 'SPX', 'value': 'Adj Close'}],
                    value='Adj Close',
                    placeholder='SPX',
                    ),
                    ],
                    className = 'four columns',
                    style = {'marginLeft' : 20},
                    ),
        
            html.Div([
                html.Label('Stock %:'),
                dcc.Input(
                    id='stock_perc',
                    type = 'number',
                    placeholder = 1,
                    value = 80,
                    min = 0,
                    max = 100, 
                    ),
                    ],
                    className='three columns',
                    ),

            html.Div([
                html.Label('Recession Forecast:'),
                dcc.Dropdown(
                    id='recess_forecast',
                    options=[{'label': 'OECD US P->T', 'value': 'USARECM'},
                             {'label': 'OEC US P<-T', 'value': 'USARECP'},
                             {'label': 'Smoothed Recess Probabilities', 'value': 'RECPROUSM156N'},
                             {'label': 'SPF Current Qtr', 'value': 'recess1'},
                             {'label': 'SPF +1 Qtr', 'value': 'recess2'},
                             {'label': 'SPF +2 Qtr', 'value': 'recess3'},
                             {'label': 'SPF +3 Qtr', 'value': 'recess4'},
                             {'label': 'SPF +4 Qtr', 'value': 'recess5'}],
                    value='recess1',
                    placeholder='SPF Current Qtr',
                    ),
                    ],
                    className='four columns',
                    style = {'marginRight' : 20},
                    ),
        
                ],
                className='row',
                ),
   
            html.Div([            
                html.Br(),
            ], className='row'
            ),    
    
        html.Div([
            
            html.Div([
                html.Label('Bond fund:'),
                dcc.Dropdown(
                    id='bond_dropdown',
                    options=[{'label': 'BBG AGG', 'value': 'LBUSTRUU'}],
                    value='LBUSTRUU',
                    placeholder='BBG AGG',
                    ),
                    ],
                    className = 'four columns',
                    style = {'marginLeft' : 20},
                    ),
        
            html.Div([
                html.Label('Bond %:'),
                dcc.Input(
                    id='bond_perc',
                    type = 'number',
                    placeholder = 0,
                    value = 20,
                    min = 0,
                    max = 100, 
                    ),
                    ],
                    className='three columns',
                    ),
            
            html.Div([
                html.Label('Recession Indicator Threshold:'),
                dcc.Input(
                    id='recess_thresh',
                    type = 'number',
                    placeholder = 10,
                    value = 10,
                    min = 0,
                    max = 100, 
                    ),
                    ],
                    className='four columns',
                    style = {'marginRight' : 20},
                    ),            
        
        
                    ],
                    className='row'
                    ),
    
            html.Div([            
                html.Br(),
            ], className='row'
            ),    
                    
        html.Div([        
            html.Div([
                html.Label('Starting $'),
                dcc.Input(
                    id='starting_money',
                    type = 'number',
                    placeholder = 10000,
                    value = 10000,
                    min = 0,
                    ),
                    ],
                    className='four columns',
                    style = {'marginLeft' : 20},
                    ),              
       
            html.Div([
                html.Label('$ Contribution'),
                dcc.Input(
                    id='contribution',
                    type = 'number',
                    placeholder = 100,
                    value = 100,
                    min = 0,
                    ),
                    ],
                    className='four columns',
                    ),
                ],
                 className='row'
        ),
            
            html.Div([            
                html.Br(),
                html.Br(),
            ], className='row'
            ),
    
        html.Div([
            dcc.Graph(id='returns_plot',style={'max-height': '600', 'height': '60vh'}),
        ],
            className='row',
            style={'width' :'85%', 'margin-left':'auto', 'margin-right':'auto'}
        ),
    
        html.Div([
            dcc.Graph(id='growth_plot', style={'max-height': '600', 'height': '60vh'}),
        ],
            className='row',
            style={'width' :'85%', 'margin-left':'auto', 'margin-right':'auto'}
        ),

            
    html.Div([
            html.Div([
            dcc.Graph(id='ef_plot', style={'max-height': '400', 'height': '40vh'}),
        ],
            className= 'seven columns'

        ),
    
    html.Div([html.Br(),html.Br(),
              dash_table.DataTable(
        id = 'data_table', 
            columns=[
            {'name': 'Measure', 'id' : 'Measure'},
            {'name': 'Allocated', 'id': 'Allocated'},
            {'name': 'Recession-Allocated', 'id': 'Recession-Allocated'},
            {'name': 'All Stock', 'id': '100% Stock'},
            {'name': 'All Bond', 'id': '100% Bond'}]),
             ], className = 'five columns', style={'margin-top':'40'}
              ),
    ], className = 'row', style={'width' :'85%', 'margin-left':'auto', 'margin-right':'auto'}
    ),
    
            html.P(
            hidden='',
            id='returns_json',
            style={'display': 'none'}
        
        ),
            
            
            
            
            
            
],
    
    
    
    
    
     style={
        'width': '85%',
        'max-width': '1200',
        'margin-left': 'auto',
        'margin-right': 'auto',
        'font-family': 'overpass',
        'background-color': '#F3F3F3',
        'padding': '40',
        'padding-top': '20',
        'padding-bottom': '20',
    },
)


# In[ ]:


#Produce returns DF

@app.callback(Output('returns_json', 'hidden'),
              [Input('stock_dropdown', 'value'),
               Input('stock_perc', 'value'),
               Input('bond_dropdown', 'value'),
               Input('bond_perc', 'value'),
               Input('recess_forecast', 'value'),
               Input('recess_thresh', 'value')])

def calc_returns(stock, stock_perc, bond, bond_perc, forecast, threshold):
    
    
    stock_perc = stock_perc/100
    bond_perc = bond_perc/100
    
    df['stock returns'] = (df[stock] - df[stock].shift()) / df[stock].shift()
    df['bond returns'] = (df[bond] - df[bond].shift()) / df[bond].shift()
    
    df['allocated_non_recess_return'] = (df['stock returns'] * stock_perc) + (df['bond returns'] * bond_perc)
    df['recession_ind'] = np.where(df[forecast] >= threshold, 1, 0)
    df['recession_return'] = np.where(df['recession_ind'] == 1, (df['stock returns'] * bond_perc) + (df['bond returns'] * stock_perc), (df['stock returns'] * stock_perc) + (df['bond returns'] * bond_perc))

    df2 = df[['date', 'stock returns', 'bond returns', 'allocated_non_recess_return', 'recession_ind', 'recession_return']]
    
    df2.dropna(inplace=True)
    df2.reset_index(inplace=True)
    
    return df2.to_json()
    
    


# In[ ]:


#Produce plot of returns

@app.callback(Output('returns_plot', 'figure'),
              [Input('returns_json', 'hidden')])
              
def ret_plot(json):
    
    df = pd.read_json(json)

    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df['date'], y=df['stock returns'], name = 'stock returns'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['date'], y=df['bond returns'], name = 'bond returns'), secondary_y=False)
    #fig.add_trace(go.Scatter(x=df['date'], y=df['gold returns'], name = 'gold returns'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['date'], y=df['allocated_non_recess_return'], name = 'allocated returns'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['date'], y=df['recession_return'], name = 'recess allocated returns'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['date'], y=df['recession_ind'], name = 'recession indicator'), secondary_y = True)
    
    fig.update_layout(title = 'Monthly Returns across Asset Allocations', paper_bgcolor = '#F3F3F3')

    return fig
        
              
              


# In[ ]:


# Produce growth of 10k

@app.callback(Output('growth_plot', 'figure'),
              [Input('returns_json', 'hidden'),
               Input('starting_money', 'value'),
               Input('contribution', 'value')])

def growth_plot(json, start, contribution):
    
    df = pd.read_json(json)
    
    length = list(range(len(df.index)))
    
    ret_cols = ['stock returns', 'bond returns', 'allocated_non_recess_return', 'recession_return']
    
    growth_cols = ['stock growth', 'bond growth',  'allocated_growth', 'allocated_recess_growth']

    for ret, growth in zip(ret_cols, growth_cols):
        for x in length:
            if x == 0:
                df.loc[x, growth] = start * (1 + df.loc[x, ret]) 

            else:
                df.loc[x, growth] = (df.loc[x-1, growth] + contribution) *  (1 + df.loc[x, ret])


    
    fig = make_subplots(specs=[[{"secondary_y": True}]])

    fig.add_trace(go.Scatter(x=df['date'], y=df['stock growth'], name = 'stock growth'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['date'], y=df['bond growth'], name = 'bond growth'), secondary_y=False)
    #fig.add_trace(go.Scatter(x=df['date'], y=df['gold growth'], name = 'gold growth'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['date'], y=df['allocated_growth'], name = 'allocated growth'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['date'], y=df['allocated_recess_growth'], name = 'recess allocated growth'), secondary_y=False)
    fig.add_trace(go.Scatter(x=df['date'], y=df['recession_ind'], name = 'recession indicator'), secondary_y = True)
    
    fig.update_layout(title = 'Growth of $' + str(start) + ' with Periodic Contribution of $' + str(contribution), paper_bgcolor = '#F3F3F3' )
    
    return fig


# In[ ]:


# Produce efficient frontier

@app.callback(Output('ef_plot', 'figure'),
              [Input('returns_json', 'hidden')])

def efficient_frontier(json):
    
    df = pd.read_json(json)
    
    rets_df = df[['stock returns', 'bond returns']]
    noa = len(rets_df.columns)
    
    def port_ret(weights):
        return np.sum(rets_df.mean() * weights) * 12
    
    def port_vol(weights):
        return np.sqrt(np.dot(weights.T, np.dot(rets_df.cov() * 12, weights)))
    
    allocated_ret = np.sum(df['allocated_non_recess_return'].mean()) * 12
    allocated_vol = df['allocated_non_recess_return'].std()*np.sqrt(12)
    res_ret = np.sum(df['recession_return'].mean()) * 12
    res_vol = df['recession_return'].std()*np.sqrt(12)
        
    prets = []
    pvols = []
    for p in range (2500):
        weights = np.random.random(noa)
        weights /= np.sum(weights)
        prets.append(port_ret(weights))
        pvols.append(port_vol(weights))
    prets = np.array(prets)
    pvols = np.array(pvols)
    data = go.Scatter(x=pvols, y=prets, mode='markers', name='Base Allocations')
    fig = go.Figure(data)
    fig.add_trace(go.Scatter(x=[allocated_vol], y=[allocated_ret], mode='markers', name='Static Allocation'))
    fig.add_trace(go.Scatter(x=[res_ret], y=[res_vol], mode='markers', name='Recession Allocation'))
    
    fig.update_layout(title = 'Efficient Frontier', paper_bgcolor = '#F3F3F3')
    
    return fig


# In[ ]:


#Produce table with various metrics

@app.callback(Output('data_table', 'data'),
              [Input('returns_json', 'hidden')])

def data_table(json):
    
    df = pd.read_json(json)
    
    measure_df = pd.DataFrame(columns = ['Allocated', 'Recession-Allocated', '100% Stock', '100% Bond'])
    
    input_cols = ['allocated_non_recess_return', 'recession_return', 'stock returns', 'bond returns']
    rets = []
    vols = []
    dvols = []
    
    names = ['Sharp', 'Sortino']
    sharps = []
    sortinos = []
    te = []
    ir = []
    
    #Produce sharpe ratio
    for i in input_cols:
        rets.append(np.sum(df[i].mean()) * 12)
        vols.append(df[i].std()*np.sqrt(12))
    for l in list(range(0,len(rets))):
        sharps.append(round((rets[l] - .02)/vols[l],2))

    #Produce sortino ratio
    for i in input_cols:
        downside_df = df.loc[df[i] < 0]
        dvols.append(downside_df[i].std()*np.sqrt(12))
    for l in list(range(0,len(rets))):
        sortinos.append(round((rets[l] - .02)/dvols[l],2))
    
    
    #Produce Tracking Error
    for i in input_cols:
        te_data = np.sqrt(np.sum((df[i] - df['stock returns'])**2) / (len(df) - 1))
        te.append(round(te_data,2))
        
    #Produce information ratio
    for l in list(range(0,len(rets))):
        ir.append(round((rets[l] - rets[2])/ te[l],2))
        
        
    
    measure_df.loc[len(measure_df)] = sharps
    measure_df.loc[len(measure_df)] = sortinos
    measure_df.loc[len(measure_df)] = te
    measure_df.loc[len(measure_df)] = ir
    
    measure_df['Measure'] = ['Sharpe', 'Sortino', 'TE', 'IR']
    
    data = measure_df.to_dict('records')

    return data
    

    

    
    
    
    
    
    
    


# In[ ]:


if __name__ == '__main__':
    app.server.run(debug=False)

