
import gpxpy.gpx
import pandas as pd
import numpy
from datetime import datetime
import gmplot
import dash
import plotly.express as px
import os
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

gpx_file = open('data/Chillllll.gpx', 'r')
filename = os.path.splitext("Chillllll.gpx")[0]
gpx = gpxpy.parse(gpx_file)

data = gpx.tracks[0].segments[0].points

waypoint_df = pd.DataFrame(columns = ["Longitude", "Latitude", "Elevation", "Time", "Speed m/s"])

for num, point in enumerate(data):
    waypoint_df = waypoint_df.append({"Longitude" : point.longitude,
                                    "Latitude" : point.latitude,
                                    "Elevation" : point.elevation,
                                    "Time" : point.time.time(),
                                     "Speed m/s" : point.speed_between(data[num - 1] )},
                                     ignore_index = True)

px.set_mapbox_access_token(open(".mapbox_token.txt").read())

fig_run = px.scatter_mapbox(waypoint_df,
                            lat = "Latitude",
                            lon = "Longitude",
                            color = "Speed m/s",
                            color_continuous_scale = px.colors.sequential.Turbo,
                           zoom = 13)

app.layout = html.Div(children=[
    html.H1('Run run run'),
    html.H3(children = """Speed as colors"""),
    dcc.Graph(id = "run track",
              figure = fig_run,
              style = {"height" : "80vh"})])




if __name__ == '__main__':
    app.run_server(debug=True)