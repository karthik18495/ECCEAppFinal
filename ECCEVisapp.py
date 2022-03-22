import os

import dash
from dash import dcc
from dash import html
import dash_auth
from dash.dependencies import Input, Output
import plotly.express as px
import numpy as np
import pandas as pd

# Keep this out of source code repository - save in a file or a database
VALID_USERNAME_PASSWORD_PAIRS = {
    'ECCE': 'Optimiser'
}


df = pd.read_csv("/home/karthik18495/ECCEApp/data/ResultsNormalised_12DecOpt_184_calls.csv", sep = ",")

indices = np.arange(1, len(df)+1)

df['indices'] = indices

f1_mod = []
f2_mod = []

for i in range(len(df)):
    temp = np.random.rand()
    f1_mod.append(0.8 + 0.2 * temp) # currently dummy
    f2_mod.append(1.0 - 0.2 * temp)

df['mod_f1'] = f1_mod
df['mod_f2'] = f2_mod

HTML_STYLE = {'height' : '100%', 'width': '100%', 'display': 'block', 'align-items': 'center', 'justify-content': 'center'}

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', "https://www.w3schools.com/w3css/4/w3.css"]

mathjax = 'https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML'

JSRoot = "https://karthik18495.github.io/ECCE_GeomFiles/JsRoot633/scripts/JSRoot.core.js"

JSRoot_url = "https://karthik18495.github.io/ECCE_GeomFiles/JsRoot633/?nobrowser"
GeomFileLocation = "&file=https://karthik18495.github.io/ECCE_GeomFiles/geom/"
DrawOptions = "&item=Default&opt=all;clipx;roty323;rotz356;zoom13"


app = dash.Dash(external_stylesheets=external_stylesheets)

#server = app.server

app.title = "ECCE Tracker Optimisation"
app.scripts.append_script({ 'external_url' : JSRoot })
#auth = dash_auth.BasicAuth(
#    app,
#    VALID_USERNAME_PASSWORD_PAIRS
#)

background_url = "https://cdn.wallpapersafari.com/27/2/neKuYV.jpg"

style = {'background-image':'url({})'.format(background_url)}
app.layout = html.Div(style = style, children = [
    html.H2(html.Center(children = 'ECCE Tracker Optimisation Summary')),
    html.H3(html.Center(children = "This is just under development")),
    html.Div(html.Center([dcc.Dropdown(id="Algo", options = [{'label' : i, 'value' : i} for i in ["MOBO", "MOGA"]], value = "MOGA", style = {'width' : '50%', 'display' : 'block'})])),

    html.Div([dcc.Graph(id='f1-f2-objectives', style = {'height' : '100%', 'width' : '50%', 'display' : 'inline-block'}), html.Iframe(id = "TGeoDraw", style = {'height' : '450px', 'width' : '50%', 'display' : 'inline-block'})], style = HTML_STYLE)
])

@app.callback(Output('f1-f2-objectives', 'figure'), [Input('Algo', 'value')])
def display_f1f2(value):
    fig = None
    if(value == "MOGA"): fig = px.scatter(df, x="mod_f1", y="mod_f2", title = "MOGA performance", labels = {"mod_f1": "Ratio Momentum", "mod_f2": "Ratio Angular resolution"}, custom_data = ['indices'])
    elif value == "MOBO": fig = px.scatter(x=np.random.random(50), y=np.random.random(50), color = np.random.random(50))

    return fig

#@app.callback(Output(component_id = 'TGeoDraw', component_property = 'src'), [Input('Algo', 'value')])
#def RefreshTGeo(value):
#    return JSRoot_url


@app.callback(Output(component_id = 'TGeoDraw', component_property = 'src'), [Input('f1-f2-objectives', 'clickData'), Input('Algo', 'value')])
def DrawGeom(clickData, value):

    if clickData == None: return JSRoot_url
    elif value == "MOBO": return JSRoot_url
    else:
        return JSRoot_url + GeomFileLocation + "ECCE_Tracker_point_{}.root".format(clickData['points'][0]['customdata'][0]) + DrawOptions


#if __name__ == '__main__':
#    app.run_server(debug=True)

# https://root.cern/files/alice2.root&item=Geometry;1
