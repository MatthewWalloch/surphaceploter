import math
import numpy as np
import plotly.graph_objs as go
from scipy.optimize import fsolve
from sympy import cos, sin, solve, Symbol, Interval, solveset
import pprint
import dash
from dash import html, dcc, Input, Output

#have a contstant for pi as well as initiate the dash enviorment
p = np.pi
app = dash.Dash()

def plotrotatey(yvar):
    fig = go.Figure()
    rotate = []
    tfirst = fsolve(trefoily, np.linspace(0, 1, 100), args=(yvar))
    tcheckdoup = []
    for q in tfirst:
        if trefoily(q, yvar) < 1e-5:
            if trefoily(q, yvar) > -1e-5:
                tcheckdoup.append(q)
    tcheck = []
    for q in tcheckdoup:
        check = True
        for item in tcheck:
            if abs(q-item) < 1e-5:
                check = False
        if check:
            tcheck.append(q)
    for i in tcheck:
        x = []
        y = []
        z = []
        for theta in range(0,50):
            x.append(trefoiltangel(i,2* p*theta/ 50)[0])
            y.append(trefoiltangel(i, 2 * p * theta / 50)[2])
            z.append(trefoiltangel(i, 2 * p * theta / 50)[3])
        newx=[]
        newy=[]
        newz=[]
        for i in range(len(x)):
            newx.append(x[i])
            newy.append(y[i])
            newz.append(z[i])
        newx.append(x[0])
        newy.append(y[0])
        newz.append(z[0])
        if len(newx) > 0 and abs(newx[0]) >0:
            fig.add_trace(go.Scatter3d(x=newx, y=newy, z=newz, mode='lines'))

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
        uirevision=False)
    return fig
def trefoily(t, y):
    return np.sin(4 * p * t) * (2 + np.cos(6 * p * t))-y

# paramterization of the trefoil between 1/12 and 11/12
def trefoiltangel(t, theta):
    start = 1.0 / 12
    stop = 11.0 / 12
    k0 = (np.cos(4 * p * start) * (2 + np.cos(2 * p * start)) - 4, np.sin(4 * p * start) * (2 + np.cos(6 * p * start)),
          np.sin(6 * p * start), 0)
    k1 = (np.cos(4 * p * stop) * (2 + np.cos(2 * p * stop)) - 4, np.sin(4 * p * stop) * (2 + np.cos(6 * p * stop)),
          np.sin(6 * p * stop), 0)
    if 0<= t <=start:
        return [np.cos(theta)  * k0[0]*(12*t),
                k0[1]*(12*t)+(1-12*t),
                k0[2]*(12*t),
                np.sin(theta)* k0[0]*(12*t)]
    elif 1> t >= stop:
        return [np.cos(theta)  * k1[0]*(1-12*(t-stop)),
                k1[1]*(1-12*(t-stop))+(12*(t-stop))*-1,
                k1[2]*(1-12*(t-stop)),
                np.sin(theta)* k1[0]*(1-12*(t-stop))]
    else:
        return [np.cos(theta) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4),
                np.sin(4 * p * t) * (2 + np.cos(6 * p * t)),
                np.sin(6 * p * t),
                np.sin(theta)* (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4) ]

# makes the dash enviorment work with slider and what not
app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='Visualizing the spun trefoil', style={'textAlign': 'center', \
                                                                      'marginTop': 40, 'marginBottom': 40}),
    dcc.Graph(id='tangle', figure=plottrefoil(), responsive=True, style={'justify': 'center','width': '80vw', 'height': '80vh'}),
    dcc.Graph(id='knotprojectionthoughy', figure=plotrotatey(0), responsive=True, style={'justify': 'center','width': '80vw', 'height': '80vh'}),

    html.Div([dcc.Slider(-2.8, 2.8, id='yaxis', value=0, marks=None)],style= {'transform': 'scale(.8)'}),
    html.Div(id='updatemode-output-container', style={'textAlign': 'center', \
                                                                      'marginTop': 40, 'marginBottom': 40})
])
@app.callback(Output('updatemode-output-container', 'children'),
              Input('yaxis', 'value'))
def display_value(value):
    return 'y axis: {}'.format(value)
@app.callback(
    Output('knotprojectionthoughy', 'figure'),
    Input('yaxis', 'value')
)
def update_graph2(slider):
    fig = plotrotatey(slider)
    return fig


if __name__ == '__main__':
    app.run_server()