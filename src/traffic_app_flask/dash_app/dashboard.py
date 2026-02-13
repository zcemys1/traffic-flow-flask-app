import pandas as pd
import plotly.express as px
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
from pathlib import Path
import os

assets_path = os.path.join(
    os.getcwd(), "src", "traffic_app_flask", "dash_app", "assets"
)


# REMOVED DASH CODE BELOW
# app = Dash(__name__, external_stylesheets=external_stylesheets, meta_tags=meta_tags)
def init_dash(flask_app):
    dash_app = Dash(
        server=flask_app,
        url_base_pathname="/dash_app/",
        external_stylesheets=[dbc.themes.SOLAR],
        assets_folder=assets_path,
        suppress_callback_exceptions=True,
    )

    # Load file
    file_path = Path(__file__).parent / "traffic-flow-borough_dash.xlsx"
    # file_path = r"C:\Users\uswe\OneDrive - University College London\Desktop\COMP0034 T2 2025\comp0034-cw2-zcemys1\src\traffic_app_flask\dash_app\traffic-flow-borough_dash.xlsx"
    df_cars = pd.read_excel(
        file_path, sheet_name="Traffic Flows Cars", engine="openpyxl"
    )
    df_vehicles = pd.read_excel(
        file_path, sheet_name="Traffic Flows All vehicles", engine="openpyxl"
    )
    # Select Boroughs Within London
    df_cars = df_cars[df_cars["LA Code"].astype(str).str.startswith("E09")]
    df_vehicles = df_vehicles[df_vehicles["LA Code"].astype(str).str.startswith("E09")]

    # Clean Data for visuals
    df_cars_melted = df_cars.melt(
        id_vars=["LA Code", "Local Authority"],
        var_name="Year",
        value_name="Traffic Flow",
    )
    df_vehicles_melted = df_vehicles.melt(
        id_vars=["LA Code", "Local Authority"],
        var_name="Year",
        value_name="Traffic Flow",
    )

    # Convert the Year column to integer
    df_cars_melted["Year"] = df_cars_melted["Year"].astype(int)
    df_vehicles_melted["Year"] = df_vehicles_melted["Year"].astype(int)

    # Split data for ULEZ analysis
    df_cars_before_ulez = df_cars_melted[df_cars_melted["Year"] < 2019]
    df_cars_within_ulez = df_cars_melted[df_cars_melted["Year"] >= 2019]

    df_vehicles_before_ulez = df_vehicles_melted[df_vehicles_melted["Year"] < 2019]
    df_vehicles_within_ulez = df_vehicles_melted[df_vehicles_melted["Year"] >= 2019]

    external_stylesheets = [
        dbc.themes.SOLAR
    ]  # modify last section for different themes

    # Function to generate a line chart
    def generate_chart(df, title):
        fig = px.line(
            df, x="Year", y="Traffic Flow", color="Local Authority", title=title
        )
        return fig

    # APP LAYOUT!!!!!!! Wrap the layout in a Bootstrap container
    dash_app.layout = dbc.Container(
        [  # Opening Container
            # Add the HTML layout components in here
            # Title
            html.H1(
                "How affective is the Ultra Low Emission Zone?",
                className="text-center mt-4 mb-4",
            ),  # Title with center alignment and margin
            # Text body 1
            dbc.Container(
                [  # Container for the body content
                    html.H3("What is ULEZ?", className="mt-4"),
                    html.P(
                        """The Ultra Low Emission Zone is a zone that covers the London boroughs in an attempt to increase air quality and tackle climate change. 
                It is a zone that targets motor vehicles that have to meet the required emissions standard in order to be compliant. 
                If you are exempt, you avoid having to pay the daily fee of £12.50. The government implemented the scheme in 2019.""",
                        className="lead",
                    ),
                    # Back to home button
                    html.A(
                        html.Button(
                            "Back to Home",
                            className="btn btn-primary mt-4",
                            id="back-home-btn",
                        ),
                        href="/",  # Back to home page
                    ),
                ],
                fluid=True,
            ),
            html.Hr(),  # Horizontal rule (line separator)
            # First Image (ULEZ Zone)
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=dash_app.get_asset_url("ulez-zone.png"),
                            className="img-fluid",
                        ),
                        width=12,
                        className="text-center",
                    )
                ],
                className="mb-4",
            ),
            # Text body 2
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    html.H3(
                                        "What is the impact of the ULEZ zone?",
                                        className="mt-4",
                                    ),
                                    html.P(
                                        """Figures show that the emissions restrictions have contributed to the decrease in toxic gas pollution. 
                        It is seen that within Central London, there has been a 53% decrease in nitrogen dioxide levels since the start of ULEZ. 
                        We can also see the increase in vehicle emissions compliance, which has contributed to decreasing pollution 
                        and also increasing activity within the car sector.""",
                                        className="lead",
                                    ),
                                ],
                                className="d-flex flex-column justify-content-center h-100",
                            )
                        ],
                        width=6,
                        className="d-flex align-items-center",
                    ),
                    dbc.Col(
                        [
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(
                                            src=dash_app.get_asset_url(
                                                "air-quality.png"
                                            ),
                                            className="img-fluid",
                                        ),
                                        width=12,
                                    ),
                                ],
                                className="mb-2",
                            ),  # First Image
                            dbc.Row(
                                [
                                    dbc.Col(
                                        html.Img(
                                            src=dash_app.get_asset_url(
                                                "car-compliancy.png"
                                            ),
                                            className="img-fluid",
                                        ),
                                        width=12,
                                    ),
                                ]
                            ),  # Second Image
                        ],
                        width=6,
                    ),
                ],
                className="mb-4 align-items-center",
            ),
            # Graphs from Traffic Flow data
            dbc.Row(
                [
                    # Left: Cars Graph
                    dbc.Col(
                        [
                            html.H3("Traffic Flow of Cars"),
                            dcc.Dropdown(
                                id="cars-dropdown",
                                options=[
                                    {
                                        "label": "Cars Before ULEZ (Pre-2019)",
                                        "value": "before",
                                    },
                                    {
                                        "label": "Cars Within ULEZ (2019+)",
                                        "value": "within",
                                    },
                                ],
                                value="before",
                                className="mb-2",
                            ),
                            dcc.Graph(id="cars-graph"),
                        ],
                        width=6,
                    ),
                    # Right: Vehicles Graph
                    dbc.Col(
                        [
                            html.H3("Traffic Flow of All Vehicles"),
                            dcc.Dropdown(
                                id="vehicles-dropdown",
                                options=[
                                    {
                                        "label": "Vehicles Before ULEZ (Pre-2019)",
                                        "value": "before",
                                    },
                                    {
                                        "label": "Vehicles Within ULEZ (2019+)",
                                        "value": "within",
                                    },
                                ],
                                value="before",
                                className="mb-2",
                            ),
                            dcc.Graph(id="vehicles-graph"),
                        ],
                        width=6,
                    ),
                ],
                className="mb-4",
            ),
            # Text body 3
            dbc.Row(
                [
                    dbc.Col(
                        [
                            html.H3(
                                "What are the prospects for the ULEZ scheme?",
                                className="mt-4",
                            ),
                            html.P(
                                """The Ultra Low Emission Zone has expanded over time to cover a larger area. 
                    Initially, it covered only Central London, but in October 2021, it expanded to cover 
                    the area within the North and South Circular Roads. In 2023, the scheme was further expanded 
                    to include all London boroughs. This expansion aims to further reduce air pollution and encourage 
                    more people to switch to cleaner, low-emission vehicles.""",
                                className="lead",
                            ),
                        ],
                        width=12,
                    )  # Full-width text section
                ],
                className="mb-4",
            ),
            # Final Image (ULEZ Expansion)
            dbc.Row(
                [
                    dbc.Col(
                        html.Img(
                            src=dash_app.get_asset_url("ulez-expansion.png"),
                            className="img-fluid",
                        ),
                        width=12,
                        className="text-center",
                    )
                ],
                className="mb-4",
            ),
        ],
        fluid=True,
    )  # Closing for dbc.Container

    # Callbacks to update graphs based on dropdown selection
    @dash_app.callback(Output("cars-graph", "figure"), Input("cars-dropdown", "value"))
    def update_cars_graph(selected_option):
        if selected_option == "before":
            return generate_chart(df_cars_before_ulez, "Cars Before ULEZ (Pre-2019)")
        return generate_chart(df_cars_within_ulez, "Cars Within ULEZ (2019+)")

    @dash_app.callback(
        Output("vehicles-graph", "figure"), Input("vehicles-dropdown", "value")
    )
    def update_vehicles_graph(selected_option):
        if selected_option == "before":
            return generate_chart(
                df_vehicles_before_ulez, "Vehicles Before ULEZ (Pre-2019)"
            )
        return generate_chart(df_vehicles_within_ulez, "Vehicles Within ULEZ (2019+)")

    return dash_app  # Return the Dash app (but do NOT run it here!)
