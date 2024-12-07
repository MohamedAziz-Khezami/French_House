# Libraries
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import json
import plotly.express as px
import geopandas as gpd
import requests






# App Config
app = dash.Dash(
    __name__,
    meta_tags=[{"name": "viewport", "content": "width=device-width, initial-scale=1.0"}],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
)

server = app.server
app.title = "French House"


mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"





# Database connection
df = pd.read_csv('linechart.csv')
hbar = pd.read_csv('hbar.csv').iloc[:10, :]
histo = pd.read_csv('histogram.csv')


mb = pd.read_csv('mapy.csv')

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
            zerolinewidth=500,
            zeroline=False,)
        ,
        yaxis=dict(
            title='Valeur fonciere',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=500,
            zeroline=False,
        ),
        
    #margin={"r": 0, "t": 0, "l": 0, "b": 0},

    )
}

# pie chart: effects on price
pie_chart = {
    'data': [
        go.Pie(
            labels=['Surface', 'Location', 'Rooms', 'Type'],
            values=[0.39, 0.25, 0.08,0.03],
            marker=dict(colors=['#252E3F', '#9ECAE1', '#252E3F', '#9ECAE1', '#252E3F']),
        )
    ],
    'layout': go.Layout(
        title='Pie Chart',
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        showlegend=True,
        #margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
}

# horizontal bar chart most expensive cities
horizontal_bar_chart = {
    'data': [
        go.Bar(
            x=hbar['valeur_fonciere'],
            y=hbar['departmentName'] ,
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
            title='Average Price',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=False,
        ),
        yaxis=dict(
     
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=False,
        ),
       #margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
}

# histogram: avg price per year
histogram = {
    'data': [
        go.Histogram(
            x=histo['date_mutation'],
            y=histo['valeur_fonciere'],
        )
    ],
    'layout': go.Layout(
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        xaxis=dict(
            title='Year',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=False,)
        ,
        yaxis=dict(
            title='Average Price/Year',
            titlefont=dict(color='white'),
            tickfont=dict(color='white'),
            gridcolor='#444',
            zerolinecolor='#444',
            zerolinewidth=1,
            zeroline=False,
        ),
        title='Histogram',
        
    
    )
}

# cards: avg rooms, avg surface, avg price, house type,...
cards_rooms = {
    'data': [
        go.Indicator(
            mode="number",
            value=5,
            title={"text": "Avg rooms"},
            number={"valueformat": ".0f", "suffix": " rooms"},
        )
    ],
    'layout': go.Layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        width=200,
        height=200,
        
    ),

}

cards_surface = {
    'data': [
        go.Indicator(
            mode="number",
            value=5,
            title={"text": "Avg rooms"},
            number={"valueformat": ".0f", "suffix": " rooms"},
        )
    ],
    'layout': go.Layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        width=200,
        height=200,
        
    ),

}

cards_type = {
    'data': [
        go.Indicator(
            mode="number",
            value=5,
            title={"text": "Avg rooms"},
            number={"valueformat": ".0f", "suffix": " rooms"},
        )
    ],
    'layout': go.Layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        width=200,
        height=200,
        
    ),

}

cards_avgPrice = {
    'data': [
        go.Indicator(
            mode="number",
            value=5,
            title={"text": "Avg rooms"},
            number={"valueformat": ".0f", "suffix": " rooms"},
        )
    ],
    'layout': go.Layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        paper_bgcolor='#1F2630',
        plot_bgcolor='#252E3F',
        width=200,
        height=200,
        
    ),

}

# Loading the geojson file
with open("geojsfile.json") as f:
    geojson = json.load(f)

# Choropleth map
figg = px.choropleth_mapbox(
    mb,
    geojson=geojson,
    featureidkey='properties.code',
    locations="code_departement",   # Column with ISO country codes
    color="valeur_fonciere",          # Column to color by
    hover_name="valeur_fonciere",   # Information shown on hover
    mapbox_style="carto-darkmatter",  # Map style
    center={"lat": 46.2276, "lon": 2.2137},   # Map center
    zoom=4.2,
    color_continuous_scale='dense'
)
figg.update_layout(margin={"r":0,"t":0,"l":0,"b":0}, coloraxis_showscale=False)

# The main app layout
app.layout = html.Div(
  
    children=[
        
        html.H1(
            'French House',
            style = {'color': 'white'}
        ),
        html.P(
            'This project is for educational purpose only, the author is not responsible for any misuse or consequences of the information used. Enjoy :)',
            style = {'color': 'white'}
        ),
        
        html.Hr(),
        
        html.Div(
            children=[
                html.Div(
                  dcc.Graph(figure=figg),  
                ),
html.Div(
    children=[
                html.P("Address: ", style = {'color': 'white', 'left': '0px'}),
                dcc.Input(id='input-address', type='text', placeholder = 'Enter address...', style={'width': '70%', 'margin-bottom': '10px',}),
                html.P("Surface in m2: ", style = {'color': 'white', 'left': '0px'}),
                dcc.Input(id='input-surface', type='number', placeholder = 'Enter house overall surface in m2...', style={'width': '70%', 'margin-bottom': '10px',}),
                
                html.P("Rooms: ", style = {'color': 'white'}),
                dcc.Input(id='input-rooms', type='number',placeholder = 'Enter rooms number...', style={'width': '70%', 'margin-bottom': '10px', }),
                
                html.P("Type: ", style ={'color': 'white'}),
                dcc.Dropdown(
                    id='input-type',
                    placeholder = 'Select house type...',
                    options=[
                        {'label': 'Maison', 'value': 'Maison'},
                        {'label': 'Dépendance', 'value': 'Dépendance'},
                        {'label': 'Local industriel. commercial ou assimilé', 'value': 'Local industriel. commercial ou assimilé'},
                        {'label': 'Appartement', 'value': 'Appartement'},
                    
                    ],
                      # Default selected value
                    style={'width': '70%', 'margin-bottom': '10px', }
                ),
                
                dbc.Button("Predict", id ='button',color="primary", style={'width': '30%'}),
                
                html.H3(id='prediction')
                
                
            ],
     

    style={'display': 'flex', 'flexDirection': 'column', 'alignItems': '', 'paddingTop': '20px',  'backgroundColor': '', 'width':'100%', 'paddingLeft': '10px', 'borderLeft': 'solid gray 1px', 'marginLeft':'20px' , 'height': '90%' }
)


            ],
            style={
                'width': '100%',
                'display': 'flex',
                'height': '500px',
                'marginTop': '20px'
            }
        ),
        html.Hr(),
        html.Div(
            children=[
                dcc.Graph(id="line-chart", figure=line_chart, config={"displayModeBar": 'hover'}, animate=True),
            ],
            style={'width': '100%', 'margin': 'auto', 'backgroundColor': ''}
        ),
                html.Hr(),

        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(id="pie-chart", figure=pie_chart, config={"displayModeBar": 'hover'}, animate=True),
                    ],
                    style={'width': '50%', 'borderLeft': 'solide gray 3px', 'paddingLeft': '20px'}
                ),
                html.Div(
                    children=[
                        dcc.Graph(id="bar-chart", figure=horizontal_bar_chart, config={"displayModeBar": 'hover'}, animate=True),
                    ],
                    style={'width': '50%'}
                ),
            ],
            style={'width': '100%', 'display': 'flex', 'backgroundColor': '#1F2630', 'flexWrap': 'wrap', 'margin': 'auto'}
        ),
        
                html.Hr(),

        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(id="histogram", figure=histogram, config={"displayModeBar": 'hover'}, animate=True),
                    ],
                     style={'width': '100%'},
                 
              
                ),
                
                            html.Div(
                    children=[

                            html.Div(
                                [
                        dcc.Graph(figure=cards_avgPrice, config={"displayModeBar": 'hover'}, animate=True),
                        dcc.Graph(figure=cards_type, config={"displayModeBar": 'hover'}, animate=True),

                                ],
                                style = {'display': 'block', 'marginLeft' : 'auto', 'marginRight': 'auto', 'backgroundColor': 'red'}
                                
                            ),
                            
                            
                            
                            html.Div(
                                
                                [
                        dcc.Graph(figure=cards_surface, config={"displayModeBar": 'hover'}, animate=True),
                        dcc.Graph(figure=cards_rooms, config={"displayModeBar": 'hover'}, animate=True),
                                    
                                ],
                                  style = {'display': 'block', 'marginLeft' : 'auto', 'marginRight': 'auto', 'backgroundColor': 'red'}
                                
                            ),
                            
                            
                    ],
                    style={
                         "display": "grid",
                        "gridTemplateColumns": "repeat(2, 1fr)",
                        'width': '100%',
                        'margin': 'auto',
                        'color': 'white'
                 
                    },
                ),
  
            ],
            style={'width': '100%', 'display': 'flex', 'backgroundColor': '#1F2630', 'flex-direction': 'row', 'justify-content': 'center', 'align-items': 'center', 'margin': 'auto'},
        
        ),

    ],
    style={'backgroundColor': '#1F2630', 'width': '100%', 'height': '100%', 'padding': '20px'}
)

# External CSS for responsiveness
app.css.append_css({
    'external_url': 'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css',
    'url': 'style.css'
})


#Callback functions

def get_coordinates_with_requests(address):
    """Get longitude and latitude for a given address using requests."""
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    # Construct the API URL
    url = f"{base_url}/{address}.json"
    params = {
        "access_token": mapbox_access_token,
        "limit": 1  # Get only the most relevant result
    }
    
    # Make the API request
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        data = response.json()
        features = data.get('features', [])
        if features:
            # Extract longitude and latitude
            coordinates = features[0]['geometry']['coordinates']  # [lon, lat]
            return {'lon': coordinates[0], 'lat': coordinates[1]}
        else:
            print("No results found for the given address.")
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
    return None


@app.callback(
		Output('prediction', 'children'),
		[Input('input-address', 'value'),
      Input('input-surface', 'value'),
		Input('input-rooms', 'value'),
		Input('input-type', 'value'),
    Input('button', 'n_clicks')
  ],
)



def predict(address, surface, rooms, type, n_clicks):
    
    if n_clicks:
    
    
            place = get_coordinates_with_requests(address)
        
            from joblib import load
            model = load('/Users/mak/Desktop/French_House/lgbm_model_250_mse (1).pkl')
            
            to_pred = [place['lon'], place['lat'], type, rooms, surface]
            
            df_pred = pd.DataFrame([to_pred], columns=['longitude', 'latitude', 'type_local', 'nombre_pieces_principales', 'surface'])
            print(df_pred)
            
            
            prediction = model.predict(df_pred)
            
            print(prediction)
            




# App running
if __name__ == '__main__':
    app.run_server(debug=True)
