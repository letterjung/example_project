
# coding: utf-8

# In[ ]:


# Final Project

# Create a Dashboard taking data from [Eurostat, GDP and main components (output, expenditure and income)](http://ec.europa.eu/eurostat/web/products-datasets/-/nama_10_gdp). 
# The dashboard will have two graphs: 

# * The first one will be a scatterplot with two DropDown boxes for the different indicators. It will have also a slide for the different years in the data. 
# * The other graph will be a line chart with two DropDown boxes, one for the country and the other for selecting one of the indicators. (hint use Scatter object using mode = 'lines' [(more here)](https://plot.ly/python/line-charts/) 


import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go


eurostat = pd.read_csv("nama_10_gdp_1_Data.csv")

available_indicators = eurostat['NA_ITEM'].unique()

available_countries = eurostat['GEO'].unique()


# Creating the Dashboard for Graph 1 & 2:

app = dash.Dash(__name__)
server = app.server
app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})



# Creating the data frame for the units:

eurostat_1 = eurostat[eurostat['UNIT'] == 'Current prices, million euro']


app.layout = html.Div([

#Graph 1    
#I create the layout of the first dropdown and set the default value for my graph - Gross domestic product at market prices
# name of the x-axis is: xaxis-columns, and same for the yaxis = yaxiscolumns 
#first graph name = graph1
    
    html.Div([
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'display': 'inline-block'}),
        html.Div([
            dcc.Dropdown( 
                id='yaxis-column1',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Wages and salaries'
            )
        ],style={'width': '30%', 'float': 'right', 'display': 'inline-block'})
    ]),
    dcc.Graph(id='graph1'),
    html.Div(dcc.Slider( 
        id='year--slider',
        min=eurostat['TIME'].min(),
        max=eurostat['TIME'].max(),
        value=eurostat['TIME'].max(),
        step=None,
        marks={str(time): str(time) for time in eurostat['TIME'].unique()},
    ), style={'marginRight': 50, 'marginLeft': 110},),

#Second chart
# Second graph name is id graph2
    
    html.Div([
        
        html.Div([
            dcc.Dropdown( 
                id='xaxis-column2',
                options=[{'label': i, 'value': i} for i in available_indicators],
                value='Gross domestic product at market prices'
            )
        ],
        style={'width': '30%', 'marginTop': 40, 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown( 
                id='yaxis-column2',
                options=[{'label': i, 'value': i} for i in available_countries],
                value= "Spain"    
            )
        ],style={'width': '30%', 'marginTop': 40, 'float': 'right', 'display': 'inline-block'})
     ]),
     dcc.Graph(id='graph2'),
])


#This is the call back function for the first graph

@app.callback(
    dash.dependencies.Output('graph1', 'figure'),
    [dash.dependencies.Input('xaxis-column1', 'value'),
     dash.dependencies.Input('yaxis-column1', 'value'),
     dash.dependencies.Input('year--slider', 'value')])


#Dataframe for the time

def update_graph(xaxis_column_name, yaxis_column_name,
                 year_value):
    
    eurostatframe = eurostat[eurostat['TIME'] == year_value]
    return {
        'data': [go.Scatter(
            x=eurostatframe[eurostatframe['NA_ITEM'] == xaxis_column_name]['Value'],
            y=eurostatframe[eurostatframe['NA_ITEM'] == yaxis_column_name]['Value'],
            text=eurostatframe[eurostatframe['NA_ITEM'] == yaxis_column_name]['GEO'],
            mode='markers',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
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


#This is the call back function for the second chart
@app.callback(
    dash.dependencies.Output('graph2', 'figure'),
    [dash.dependencies.Input('xaxis-column2', 'value'),
     dash.dependencies.Input('yaxis-column2', 'value')])



#As here I have all of the years I just have to update the column names of the chart

def update_graph(xaxis_column_name, yaxis_column_name):
    


    eurostatframe = eurostat_1[eurostat_1['GEO'] == yaxis_column_name]
    return {
        'data': [go.Scatter(
            x=eurostatframe['TIME'].unique(),
            y=eurostatframe[eurostatframe['NA_ITEM'] == xaxis_column_name]['Value'],
            mode='lines',
            marker={
                'size': 15,
                'opacity': 0.5,
                'line': {'width': 0.5, 'color': 'white'}
            }
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
