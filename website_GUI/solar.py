
#coding=utf-8
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
import us

mapbox_access_token = "pk.eyJ1IjoicHJpeWF0aGFyc2FuIiwiYSI6ImNqbGRyMGQ5YTBhcmkzcXF6YWZldnVvZXoifQ.sN7gyyHTIq1BSfHQRBZdHA"

dfs = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv")
dfstate = dfs.dropna(axis=0)

df1 = pd.read_csv("dem.txt")
df = df1.dropna(axis=0)

app = dash.Dash(__name__)

#app.layout = html.Div(
#style={'backgroundColor': '#787878'},)


external_css = ["https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                "//fonts.googleapis.com/css?family=Dosis:Medium",
                "https://cdn.rawgit.com/plotly/dash-app-stylesheets/62f0eb4f1fadbefea64b2404493079bf848974e8/dash-uber-ride-demo.css",
                "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css"]


for css in external_css:
    app.css.append_css({"external_url": css})




app.layout = html.Div([
    html.Div([
        html.H1("Solar Site Parcel Selection in Colorado")
    ], style={
        'textAlign': "center",
        "padding-left": "100",
        "padding-bottom": "50",
        #"margin": "200",
        "width": '30%',
        "display": 'table-cell',
        "padding-top": "50"}),
    html.Div([
        dcc.Dropdown(id="state-selected",
                     options=[{'label': f'{us.states.lookup(i)}', 'value': i} for i in dfstate.state.unique()], #this is where we might query weighting options
                     value=['CO'],
                     multi=True,
                     style={
                         "display": "block",
                         "margin-left": "auto",
                         "margin-right": "auto",
                         "width": "50%"

                     }
                     ),
        dcc.Input(id = 'input-1-keypress', type = 'number',placeholder = 'Slope Weighted %'),
        dcc.Input(id = 'input-2-keypress', type = 'number',placeholder = 'Aspect Weighted %'),
        #dcc.Input(id = 'input-3-keypress', type = 'number',placeholder = 'Transmission Line/Substation Weighted %'),
        dcc.Input(id = 'input-4-keypress', type = 'number',placeholder = 'Zoning Weighted %'),
        #dcc.Input(id = 'input-5-keypress', type = 'number',placeholder = 'Parcel Size Weighted %'),
        html.Div(id='output-keypress')
    ], style={
        'textAlign': "center",}),
    html.Div(dcc.Graph(id="my-graph"))

],className="container")


@app.callback(
    dash.dependencies.Output("my-graph", "figure"),
    [dash.dependencies.Input("state-selected", "value")]

)
def update_figure(selected):
    trace = []
    #for state in selected:
        #dff = dfstate[dfstate["state"] == state]
    for df.X_COORD in selected:
        trace.append(go.Scattermapbox(
            lat = df.X_COORD,
            lon = df.Y_COORD,
            mode = 'markers',
            marker = {'symbol': "circle-stroked", 'size': 10, 'color': 'rgb(231, 99, 250)'},
            #text = df.OWNNAM,
            #hoverinfo = 'text',
            #name = state
        ))
    return {
        "data": trace,
        "layout": go.Layout(
            autosize = True,
            hovermode = 'closest',
            showlegend = False,
            height = 700,
            mapbox = {'accesstoken': mapbox_access_token,
                    'bearing': 0,
                    'center': {'lat': 38, 'lon': -94},
                    'pitch': 30, 'zoom': 3,
                    "style": 'mapbox://styles/mapbox/light-v9'},
        )

    }


server = app.server

if __name__ == '__main__':
    app.run_server(debug=True)
