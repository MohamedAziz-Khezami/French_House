# Libraries
import dash
import dash_bootstrap_components as dbc
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import pandas as pd
import json
import plotly.express as px
import requests


# App Config
app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.BOOTSTRAP,
    ],
)

server = app.server
app.title = "French House"


mapbox_access_token = "pk.eyJ1IjoiamFja3AiLCJhIjoidGpzN0lXVSJ9.7YK6eRwUNFwd3ODZff6JvA"


# Database connection
df = pd.read_csv("datasets/linechart.csv")
hbar = pd.read_csv("datasets/hbar.csv").iloc[:10, :]
histo = pd.read_csv("datasets/histogram.csv")


appartement_bar = pd.read_csv("datasets/appartement_bar.csv").sort_values(
    by="valeur_fonciere", ascending=True
)
appartement_line = pd.read_csv("datasets/appartement_line.csv")

commercial_bar = pd.read_csv("datasets/commercial_bar.csv").sort_values(
    by="valeur_fonciere", ascending=True
)
commercial_line = pd.read_csv("datasets/commercial_line.csv")

maison_bar = pd.read_csv("datasets/maison_bar.csv").sort_values(
    by="valeur_fonciere", ascending=True
)
maison_line = pd.read_csv("datasets/maison_line.csv")


# avg total price per month line chart
line_chart = {
    "data": [
        go.Scatter(
            x=df["date_mutation"],
            y=df["valeur_fonciere"],
            mode="lines",
            name="Valeur fonciere",
            yaxis="y1",  # Assign to the primary y-axis
        ),
        go.Scatter(
            x=df["date_mutation"],
            y=df["count"],
            mode="lines",
            name="Number of sales",
            yaxis="y2",  # Assign to the secondary y-axis
        ),
    ],
    "layout": go.Layout(
        title={
            "text": "Average total selling price and counts per month",
            "font": {"color": "white", "size": 50},  # Set title font color to white
        },
        paper_bgcolor="#1F2630",
        plot_bgcolor="#252E3F",
        xaxis=dict(
            title="Date mutation",
            titlefont=dict(color="white"),
            tickfont=dict(color="white"),
            gridcolor="#444",
            zerolinecolor="#444",
            zeroline=False,
        ),
        yaxis=dict(
            title="Valeur fonciere",
            titlefont=dict(color="white"),
            tickfont=dict(color="white"),
            gridcolor="#444",
            zerolinecolor="#444",
            zeroline=False,
        ),
        yaxis2=dict(
            title="Counts",
            titlefont=dict(color="white"),
            tickfont=dict(color="white"),
            gridcolor="#444",
            zerolinecolor="#444",
            zeroline=False,
            overlaying="y",  # Overlay on the same plot
            side="right",  # Place on the right side
        ),
    ),
}


# pie chart: effects on price
pie_chart = {
    "data": [
        go.Pie(
            labels=["Surface", "Location", "Rooms", "Type"],
            values=[0.39, 0.25, 0.08, 0.03],
            marker=dict(colors=["#252E3F", "#9ECAE1", "#252E3F", "#9ECAE1", "#252E3F"]),
        )
    ],
    "layout": go.Layout(
        title={
            "text": "The effects on price",
            "font": {"color": "white", "size": 40},  # Set title font color to white
        },
        paper_bgcolor="#1F2630",
        plot_bgcolor="#252E3F",
        showlegend=True,
        # margin={"r": 0, "t": 0, "l": 0, "b": 0},
    ),
}

# histogram: avg price per year
histogram = {
    "data": [
        go.Bar(
            x=histo["date_mutation"].astype(str),  # Each unique date
            y=histo["valeur_fonciere"],  # Corresponding value for each date
            marker=dict(
                color="#1f77b4",  # Customize bar color
                line=dict(color="white", width=1),
            ),
        )
    ],
    "layout": go.Layout(
        paper_bgcolor="#1F2630",
        plot_bgcolor="#252E3F",
        xaxis=dict(
            title="Date",
            titlefont=dict(color="white"),
            tickfont=dict(color="white"),
            gridcolor="#444",
            zerolinecolor="#444",
            zerolinewidth=1,
            zeroline=False,
        ),
        yaxis=dict(
            title="Valeur Foncière",
            titlefont=dict(color="white"),
            tickfont=dict(color="white"),
            gridcolor="#444",
            zerolinecolor="#444",
            zerolinewidth=1,
            zeroline=False,
        ),
        title={
            "text": "Average total selling price per year",
            "font": {"color": "white", "size": 40},  # Set title font color to white
        },
    ),
}


# The main app layout
app.layout = html.Div(
    children=[
        html.H1(
            "🇫🇷 French House",
            style={"color": "white", "fontSize": "50px", "fontWeight": "bolder"},
        ),
        html.P(
            "This project is for educational purpose only, the author is not responsible for any misuse or consequences of the information used. Enjoy :)",
            style={"color": "white"},
        ),
        html.Hr(),
        html.Div(
            children=[
                html.Div(
                    [
                        dcc.Graph(id="choropleth-map"),
                        dcc.RadioItems(
                            id="dropdown-commune",
                            options=[
                                {"label": "By Department", "value": "departement"},
                                {"label": "By Commune", "value": "commune"},
                                {"label": "Streets Map", "value": "street"},
                            ],
                            value="departement",
                        ),
                    ],
                    style={
                        "width": "100%",
                        "display": "inline-block",
                        "margin-left": "10px",
                        "color": "gray",
                    },
                ),
                html.Div(
                    children=[
                        html.P("Address: ", style={"color": "white", "left": "0px"}),
                        dcc.Input(
                            id="input-address",
                            type="text",
                            placeholder="Enter address...",
                            value="",
                            style={
                                "width": "70%",
                                "margin-bottom": "10px",
                            },
                        ),
                        html.P(
                            "Surface in m2: ", style={"color": "white", "left": "0px"}
                        ),
                        dcc.Input(
                            id="input-surface",
                            type="number",
                            placeholder="Enter house overall surface in m2...",
                            value="",
                            style={
                                "width": "70%",
                                "margin-bottom": "10px",
                            },
                        ),
                        html.P("Rooms: ", style={"color": "white"}),
                        dcc.Input(
                            id="input-rooms",
                            type="number",
                            placeholder="Enter rooms number...",
                            value="",
                            style={
                                "width": "70%",
                                "margin-bottom": "10px",
                            },
                        ),
                        html.P("Type: ", style={"color": "white"}),
                        dcc.Dropdown(
                            id="input-type",
                            placeholder="Select house type...",
                            options=[
                                {"label": "Maison", "value": 3},
                                {"label": "Dépendance", "value": 1},
                                {
                                    "label": "Local industriel. commercial ou assimilé",
                                    "value": 2,
                                },
                                {"label": "Appartement", "value": 0},
                            ],
                            # Default selected value
                            style={
                                "width": "70%",
                                "margin-bottom": "10px",
                            },
                        ),
                        dbc.Button(
                            "Predict",
                            id="button",
                            color="primary",
                            style={"width": "30%"},
                        ),
                        html.H3(id="prediction"),
                    ],
                    style={
                        "display": "flex",
                        "flexDirection": "column",
                        "alignItems": "",
                        "paddingTop": "20px",
                        "backgroundColor": "",
                        "width": "100%",
                        "paddingLeft": "10px",
                        "borderLeft": "solid gray 1px",
                        "marginLeft": "20px",
                        "height": "100%",
                        "justify-content": "space-evenly",
                        "flexWrap": "wrap",
                    },
                ),
            ],
            style={
                "width": "100%",
                "display": "flex",
                "height": "500px",
                "marginTop": "20px",
            },
        ),
        html.Hr(),
        html.Div(
            children=[
                dcc.Graph(
                    id="line-chart",
                    figure=line_chart,
                    config={"displayModeBar": "hover"},
                    animate=True,
                ),
            ],
            style={"width": "100%", "margin": "auto", "backgroundColor": ""},
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id="pie-chart",
                            figure=pie_chart,
                            config={"displayModeBar": "hover"},
                            animate=True,
                        ),
                    ],
                    style={
                        "width": "50%",
                        "borderLeft": "solide gray 3px",
                        "paddingLeft": "20px",
                    },
                ),
                html.Div(
                    children=[
                        #
                        dcc.Graph(
                            id="histogram",
                            figure=histogram,
                            config={"displayModeBar": "hover"},
                            animate=True,
                        ),
                    ],
                    style={"width": "50%"},
                ),
            ],
            style={
                "width": "100%",
                "display": "flex",
                "backgroundColor": "#1F2630",
                "flexWrap": "wrap",
                "margin": "auto",
            },
        ),
        html.Hr(),
        html.H2(
            "House prices evolution:",
            style={"color": "white", "fontSize": "40px", "fontWeight": "bold"},
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id="line-chart-houses",
                            figure={
                                "data": [
                                    go.Scatter(
                                        x=maison_line["date_mutation"],
                                        y=maison_line["valeur_fonciere"],
                                        mode="lines",
                                        name="Valeur fonciere",
                                        yaxis="y1",  # Assign to the primary y-axis
                                    ),
                                    go.Scatter(
                                        x=maison_line["date_mutation"],
                                        y=maison_line["count"],
                                        mode="lines",
                                        name="Number of sales",
                                        yaxis="y2",  # Assign to the secondary y-axis
                                    ),
                                ],
                                "layout": go.Layout(
                                    title={
                                        "text": "Average total selling price of houses per month",
                                        "font": {
                                            "color": "white",
                                            "size": 30,
                                        },  # Set title font color to white
                                    },
                                    paper_bgcolor="#1F2630",
                                    plot_bgcolor="#252E3F",
                                    xaxis=dict(
                                        title="Date mutation",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                    ),
                                    yaxis=dict(
                                        title="Valeur fonciere",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                    ),
                                    yaxis2=dict(
                                        title="Counts",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                        overlaying="y",  # Overlay on the same plot
                                        side="right",  # Place on the right side
                                    ),
                                    # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                ),
                            },
                            config={"displayModeBar": "hover"},
                            animate=True,
                        ),
                    ],
                    style={"width": "100%", "margin": "auto", "backgroundColor": ""},
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            figure={
                                "data": [
                                    go.Bar(
                                        x=maison_bar["valeur_fonciere"],
                                        y=maison_bar["departmentName"],
                                        orientation="h",
                                        marker=dict(
                                            color="rgb(158,202,225)",
                                            line=dict(color="rgb(8,48,107)", width=1.5),
                                        ),
                                    )
                                ],
                                "layout": go.Layout(
                                    title={
                                        "text": "Sorted communes by average selling house price",
                                        "font": {
                                            "color": "white",
                                            "size": 30,
                                        },  # Set title font color to white
                                    },
                                    paper_bgcolor="#1F2630",
                                    plot_bgcolor="#252E3F",
                                    xaxis=dict(
                                        title="Average Price",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zerolinewidth=1,
                                        zeroline=False,
                                    ),
                                    yaxis=dict(
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zerolinewidth=1,
                                        zeroline=False,
                                    ),
                                    # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                ),
                            },
                            config={"displayModeBar": "hover"},
                            animate=True,
                        ),
                    ],
                    style={"width": "50%"},
                ),
                html.Div(
                    children=[
                        html.Div(
                            [
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=4.2162,
                                                title={
                                                    "text": "Avg rooms",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " rooms",
                                                    "font": {
                                                        "color": "white"
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=103.5397,
                                                title={
                                                    "text": "Avg surface",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " m2",
                                                    "font": {
                                                        "color": "white"
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                            ],
                            style={
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=536591.523,
                                                title={
                                                    "text": "Avg Price",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " €",
                                                    "font": {
                                                        "color": "white"
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                            ],
                            style={
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "width": "50%",
                        "height": "100%",
                        "color": "white",
                    },
                ),
            ],
            style={
                "width": "90%",
                "display": "flex",
                "backgroundColor": "#1F2630",
                "flex-direction": "row",
                "justify-content": "",
                "align-items": "",
                "margin": "auto",
                "flexWrap": "wrap",
            },
        ),
        html.Hr(),
        html.H2(
            "Appartement prices evolution:",
            style={"color": "white", "fontSize": "40px", "fontWeight": "bold"},
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id="line-chart-appartements",
                            figure={
                                "data": [
                                    go.Scatter(
                                        x=appartement_line["date_mutation"],
                                        y=appartement_line["valeur_fonciere"],
                                        mode="lines",
                                        name="Valeur fonciere",
                                        yaxis="y1",  # Assign to the primary y-axis
                                    ),
                                    go.Scatter(
                                        x=appartement_line["date_mutation"],
                                        y=appartement_line["count"],
                                        mode="lines",
                                        name="Number of sales",
                                        yaxis="y2",  # Assign to the secondary y-axis
                                    ),
                                ],
                                "layout": go.Layout(
                                    title={
                                        "text": "Average total selling price of houses per month",
                                        "font": {
                                            "color": "white",
                                            "size": 40,
                                        },  # Set title font color to white
                                    },
                                    paper_bgcolor="#1F2630",
                                    plot_bgcolor="#252E3F",
                                    xaxis=dict(
                                        title="Date mutation",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                    ),
                                    yaxis=dict(
                                        title="Valeur fonciere",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                    ),
                                    yaxis2=dict(
                                        title="Counts",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                        overlaying="y",  # Overlay on the same plot
                                        side="right",  # Place on the right side
                                    ),
                                    # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                ),
                            },
                            config={"displayModeBar": "hover"},
                            animate=True,
                        ),
                    ],
                    style={"width": "100%", "margin": "auto", "backgroundColor": ""},
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            figure={
                                "data": [
                                    go.Bar(
                                        x=appartement_bar["valeur_fonciere"],
                                        y=appartement_bar["departmentName"],
                                        orientation="h",
                                        marker=dict(
                                            color="rgb(158,202,225)",
                                            line=dict(color="rgb(8,48,107)", width=1.5),
                                        ),
                                    )
                                ],
                                "layout": go.Layout(
                                    title={
                                        "text": "Average total selling price of appartements per department",
                                        "font": {
                                            "color": "white",
                                            "size": 30,
                                        },  # Set title font color to white
                                    },
                                    paper_bgcolor="#1F2630",
                                    plot_bgcolor="#252E3F",
                                    xaxis=dict(
                                        title="Average Price",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zerolinewidth=1,
                                        zeroline=False,
                                    ),
                                    yaxis=dict(
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zerolinewidth=1,
                                        zeroline=False,
                                    ),
                                    # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                ),
                            },
                            config={"displayModeBar": "hover"},
                            animate=True,
                        ),
                    ],
                    style={"width": "50%"},
                ),
                html.Div(
                    children=[
                        html.Div(
                            [
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=2.577,
                                                title={
                                                    "text": "Avg rooms",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " rooms",
                                                    "font": {
                                                        "color": "white"
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=56.5999,
                                                title={
                                                    "text": "Avg surface",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " m2",
                                                    "font": {
                                                        "color": "white"
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                            ],
                            style={
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=3740522.1062,
                                                title={
                                                    "text": "Avg Price",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " €",
                                                    "font": {
                                                        "color": "white",
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                            ],
                            style={
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "width": "50%",
                        "height": "100%",
                        "color": "white",
                    },
                ),
            ],
            style={
                "width": "90%",
                "display": "flex",
                "backgroundColor": "#1F2630",
                "flex-direction": "row",
                "justify-content": "",
                "align-items": "",
                "margin": "auto",
                "flexWrap": "wrap",
            },
        ),
        html.Hr(),
        html.H2(
            "Commercial lots prices evolution:",
            style={"color": "white", "fontSize": "40px", "fontWeight": "bold"},
        ),
        html.Div(
            children=[
                html.Div(
                    children=[
                        dcc.Graph(
                            id="line-chart-commercials",
                            figure={
                                "data": [
                                    go.Scatter(
                                        x=commercial_line["date_mutation"],
                                        y=commercial_line["valeur_fonciere"],
                                        mode="lines",
                                        name="Valeur fonciere",
                                    ),
                                    go.Scatter(
                                        x=appartement_line["date_mutation"],
                                        y=appartement_line["count"],
                                        mode="lines",
                                        name="Number of sales",
                                        yaxis="y2",  # Assign to the secondary y-axis
                                    ),
                                ],
                                "layout": go.Layout(
                                    title={
                                        "text": "Average total selling price of houses per month",
                                        "font": {
                                            "color": "white",
                                            "size": 40,
                                        },  # Set title font color to white
                                    },
                                    paper_bgcolor="#1F2630",
                                    plot_bgcolor="#252E3F",
                                    xaxis=dict(
                                        title="Date mutation",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                    ),
                                    yaxis=dict(
                                        title="Valeur fonciere",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                    ),
                                    yaxis2=dict(
                                        title="Counts",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zeroline=False,
                                        overlaying="y",  # Overlay on the same plot
                                        side="right",  # Place on the right side
                                    ),
                                    # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                ),
                            },
                            config={"displayModeBar": "hover"},
                            animate=True,
                        )
                    ],
                    style={"width": "100%", "margin": "auto", "backgroundColor": ""},
                ),
                html.Div(
                    children=[
                        dcc.Graph(
                            figure={
                                "data": [
                                    go.Bar(
                                        x=commercial_bar["valeur_fonciere"],
                                        y=commercial_bar["departmentName"],
                                        orientation="h",
                                        marker=dict(
                                            color="rgb(158,202,225)",
                                            line=dict(color="rgb(8,48,107)", width=1.5),
                                        ),
                                    )
                                ],
                                "layout": go.Layout(
                                    title={
                                        "text": "Sorted communes by average selling commercial lot price",
                                        "font": {
                                            "color": "white",
                                            "size": 30,
                                        },  # Set title font color to white
                                    },
                                    paper_bgcolor="#1F2630",
                                    plot_bgcolor="#252E3F",
                                    xaxis=dict(
                                        title="Average Price",
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zerolinewidth=1,
                                        zeroline=False,
                                    ),
                                    yaxis=dict(
                                        titlefont=dict(color="white"),
                                        tickfont=dict(color="white"),
                                        gridcolor="#444",
                                        zerolinecolor="#444",
                                        zerolinewidth=1,
                                        zeroline=False,
                                    ),
                                    # margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                ),
                            },
                            config={"displayModeBar": "hover"},
                            animate=True,
                        ),
                    ],
                    style={"width": "50%"},
                ),
                html.Div(
                    children=[
                        html.Div(
                            [
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=0.0,
                                                title={
                                                    "text": "Avg rooms",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },  # Change title color to white
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " rooms",
                                                    "font": {
                                                        "color": "white"
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=464.4628,
                                                title={
                                                    "text": "Avg surface",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " m2",
                                                    "font": {
                                                        "color": "white"
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                            ],
                            style={
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                            },
                        ),
                        html.Div(
                            [
                                dcc.Graph(
                                    figure={
                                        "data": [
                                            go.Indicator(
                                                mode="number",
                                                value=2273000.7829,
                                                title={
                                                    "text": "Avg Price",
                                                    "font": {
                                                        "color": "white",
                                                        "size": 30,
                                                    },
                                                },
                                                number={
                                                    "valueformat": ".0f",
                                                    "suffix": " €",
                                                    "font": {
                                                        "color": "white"
                                                    },  # Change number color to white
                                                },
                                            )
                                        ],
                                        "layout": go.Layout(
                                            margin={"r": 0, "t": 0, "l": 0, "b": 0},
                                            paper_bgcolor="#1F2630",
                                            plot_bgcolor="#252E3F",
                                            width=200,
                                            height=200,
                                        ),
                                    },
                                    config={"displayModeBar": "hover"},
                                    animate=True,
                                ),
                            ],
                            style={
                                "display": "block",
                                "marginLeft": "auto",
                                "marginRight": "auto",
                            },
                        ),
                    ],
                    style={
                        "display": "flex",
                        "flex-direction": "column",
                        "width": "50%",
                        "height": "100%",
                        "color": "white",
                    },
                ),
            ],
            style={
                "width": "90%",
                "display": "flex",
                "backgroundColor": "#1F2630",
                "flex-direction": "row",
                "justify-content": "",
                "align-items": "",
                "margin": "auto",
                "flexWrap": "wrap",
            },
        ),
        html.Hr(),
        html.P("Data source: data.gouv.fr", style={"color": "white"}),
    ],
    style={
        "backgroundColor": "#1F2630",
        "width": "100%",
        "height": "100%",
        "padding": "20px",
    },
)

# External CSS for responsiveness
app.css.append_css(
    {
        "external_url": "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css",
        "url": "style.css",
    }
)


# Callback functions


def get_coordinates_with_requests(address):
    """Get longitude and latitude for a given address using requests."""
    base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
    # Construct the API URL
    url = f"{base_url}/{address}.json"
    params = {
        "access_token": mapbox_access_token,
        "limit": 1,  # Get only the most relevant result
    }

    # Make the API request
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()
        features = data.get("features", [])
        if features:
            # Extract longitude and latitude
            coordinates = features[0]["geometry"]["coordinates"]  # [lon, lat]
            return {"lon": coordinates[0], "lat": coordinates[1]}
        else:
            print("No results found for the given address.")
    else:
        print(f"Error: {response.status_code}, Message: {response.text}")
    return None


@app.callback(
    Output("prediction", "children"),
    [
        Input("input-address", "value"),
        Input("input-surface", "value"),
        Input("input-rooms", "value"),
        Input("input-type", "value"),
        Input("button", "n_clicks"),
    ],
)
def predict(address, surface, rooms, type, n_clicks):

    if n_clicks:
        if address == "" or surface == "" or rooms == "" or type == "":
            return "Please fill all the fields"
        else:
            place = get_coordinates_with_requests(address)
            print(place)

            from joblib import load

            model = load("model/lgbm_model_250_mse.pkl")

            to_pred = [place["lon"], place["lat"], type, rooms, surface]

            df_pred = pd.DataFrame(
                [to_pred],
                columns=[
                    "longitude",
                    "latitude",
                    "type_local",
                    "nombre_pieces_principales",
                    "surface",
                ],
            )
            print(df_pred)

            prediction = model.predict(df_pred)

            return "The predicted price is : " + str(int(prediction)) + " €"


@app.callback(
    Output("choropleth-map", "figure"),
    Input("dropdown-commune", "value"),
)
def update_chloropleth_map(selected_commune):
    if selected_commune == "commune":
        mb = pd.read_csv("datasets/df_t_comm.csv")
        with open("datasets/communes.geojson") as f:
            geojson_data = json.load(f)
        locations = "code"
        hover_name = "nom_commune"
        zoom = 6
        mapbox_style = "carto-darkmatter"
        opacity = 1
        center = {"lat": 46.2276, "lon": 2.2137}

    elif selected_commune == "departement":
        mb = pd.read_csv("datasets/mapy.csv")
        with open("datasets/geojsfile.json") as f:
            geojson_data = json.load(f)

        locations = "code_departement"
        hover_name = "departmentName"
        zoom = 4.5
        mapbox_style = "carto-darkmatter"
        opacity = 1
        center = {"lat": 46.2276, "lon": 2.2137}

    elif selected_commune == "street":
        mb = pd.read_csv("datasets/mapy.csv")
        with open("datasets/geojsfile.json") as f:
            geojson_data = json.load(f)

        locations = "code_departement"
        hover_name = None
        zoom = 9
        mapbox_style = "open-street-map"
        opacity = 0
        center = {"lat": 48.8575, "lon": 2.3514}
        locations = None

    # Loading the geojson file

    # Choropleth map
    figg = px.choropleth_mapbox(
        mb,
        geojson=geojson_data,
        featureidkey="properties.code",
        locations=locations,  # Column with ISO country codes
        color="valeur_fonciere",  # Column to color by
        hover_name=hover_name,
        mapbox_style=mapbox_style,  # Map style
        center=center,  # Map center
        zoom=zoom,
        color_continuous_scale="dense",
        template="plotly_dark",
        opacity=opacity,
    )
    figg.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_showscale=False,
        paper_bgcolor="#1F2630",
        plot_bgcolor="#252E3F",
    )

    return figg


# App running
if __name__ == "__main__":
    app.run_server(debug=False, port=8050)
