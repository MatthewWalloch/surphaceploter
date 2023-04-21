import math
import numpy as np
import plotly.graph_objs as go
import os
import dash
from dash import html, dcc, Input, Output
import json

#have a contstant for pi as well as initiate the dash enviorment
p = np.pi
app = dash.Dash()

#bridge trisection mayer and zupan
file = 'plottingspuntrefoil.json'
my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, file)
with open(json_file_path, 'r') as f:
    plotdict = json.load(f)
def plotpoints(w):
    newnewx = plotdict[str(int(w * 10))][0][0]
    newnewy = plotdict[str(int(w * 10))][0][1]
    newnewz = plotdict[str(int(w * 10))][0][2]
    fig = go.Figure(data=go.Scatter3d(x=newnewx[0][0], y=newnewy[0][0], z=newnewz[0][0], mode='lines', showlegend=True))
    for i in range(1, len(newnewx[0])):
        fig.add_trace(go.Scatter3d(x=newnewx[0][i], y=newnewy[0][i], z=newnewz[0][i], mode='lines', showlegend=True))
    # makes sure lines look pretty
    fig.update_traces(
        line=dict(
            width=10
        )
    )
    # make the axis standard
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=10, range=[-10, 10], ),
            yaxis=dict(nticks=10, range=[-10, 10], ),
            zaxis=dict(nticks=10, range=[-10, 10], ), ),
        scene_aspectmode='cube',
        uirevision=1)
    fig.update(layout_showlegend=True)
    return fig
def plotall():
    fig = go.Figure(data=go.Scatter3d(x=[], y=[], z=[], mode='lines', showlegend=True))
    for w in plotdict.keys():
        newnewx = plotdict[w][0][0]
        newnewy = plotdict[w][0][1]
        newnewz = plotdict[w][0][2]
        if len(newnewx)>0:
            for i in range(0, len(newnewx[0])):

                fig.add_trace(go.Scatter3d(x=newnewx[0][i], y=newnewy[0][i], z=newnewz[0][i], mode='lines', showlegend=True))
        # makes sure lines look pretty
    fig.update_traces(
        line=dict(
            width=10
        )
    )
    # make the axis standard
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=10, range=[-10, 10], ),
            yaxis=dict(nticks=10, range=[-10, 10], ),
            zaxis=dict(nticks=10, range=[-10, 10], ), ),
        scene_aspectmode='cube',
        uirevision=1)
    fig.update(layout_showlegend=True)
    return fig
# makes the dash enviorment work with slider and what not
app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='Visualizing the spun trefoil', style={'textAlign': 'center', \
                                                                      'marginTop': 40, 'marginBottom': 40}),
    dcc.Graph(id='allproj', figure=plotall(), responsive=True,
              style={'justify': 'center', 'width': '80vw', 'height': '80vh'}),
    dcc.Graph(id='knotprojection', figure=plotpoints(0), responsive=True, style={'justify': 'center','width': '80vw', 'height': '80vh'}),
    html.Div([dcc.Slider(-10, 10, id='waxis', value=0, marks=None, step=.2)],style= {'transform': 'scale(.8)'}),
    html.Div(id='updatemode-output-container', style={'textAlign': 'center',
                                                                      'marginTop': 40, 'marginBottom': 40})
])
@app.callback(Output('updatemode-output-container', 'children'),
              Input('waxis', 'value'))
def display_value(value):
    return 'w axis: {}'.format(value)
@app.callback(
    Output('knotprojection', 'figure'),
    Input('waxis', 'value')
)
def update_graph2(slider):
    fig = plotpoints(slider)
    fig.update(layout_showlegend=True)
    return fig



if __name__ == '__main__':
    app.run_server(debug=True,port=3004)