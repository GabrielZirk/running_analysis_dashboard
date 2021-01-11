import pandas as pd
import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import plotly.graph_objects as go
import dash_bootstrap_components as dbc
from plotly.subplots import make_subplots

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.SUPERHERO])

server = app.server

track_df = pd.read_csv("data/myWorkouts-2021-01-08_15-49.csv", sep = "\t") # import tab-separated csv file
track_df.drop(["CADENCE", "SPEED_SENSOR", "PRESSURE", "TEMPERATURE", "ALTITUDE_BARO", "DISTANCE_SENSOR"], axis = 1, inplace = True) # elminiate unnecessary columns

# add dot "." into latitude and longitude string
track_df["LATITUDE_6"] = track_df["LATITUDE_6"].astype(str)
track_df["LATITUDE_6"] = track_df["LATITUDE_6"].apply(lambda x: x[0:2] + "." + x[2:8])
track_df["LONGITUDE_6"] = track_df["LONGITUDE_6"].astype(str)
track_df["LONGITUDE_6"] = track_df["LONGITUDE_6"].apply(lambda x: x[0:2] + "." + x[2:8])

# convert longitude and latitude to float
track_df["LONGITUDE_6"] = track_df["LONGITUDE_6"].astype(float)
track_df["LATITUDE_6"] = track_df["LATITUDE_6"].astype(float)

# define variables
long = track_df["LONGITUDE_6"]
lat = track_df["LATITUDE_6"]
hr = track_df["HEART_RATE"]
slope = track_df["SLOPE_SMOOTHED"]
altitude  = track_df["ALTITUDE_SMOOTHED"]
speed = track_df["SPEED_SMOOTHED"]
distance = track_df["DISTANCE_GPS"]

# define mapbox token for scatter mapbox plot
px.set_mapbox_access_token(open(".mapbox_token.txt").read())

track_fig1 = px.scatter_3d(track_df,
                           x = long,
                           y = lat,
                           z = altitude,
                           color = hr,
                           color_continuous_scale = px.colors.cyclical.IceFire)

track_fig1.update_layout(legend_title_text= "Heart Rate",
                         scene = dict(
    xaxis_title = "Longitude",
    yaxis_title = "Latitude",
    zaxis_title = "Altitude"),
                        margin = dict(r = 20,
                                     b = 10,
                                     l = 10,
                                     t= 10),
coloraxis_colorbar = dict(title = "Heart Rate (bpm)",
                          lenmode="pixels",
                          len=300),
font_color = "white",
                         paper_bgcolor = "rgba(0, 0, 0, 0)",
                         plot_bgcolor = "rgba(0, 0, 0, 0)"
)



track_fig2 = px.scatter_mapbox(track_df,
                               lat = lat,
                               lon = long,
                               color = speed,
                               color_continuous_scale = px.colors.cyclical.IceFire,
                               size_max = 13,
                               zoom = 12)
track_fig2.update_layout(coloraxis_colorbar = dict(title = "Speed (m/s)",
                                                   lenmode = "pixels",
                                                   len = 300),
                         font_color = "white",
                         paper_bgcolor="rgba(0, 0, 0, 0)",
                         plot_bgcolor="rgba(0, 0, 0, 0)"
                         )

correlation_hr_slope = hr.corr(slope)
correlation_speed_slope = speed.corr(slope)

corr_hr_slope_scatter = go.Figure()
corr_hr_slope_scatter.add_trace(go.Scatter(x = hr,
                                   y = slope,
                                           mode = "markers"))
corr_hr_slope_scatter.update_layout(title = "Corr. heart rate vs. slope",
                                   xaxis_title = "Heart rate (bpm)",
                                   yaxis_title = "Slope (%)",
                                    font_color = "white",
                                    paper_bgcolor="rgba(0, 0, 0, 0)",
                                    plot_bgcolor="rgba(0, 0, 0, 0)"
                                    )


corr_speed_slope_scatter = go.Figure()
corr_speed_slope_scatter.add_trace(go.Scatter(x = speed,
                                             y = slope,
                                             mode = "markers"))
corr_speed_slope_scatter.update_layout(title = "Corr. speed vs. slope",
                                      xaxis_title = "Speed (m/s)",
                                      yaxis_title = "Slope (%)",
                                       font_color = "white",
                                       paper_bgcolor="rgba(0, 0, 0, 0)",
                                       plot_bgcolor="rgba(0, 0, 0, 0)"
                                       )

track_fig3 = make_subplots(specs=[[{"secondary_y": True}]])
track_fig3.add_trace(go.Scatter(x = distance,
                                        y = hr,
                                        mode = "lines",
                                        name = "Heart rate"),
                     secondary_y = False,)

track_fig3.add_trace(go.Scatter(x = distance,
                                y = slope,
                                mode = "lines",
                                name = "Slope"),
                     secondary_y = True)
track_fig3.update_yaxes(title_text = "Speed in m/s", secondary_y = False)
track_fig3.update_yaxes(title_text = "Slope in %", secondary_y = True)
track_fig3.update_layout(hovermode="x unified",
                         legend = dict(
                             orientation = "h",
                             yanchor = "bottom",
                             y = 1,
                             xanchor = "right",
                             x = 1
                         ),
                         font_color = "white",
                         paper_bgcolor="rgba(0, 0, 0, 0)",
                         plot_bgcolor="rgba(0, 0, 0, 0)"
                         )


app.title = 'Run run run'
app.layout = row = html.Div(
    [
        dbc.Row(dbc.Col(html.Div(html.H1(html.Center("Run run run"))))),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    dcc.Graph(
                    id = "3D-plot",
                    figure = track_fig1)), width = 6),
                dbc.Col(html.Div(
                    dcc.Graph(
                    id = "mapblox plot",
                    figure = track_fig2)), width = 6)
            ]),
        dbc.Row(dbc.Col(html.Div(dcc.Graph(
                    id = "2yaxis plot",
                    figure = track_fig3)))),
        dbc.Row(
            [
                dbc.Col(html.Div(
                    dcc.Graph(
                        id="corr1",
                        figure=corr_speed_slope_scatter)), width = 6),
                dbc.Col(html.Div(
                    dcc.Graph(
                        id="corr2",
                        figure=corr_hr_slope_scatter)), width = 6)
            ])
])




if __name__ == '__main__':
    app.run_server(debug=True)