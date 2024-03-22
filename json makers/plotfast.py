import math
import numpy as np
import plotly.graph_objs as go
import os
import dash
import pprint
from dash import html, dcc, Input, Output
import json
from scipy.optimize import fsolve

#have a contstant for pi as well as initiate the dash enviorment
p = np.pi
app = dash.Dash()

#bridge trisection mayer and zupan
file = '../plotallw.json'
my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, file)
with open(json_file_path, 'r') as f:
    plotdict = json.load(f)
file = '../plotally.json'
my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, file)
with open(json_file_path, 'r') as f:
    plotdicty = json.load(f)
file = '../plottangle.json'
my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, file)
with open(json_file_path, 'r') as f:
    tanglelist = json.load(f)

def plotpoints(w):
    if f"{w:.2f}" == "-0.00":
        w = 0.001
    traces = plotdict[f"{w:.2f}"]
    fig = go.Figure(data=go.Scatter3d(x=[], y=[], z=[], mode='lines', showlegend=True))
    for trace in traces:
        fig.add_trace(go.Scatter3d(x=trace[0], y=trace[1], z=trace[2], mode='lines'))
    fig.update_traces(
        line=dict(
            width=10,
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
    return fig


def plotrotatey(yvar):
    if f"{yvar:.2f}" == "-0.00":
        yvar = 0.001
    fig = go.Figure(data=go.Scatter3d(x=[], y=[], z=[], mode='lines', showlegend=True))
    traces = plotdicty[f"{yvar:.2f}"]
    for i in range(len(traces[0])):
        fig.add_trace(go.Scatter3d(x=traces[0][i], y=traces[1][i], z=traces[2][i], mode='lines'))

    fig.update_traces(
        line=dict(
            width=10,
        )
    )
    # make the axis standard
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=10, range=[-10, 10], ),
            yaxis=dict(nticks=10, range=[-10, 10], ),
            zaxis=dict(nticks=10, range=[-10, 10], ), ),
        scene_aspectmode='cube',
        uirevision=False)
    return fig
def plottrefoil():
    fig = go.Figure(data=go.Scatter3d(x=tanglelist[0], y=tanglelist[1], z=tanglelist[2], mode='lines', showlegend=True))
    fig.update_traces(
        line=dict(
            width=10,
        )
    )
    # make the axis standard
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=10, range=[-10, 10], ),
            yaxis=dict(nticks=10, range=[-10, 10], ),
            zaxis=dict(nticks=10, range=[-10, 10], ), ),
        scene_aspectmode='cube',
        uirevision=False)
    return fig


def plotall():
    fig = go.Figure(data=go.Scatter3d(x=[], y=[], z=[], mode='lines', showlegend=True))
    for i in np.arange(-6,6,.1):
        if f"{i:.2f}" == "-0.00":
            i = 0.001
        traces = plotdict[f"{i:.2f}"]
        for trace in traces:
            fig.add_trace(go.Scatter3d(x=trace[0], y=trace[1], z=trace[2], mode='lines'))
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
def plotally():
    fig = go.Figure(data=go.Scatter3d(x=[], y=[], z=[], mode='lines', showlegend=True))
    for i in np.arange(-2.8, 2.8, .05):
        if f"{i:.2f}" == "-0.00":
            i = 0.001
        traces = plotdicty[f"{i:.2f}"]
        for j in range(len(traces[0])):
            fig.add_trace(go.Scatter3d(x=traces[0][j], y=traces[1][j], z=traces[2][j], mode='lines'))

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
    html.H1(id='H2', children='First we will plot the tangle in question:', style={'textAlign': 'center', \
                                                                      'marginTop': 40, 'marginBottom': 40}),
    dcc.Graph(id='tangle', figure=plottrefoil(), responsive=True,
              style={'justify': 'center', 'width': '80vw', 'height': '80vh'}),
    html.H1(id='H6', children='What happens when we squish the y-axis down?', style={'textAlign': 'center', \
                                                                          'marginTop': 40, 'marginBottom': 40}),
    dcc.Graph(id='allprojy', figure=plotally(), responsive=True,
              style={'justify': 'center', 'width': '80vw', 'height': '80vh'}),
    html.H1(id='H3', children='Then we can look the projection though the y-axis', style={'textAlign': 'center', \
                                                                      'marginTop': 40, 'marginBottom': 40}),
    dcc.Graph(id='knotprojectionthoughy', figure=plotrotatey(0), responsive=True,
              style={'justify': 'center', 'width': '80vw', 'height': '80vh'}),

    html.Div([dcc.Slider(-2.8, 2.8, id='yaxis', value=0, marks=None, step=.05)], style={'transform': 'scale(.8)'}),

    html.Div(id='output-container', style={'textAlign': 'center', \
                                                      'marginTop': 40, 'marginBottom': 40}),
    html.H1(id='H4', children='What happens when we squish the w-axis down?', style={'textAlign': 'center', \
                                                                          'marginTop': 40, 'marginBottom': 40}),
    dcc.Graph(id='allproj', figure=plotall(), responsive=True,
              style={'justify': 'center', 'width': '80vw', 'height': '80vh'}),
    html.H1(id='H5', children='Now we can look thought the w-axis projections:', style={'textAlign': 'center', \
                                                                          'marginTop': 40, 'marginBottom': 40}),

    dcc.Graph(id='knotprojection', figure=plotpoints(0), responsive=True, style={'justify': 'center','width': '80vw', 'height': '80vh'}),
    html.Div([dcc.Slider(-10, 10, id='waxis', value=0, marks=None, step=.05)],style= {'transform': 'scale(.8)'}),
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
@app.callback(Output('output-container', 'children'),
              Input('yaxis', 'value'))
def display_value(value):
    return 'y axis: {}'.format(value)
@app.callback(
    Output('knotprojectionthoughy', 'figure'),
    Input('yaxis', 'value')
)
def update_graph3(slider):
    fig = plotrotatey(slider)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True,port=3004)