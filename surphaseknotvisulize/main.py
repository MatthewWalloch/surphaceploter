import math
from scipy.spatial import KDTree
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objs as go
from scipy.optimize import fsolve
from sympy import cos, sin, solve, Symbol, Interval, solveset
import pprint
import dash
from dash import html, dcc, Input, Output
global ax
p = np.pi
ax = plt.figure().add_subplot(projection='3d')
plt.xlabel("x")
plt.ylabel("y")
app = dash.Dash()

#bridge trisection mayer and zupan

def plotrotate(w):
    interval = np.linspace(0, 1, 500)
    posx = []
    posy = []
    posz = []
    negx = []
    negy = []
    negz = []
    for t in interval:
        test = trefoilx(t)
        try:
            arcsin = np.arcsin(w/test)
        except:
            continue
        if (w/test) > 0:
            theta = [arcsin, p-arcsin]
        else:
            theta = [p-arcsin, 2*p+arcsin]
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
    badx = posx + negx
    bady = posy + negy
    badz = posz + negz
    x=[]
    y=[]
    z=[]
    for i in range(len(badx)):
        if not math.isnan(badx[i]):
            if not math.isnan(bady[i]):
                if not math.isnan(badz[i]):
                    x.append(badx[i])
                    y.append(bady[i])
                    z.append(badz[i])
    xline = []
    yline = []
    zline = []
    for i in range(1, len(x)):
        dist = np.sqrt((x[i]-x[i-1])**2+(y[i]-y[i-1])**2+(z[i]-z[i-1])**2)
        if dist > 1:
            if x[i] > 0:
                xline.append(x[i])
                yline.append(y[i])
                zline.append(z[i])
            if x[i-1] > 0:
                xline.append(x[i - 1])
                yline.append(y[i - 1])
                zline.append(z[i - 1])
    t = np.arange(0, len(z))
    newx=[[x[0]]]
    newy=[[y[0]]]
    newz=[[z[0]]]
    i = 1
    n = 0
    placeholder = 0
    for i in range(len(xline)):
        for q in range(0, 10):
            x.append(xline[i] + (1 - q * 1e-1) * (-2 * xline[i]))
            y.append(yline[i])
            z.append(zline[i])
    xrange = max(x)-min(x)
    zrange = max(z)-min(z)
    for i in range(1,len(x)):
        distance = {}
        for j in range(len(x)):
            distance[np.sqrt(.9*(newx[n][i-1-placeholder] - x[j]) ** 2 + (newy[n][i-1-placeholder] - y[j]) ** 2 + (newz[n][i-1-placeholder] - z[j]) ** 2)]=(x[j],y[j],z[j])
        key = min(distance.keys())
        if (key > .1*xrange) and (np.absolute(newz[n][i-1-placeholder]-distance[key][2])>.07*zrange):
            n += 1
            placeholder = i
            newx.append([x[0]])
            newy.append([y[0]])
            newz.append([z[0]])
        else:
            newx[n].append(distance[key][0])
            newy[n].append(distance[key][1])
            newz[n].append(distance[key][2])
            x.remove(distance[key][0])
            y.remove(distance[key][1])
            z.remove(distance[key][2])
    newnewx = []
    newnewy = []
    newnewz = []
    for i in range(len(newx)):
        newnewx.append([newx[i][0]])
        newnewy.append([newy[i][0]])
        newnewz.append([newz[i][0]])
        for j in range(1, len(newx[i])):
            newnewx[i].append(newx[i][j])
            newnewy[i].append(newy[i][j])
            newnewz[i].append(newz[i][j])
        newnewx[i].append(newx[i][0])
        newnewy[i].append(newy[i][0])
        newnewz[i].append(newz[i][0])
    #for i in range(len(newx)):
        #ax.plot(newnewx[i],newnewy[i],newnewz[i])
    fig = go.Figure(data=go.Scatter3d(x=newnewx[0], y=newnewy[0],z=newnewz[0], mode='lines'))
    for i in range(1,len(newnewx)):
        fig.add_trace(go.Scatter3d(x=newnewx[i], y=newnewy[i],z=newnewz[i], mode='lines'))
    fig.update_traces(
        line=dict(
            width=10,
        )
    )
    fig.update_layout(
        scene=dict(
            xaxis=dict(nticks=10, range=[-10, 10], ),
            yaxis=dict(nticks=10, range=[-10, 10], ),
            zaxis=dict(nticks=10, range=[-10, 10], ), ),
        scene_aspectmode='cube',
        uirevision=False)
    return fig
    #plt.show()
def trefoilx(t):
    return (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) -4)


def trefoil(t, theta):
    start = 1.0 / 12
    stop = 11.0 / 12
    if t <=start:
        return [0,0,0,0]
    elif t >= stop:
        return [0,0,0,0]
    else:
        return [np.cos(theta) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4),
                np.sin(4 * p * t) * (2 + np.cos(6 * p * t)),
                np.sin(6 * p * t),
                np.sin(theta)* (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4) ]

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