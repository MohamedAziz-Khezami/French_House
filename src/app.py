# Libraries
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os
import folium
import dash_leaflet as dl
import json


# App Config

app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
)

server = app.server

app.title = "French House"


# Database connection
# database = pd.read_csv('database/train.csv')
df = pd.read_csv('database/test.csv')


# Folium map
def map():
    ...





# avg total price per month line chart
line_chart = {
    'data': [
        go.Scatter(
            x=df['date_mutation'],
            y=df['valeur_fonciere'],
            mode='lines',
            name='Valeur fonciere',
            
           
        )
    ],
    'layout': go.Layout(
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        xaxis=dict(
            title='Date mutation',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=True,)
        
        ,
        yaxis=dict(
            title='Valeur fonciere',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=True,
        ),
        
 
    )

}









# pie chart: effects on price
pie_chart = {
    'data': [
        go.Pie(
            labels=['A', 'B', 'C', 'D', 'E'],
            values=[10, 20, 30, 40, 50],
            marker=dict(colors=['#252E3F', '#9ECAE1', '#252E3F', '#9ECAE1', '#252E3F']),
        )
    ],
    'layout': go.Layout(
        title='Pie Chart',
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        showlegend=True,
        width=1000,
        height=500
    )
}



#horizontal bar chart most expensive cities
horizontal_bar_chart = {
    'data': [
        go.Bar(
            x=[20, 14, 23],
            y=["giraffes", "orangutans", "monkeys"],
            orientation="h",
            marker=dict(
                color="rgb(158,202,225)",
                line=dict(color="rgb(8,48,107)", width=1.5),
            ),
        )
    ],
    'layout': go.Layout(
        title='Most expensive cities',
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        xaxis=dict(
            title='Price',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=True,
            )
        
        ,
        yaxis=dict(
            title='City',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=True,
        ),
        width=1000,
        height=500
    )
}





#histogram: avg price per year
histogram = {
    'data': [
        go.Histogram(
            x=df['date_mutation']
        )
    ],
    'layout': go.Layout(
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        xaxis=dict(
            title='Date mutation',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=False,)
        
        ,
        yaxis=dict(
            title='Count',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=False,
        ),#1F77B4
        title='Histogram',
        width=1000,
        height=600,
    )
}




#cards: avg rooms, avg surface, avg price, house type,...
cards = {
    'data': [
        go.Indicator(
            mode="number",
            value=5,
            title={"text": "Avg rooms"},
            number={"valueformat": ".0f", "suffix": " rooms"},

        )
    ],
    'layout': go.Layout(
        width=500,
        height=300,
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
    )
}





# The main app
app.layout = html.Div(

    [

        #for the map use plotly


        html.Div(
            dcc.Graph(
                id="line-chart",
                figure=line_chart,
                config={"displayModeBar": 'hover'},
                animate=True
            ),
            style={'width': '89%', 'margin' : 'auto', 'backgroundColor': ''}
        ),

        html.Div(
            [
                dcc.Graph(
                    id="pie-chart",
                    figure=pie_chart,
                    config={"displayModeBar": 'hover'},
                    animate=True
                ),

                dcc.Graph(
                    id="bar-chart",
                    figure=horizontal_bar_chart,
                    config={"displayModeBar": 'hover'},
                    animate=True
                ),

            ],
            style={'width': '100%', 'display': 'flex', 'backgroundColor': '#1F2630', 'flex-direction': 'row', 'justify-content': 'space-around'}
        ),

        html.Div(
            [
          
                dcc.Graph(
                    id="histogram",
                    figure=histogram,
                    config={"displayModeBar": 'hover'},
                    animate=True
                ),
            

                # Updated section: Cards in a grid layout using CSS Grid
                html.Div(
                    children=[
                       dcc.Graph(
                         
                           figure=cards,
                           config={"displayModeBar": 'hover'},
                           animate=True
                       ),
                                              dcc.Graph(
                         
                           figure=cards,
                           config={"displayModeBar": 'hover'},
                           animate=True
                       ),
                                              dcc.Graph(
                         
                           figure=cards,
                           config={"displayModeBar": 'hover'},
                           animate=True
                       ),
                                              dcc.Graph(
                        
                           figure=cards,
                           config={"displayModeBar": 'hover'},
                           animate=True
                       ),

                    ],
                    style={
                        "display": "grid",  # Enable grid layout
                        "gridTemplateColumns": "repeat(2, 1fr)",  # 2 columns layout
                        'backgroundColor': 'black',
                   
                  
                       
                    }
                ),
            ],
            style={'width': '100%', 'display': 'flex', 'backgroundColor': '#1F2630', 'flex-direction': 'row', 'justify-content': 'space-around' ,'margin-top': '10px'}
        ),
    ],
    style={'backgroundColor': '#1F2630', 'width': '100%', 'height': '100%'}
)



if __name__ == "__main__":
    app.run_server(debug=True)
