
# coding: utf-8

# In[ ]:


# Final Project

# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 

# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 


#Import necessary libraries

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

eurostat = pd.read_csv('nama_10_gdp_1_Data.csv')



# Create the Dashboard for Graph 1 & 2: 

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


eurostat_drop = eurostat.dropna(how='any',subset=["Value"],axis=0)
eurostat_1 = eurostat_drop[-eurostat_drop.GEO.str.contains('Euro')]
eurostat_final = eurostat_1.rename(index = {'Germany (until 1990 former territory of the FRG)': "Germany",'Kosovo (under United Nations Security Council Resolution 1244/99)': "Kosovo",'Former Yugoslav Republic of Macedonia, the': "Macedonia"})

available_indicators = eurostat_final['NA_ITEM'].unique()
available_countries = eurostat_final['GEO'].unique()

# Creating the data frame for the units:

eurostat_final_1 = eurostat_final[eurostat_final['UNIT'] == 'Current prices, million euro']

# Graph 1    
# define the outline style, naming of the axes and the headings

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app.layout = html.Div([
    html.H2('Cloud Computing Assignment - Oskar Schwarze',style={'textAlign': 'center', 'color': 'black'}),
    html.H4('Two Indicators',style={'textAlign': 'left'}),    
    html.Div([
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            ),
            dcc.RadioItems(
                id='xaxis-type',
                options=[{'label': i, 'value': i} for i in ['Linear', 'Log']],
                value = 'Linear',
                labelStyle={'display': 'inline-block'}
            ),
        ],
        style={'width': '45%', 'display': 'inline-block', 'padding': 10}),
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Changes in inventories'
            )
        ],style={'width': '45%', 'float': 'right', 'display': 'inline-block','padding':10})
    ]),            
    
    
    dcc.Graph(id='graph1'),
    
    dcc.Slider( #definition of the year slider
        id='year--slider',
        min=eurostat['TIME'].min(),
        max=eurostat['TIME'].max(),
        value=eurostat['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in eurostat['TIME'].unique()},
    ),
    
    html.H1('\n'),

# Graph 2
# define the outline style, naming of the axes and the headings
    html.H4('Country & Indicator',style={'textAlign': 'left'}),   
    html.Div([ 
        
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Final consumption expenditure'
            ),
        ],
        style={'width': '45%', 'marginTop': 40, 'display': 'inline-block', 'padding': 10}),

        html.Div([
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "Spain"    
            ),
        ],style={'width': '45%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block', 'padding':10})
     ]),
     dcc.Graph(id='graph2')
])


#This is the call back function for the first graph

@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value'),
     dash.dependencies.Input('xaxis-type', 'value')])


# Dataframe for the time

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value, xaxis_type):
    
    eurostatframe = eurostat_final[eurostat_final['TIME'] == year_value]
    return {
        'data': [go.Scatter(
            x=eurostatframe[eurostatframe['NA_ITEM'] == xaxis_column_name]['Value'],
            y=eurostatframe[eurostatframe['NA_ITEM'] == yaxis_column_name]['Value'],
            text=eurostatframe[eurostatframe['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 20,
                'opacity': 0.5,
                'line': {'width': 1.5, 'color': 'red'}
            },
            name=i[:20]
            
        )for i in eurostatframe.GEO.unique()
            ],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'if xaxis_type=='Linear' else 'log'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }


# call back function for the second graph
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])



# Updater for the column names of the graphs

def update_graph(xaxis_column_name, yaxis_column_name):
    


    eurostatframe = eurostat_final_1[eurostat_final_1['GEO'] == yaxis_column_name]
    return {
        'data': [go.Scatter(
            x=eurostatframe['TIME'].unique(),
            y=eurostatframe[eurostatframe['NA_ITEM'] == xaxis_column_name]['Value'],
            text=eurostatframe[eurostatframe['NA_ITEM'] == yaxis_column_name]['Value'],
            mode='lines'
           
        )],
        'layout': go.Layout(
            xaxis={
                'title': xaxis_column_name,
                'type': 'linear'
            },
            yaxis={
                'title': yaxis_column_name,
                'type': 'linear'
            },
            margin={'l': 110, 'b': 50, 't': 20, 'r': 50},
            hovermode='closest'
        )
    }



if __name__ == '__main__':
    app.run_server()

