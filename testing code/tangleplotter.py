import math
import numpy as np
import plotly.graph_objs as go
import os
import dash
from dash import html, dcc, Input, Output
import json
from scipy.optimize import fsolve

#have a contstant for pi as well as initiate the dash enviorment
p = np.pi
m=2
app = dash.Dash()

def plottrefoil():
    fig = go.Figure()
    x = []
    y = []
    z = []
    for i in range(0, 100):
        x.append(trefoiltangel(i/100, 0)[0])
        y.append(trefoiltangel(i/100, 0)[1])
        z.append(trefoiltangel(i/100, 0)[2])
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines'))
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
# paramterization of the trefoil between 1/12 and 11/12
def trefoiltangel(t, theta, n):
    start = 1.0 / 12
    stop = 11.0 / 12
    k0 = [
        np.cos(theta) * (np.cos(n * theta) * (np.cos(4 * p * start) * (2 + np.cos(2 * p * start)) - 6) - np.sin(
            n * theta) * (np.sin(4 * p * start) * (2 + np.cos(6 * p * start)))),
        np.sin(n * theta) * (np.cos(4 * p * start) * (2 + np.cos(2 * p * start)) - 6) + np.cos(n * theta) * (
                    np.sin(4 * p * start) * (2 + np.cos(6 * p * start))),
        np.sin(6 * p * start),
        np.sin(theta) * (np.cos(n * theta) * (np.cos(4 * p * start) * (2 + np.cos(2 * p * start)) - 6) - np.sin(
            n * theta) * (np.sin(4 * p * start) * (2 + np.cos(6 * p * start))))
    ]

    k1 = [
        np.cos(theta) * (
                    np.cos(n * theta) * (np.cos(4 * p * stop) * (2 + np.cos(2 * p * stop)) - 6) - np.sin(n * theta) * (
                        np.sin(4 * p * stop) * (2 + np.cos(6 * p * stop)))),
        np.sin(n * theta) * (np.cos(4 * p * stop) * (2 + np.cos(2 * p * stop)) - 6) + np.cos(n * theta) * (
                    np.sin(4 * p * stop) * (2 + np.cos(6 * p * stop))),
        np.sin(6 * p * stop),
        np.sin(theta) * (
                    np.cos(n * theta) * (np.cos(4 * p * stop) * (2 + np.cos(2 * p * stop)) - 6) - np.sin(n * theta) * (
                        np.sin(4 * p * stop) * (2 + np.cos(6 * p * stop))))
    ]

    if 0 <= t <= start:
        return [np.cos(theta) * k0[0] * (12 * t),
                k0[1] * (12 * t),
                k0[2] * (12 * t) + (1 - 12 * t) * 2,
                np.sin(theta) * k0[0] * (12 * t)]
    elif 1 > t >= stop:
        return [np.cos(theta) * k1[0] * (1 - 12 * (t - stop)),
                k1[1] * (1 - 12 * (t - stop)),
                k1[2] * (1 - 12 * (t - stop)) + (12 * (t - stop)) * -2,
                np.sin(theta) * k1[0] * (1 - 12 * (t - stop))]
    else:
        return [
            np.cos(theta) * (
                        np.cos(n * theta) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 6) - np.sin(n * theta) * (
                            np.sin(4 * p * t) * (2 + np.cos(6 * p * t)))),
            np.sin(n * theta) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 6) + np.cos(n * theta) * (
                        np.sin(4 * p * t) * (2 + np.cos(6 * p * t))),
            np.sin(6 * p * t),
            np.sin(theta) * (
                        np.cos(n * theta) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 6) - np.sin(n * theta) * (
                            np.sin(4 * p * t) * (2 + np.cos(6 * p * t))))
        ]
def plottrefoil(theta, n):
    fig = go.Figure()
    x = []
    y = []
    z = []
    for i in range(0, 100):
        x.append(trefoiltangel(i/100, theta, n)[0])
        y.append(trefoiltangel(i/100, theta, n)[1])
        z.append(trefoiltangel(i/100, theta, n)[2])
    fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines'))
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

app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='Visualizing the spun trefoil', style={'textAlign': 'center', \
                                                                      'marginTop': 40, 'marginBottom': 40}),
    html.H1(id='H2', children='First we will plot the tangle in question:', style={'textAlign': 'center', \
                                                                      'marginTop': 40, 'marginBottom': 40}),
    dcc.Graph(id='tangle', figure=plottrefoil(0, m), responsive=True,
              style={'justify': 'center', 'width': '80vw', 'height': '80vh'}),
    html.Div([dcc.Slider(0, 2*p, id='theta', value=0, marks=None, step=.1)],style= {'transform': 'scale(.8)'}),
    html.Div(id='updatemode-output-container', style={'textAlign': 'center',
                                                                      'marginTop': 40, 'marginBottom': 40})
])
@app.callback(Output('updatemode-output-container', 'children'),
              Input('theta', 'value'))
def display_value(value):
    return 'theta: {}'.format(value)
@app.callback(
    Output('tangle', 'figure'),
    Input('theta', 'value')
)
def update_graph2(slider):
    fig = plottrefoil(slider, m)
    fig.update(layout_showlegend=True)
    return fig
# makes the dash enviorment work with slider and what not



if __name__ == '__main__':
    app.run_server(debug=True,port=3004)