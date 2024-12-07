'''
import dash
import dash_leaflet as dl
import json

from dash import Input, Output, html

# Initialize the Dash app
app = dash.Dash(__name__)

# Load your GeoJSON file (replace with your file path)
with open('geofrance.json') as f:
    geojson_data = json.load(f)

# Layout with a map and GeoJSON layer
app.layout = html.Div([
    dl.Map(center=[48.8575, 2.3514], zoom=6, children=[
        # Using CartoDB positron (a light background)
        dl.TileLayer(url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}.png"),
        dl.GeoJSON(
            id="geojson",
            data=geojson_data,
            hoverStyle={'fillColor': 'yellow', 'weight': 3},  # Highlight feature on hover
        ),
    ], style={'width': '70%', 'height': '800px'}),
    html.Div(id="hover-output")  # To display the feature properties on hover
])

# Callback to display information about the feature on hover
@app.callback(
    Output('hover-output', 'children'),
    Input('geojson', 'hoverData')
)
def display_hover_info(hoverData):
    if hoverData:
        # Extract feature information (e.g., name or properties)
        feature_properties = hoverData['features'][0]['properties']
        return f"Hovered over: {json.dumps(feature_properties, indent=2)}"
    return "Hover over a feature to see details."

if __name__ == '__main__':
    app.run_server(debug=True)




import pickle as pkl
import pandas as pd
with open('lgbm_model_250_mse.pkl', 'rb') as f:
    model = pkl.load(f)



df_pred = pd.DataFrame([["2.0", "2.0", "2.0", "2.0", "2.0"]], columns=['longitude', 'latitude', 'type_local', 'nombre_pieces_principales', 'surface'])


print(model.predict(df_pred))

'''



import os
import pickle

scores = {} # scores is an empty dict already
target = '/Users/mak/Desktop/French_House/lgbm_model_250_mse.pkl'
if os.path.getsize(target) > 0:      
    with open(target, "rb") as f:
        unpickler = pickle.Unpickler(f)
        # if file is not empty scores will be equal
        # to the value unpickled
        scores = unpickler.load()
        
        
print(scores)