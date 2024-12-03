import dash
import dash_leaflet as dl
import json

from dash import Input, Output, html

# Initialize the Dash app
app = dash.Dash(__name__)

# Load your GeoJSON file (replace with your file path)
with open('database/geofrance.json') as f:
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
            # Event handler for hover
            on_hover={'target': 'geojson', 'action': 'hover'}
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
