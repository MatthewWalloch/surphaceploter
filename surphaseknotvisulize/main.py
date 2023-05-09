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

#bridge trisection mayer and zupan

def plotrotate(w):
    # we first create a line space enviormnet, ie 100 points evenly spaced on 0,1
    interval = np.linspace(0, .9999, 500)
    # we need a posijtive and a negative version for each as the inverse sin
    posx = []
    posy = []
    posz = []
    negx = []
    negy = []
    negz = []
    # this goes and checks if there is an inverse sign for each point in the trefoil
    for t in interval:
        test = trefoilx(t)
        try:
            arcsin = np.arcsin(w/test)
        except:
            continue
        if (w/test) > 0:
            theta = [arcsin]#, p-arcsin]
        else:
            theta = [p-arcsin]#, 2*p+arcsin]
            # evaluate the rotation and seperate into a positve and a negative
        for the in theta:
            pos = trefoil(t, the)
            if pos[0] > 0:
                posx.append(pos[0])
                posy.append(pos[1])
                posz.append(pos[2])
            if pos[0] < 0:
                negx.append(pos[0])
                negy.append(pos[1])
                negz.append(pos[2])
    # these are called bad version as they contain NaN's which is messy
    badx = posx + negx
    bady = posy + negy
    badz = posz + negz
    x=[]
    y=[]
    z=[]
    #removes NaNs
    for i in range(len(badx)):
        if not math.isnan(badx[i]):
            if not math.isnan(bady[i]):
                if not math.isnan(badz[i]):
                    x.append(badx[i])
                    y.append(bady[i])
                    z.append(badz[i])
    # recreates lines that attaceh the tangle to the zy axis
    # adds the points to the graph
    fig = go.Figure(data=go.Scatter3d(x=x, y=y, z=z, mode='lines'))
    # fig = go.Figure(data=go.Scatter3d(x=x[0], y=newnewy[0],z=newnewz[0], mode='lines'))
    # for i in range(1,len(newnewx)):
    #     fig.add_trace(go.Scatter3d(x=newnewx[i], y=newnewy[i],z=newnewz[i], mode='lines'))
    # makes sure lines look pretty
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
    #plt.show()


# the x of trefoil parameterization used to determine the invese sin
def trefoilx(t):
    return (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) -4)

# paramterization of the trefoil between 1/12 and 11/12
def trefoil(t, theta):
    start = 1.0 / 12
    stop = 11.0 / 12
    k0 = (np.cos(4 * p * start) * (2 + np.cos(2 * p * start)) - 4, np.sin(4 * p * start) * (2 + np.cos(6 * p * start)),
          np.sin(6 * p * start), 0)
    k1 = (np.cos(4 * p * stop) * (2 + np.cos(2 * p * stop)) - 4, np.sin(4 * p * stop) * (2 + np.cos(6 * p * stop)),
          np.sin(6 * p * stop), 0)
    if 0 <= t <= start:
        return [np.cos(theta) * k0[0] * (12 * t),
                k0[1] * (12 * t) + (1 - 12 * t),
                k0[2] * (12 * t),
                np.sin(theta) * k0[0] * (12 * t)]
    elif 1 > t >= stop:
        return [np.cos(theta) * k1[0] * (1 - 12 * (t - stop)),
                k1[1] * (1 - 12 * (t - stop)) + (12 * (t - stop)) * -1,
                k1[2] * (1 - 12 * (t - stop)),
                np.sin(theta) * k1[0] * (1 - 12 * (t - stop))]
    else:
        return [np.cos(theta) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4),
                np.sin(4 * p * t) * (2 + np.cos(6 * p * t)),
                np.sin(6 * p * t),
                np.sin(theta) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4)]
# makes the dash enviorment work with slider and what not
app.layout = html.Div(id='parent', children=[
    html.H1(id='H1', children='Visualizing the spun trefoil', style={'textAlign': 'center', \
                                                                      'marginTop': 40, 'marginBottom': 40}),

    dcc.Graph(id='knotprojection', figure=plotrotate(0), responsive=True, style={'justify': 'center','width': '80vw', 'height': '80vh'}),
    html.Div([dcc.Slider(-10, 10, id='waxis', value=0, marks=None)],style= {'transform': 'scale(.8)'}),
    html.Div(id='updatemode-output-container', style={'textAlign': 'center', \
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
    fig = plotrotate(slider)
    return fig


if __name__ == '__main__':
    app.run_server()