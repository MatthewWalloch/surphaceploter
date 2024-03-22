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
app = dash.Dash()

#bridge trisection mayer and zupan
file = 'plottingspuntrefoil.json'
my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, file)
with open(json_file_path, 'r') as f:
    plotdict = json.load(f)
file = 'plotspuntrefoily.json'
my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, file)
with open(json_file_path, 'r') as f:
    plotdicty = json.load(f)
def plotpoints(w):
    # we first create a line space enviormnet, ie 100 points evenly spaced on 0,1
    interval = np.linspace(0, .5, 500)
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
            arcsin = np.arcsin(w / test)
        except:
            continue
        if (w / test) > 0:
            theta = [arcsin, p - arcsin]
        else:
            theta = [p - arcsin, 2 * p + arcsin]
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
    # these are called bad version as they contain NaN's which is mes
    fpx = []
    fpy = []
    fpz = []
    # removes NaNs
    for i in range(len(posx)):
        if not math.isnan(posx[i]):
            if not math.isnan(posy[i]):
                if not math.isnan(posz[i]):
                    fpx.append(posx[i])
                    fpy.append(posy[i])
                    fpz.append(posz[i])
    fnx = []
    fny = []
    fnz = []
    # removes NaNs
    for i in range(len(negx)):
        if not math.isnan(negx[i]):
            if not math.isnan(negy[i]):
                if not math.isnan(negz[i]):
                    fnx.append(negx[i])
                    fny.append(negy[i])
                    fnz.append(negz[i])
    # recreates lines that attaceh the tangle to the zy axis
    # adds the points to the graph
    interval = np.linspace(.5, .9999, 500)
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
            arcsin = np.arcsin(w / test)
        except:
            continue
        if (w / test) > 0:
            theta = [arcsin, p - arcsin]
        else:
            theta = [p - arcsin, 2 * p + arcsin]
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
    # these are called bad version as they contain NaN's which is mes
    spx = []
    spy = []
    spz = []
    # removes NaNs
    for i in range(len(posx)):
        if not math.isnan(posx[i]):
            if not math.isnan(posy[i]):
                if not math.isnan(posz[i]):
                    spx.append(posx[i])
                    spy.append(posy[i])
                    spz.append(posz[i])
    snx = []
    sny = []
    snz = []
    # removes NaNs
    for i in range(len(negx)):
        if not math.isnan(negx[i]):
            if not math.isnan(negy[i]):
                if not math.isnan(negz[i]):
                    snx.append(negx[i])
                    sny.append(negy[i])
                    snz.append(negz[i])
    # recreates lines that attaceh the tangle to the zy axis
    # adds the points to the graph

    x = fpx
    y = fpy
    z = fpz
    if (x[-1] - spx[0]) ** 2 + (y[-1] - spy[0]) ** 2 + (z[-1] - spz[0]) ** 2 < .01:
        x += spx
        x += snx[::-1]
        x += fnx[::-1]
        y += spy
        y += sny[::-1]
        y += fny[::-1]
        z += spz
        z += snz[::-1]
        z += fnz[::-1]
        x.append(fpx[0])
        y.append(fpy[0])
        z.append(fpz[0])
        fig = go.Figure(data=go.Scatter3d(x=x, y=y, z=z, mode='lines'))
    else:
        x += fnx[::-1]
        y += fny[::-1]
        z += fnz[::-1]
        x.append(fpx[0])
        y.append(fpy[0])
        z.append(fpz[0])
        fig = go.Figure(data=go.Scatter3d(x=x, y=y, z=z, mode='lines'))
        x = spx
        y = spy
        z = spz
        x += snx[::-1]
        y += sny[::-1]
        z += snz[::-1]
        x.append(spx[0])
        y.append(spy[0])
        z.append(spz[0])
        fig.add_trace(go.Scatter3d(x=x, y=y, z=z, mode='lines'))

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

def plotall():
    fig = go.Figure(data=go.Scatter3d(x=[], y=[], z=[], mode='lines', showlegend=True))
    for i in np.arange(-6,6,.1):
        fig1 = plotpoints(i)
        fig = go.Figure(data=fig.data +fig1.data)
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
    for w in plotdict.keys():
        newnewx = plotdicty[w][0][0]
        newnewy = plotdicty[w][0][1]
        newnewz = plotdicty[w][0][2]
        if len(newnewx)>0:
            for i in range(0, len(newnewx)):

                fig.add_trace(go.Scatter3d(x=newnewx[i], y=newnewy[i], z=newnewz[i], mode='lines', showlegend=True))
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

    html.Div([dcc.Slider(-2.8, 2.8, id='yaxis', value=0, marks=None)], style={'transform': 'scale(.8)'}),

    html.Div(id='output-container', style={'textAlign': 'center', \
                                                      'marginTop': 40, 'marginBottom': 40}),
    html.H1(id='H4', children='What happens when we squish the w-axis down?', style={'textAlign': 'center', \
                                                                          'marginTop': 40, 'marginBottom': 40}),
    dcc.Graph(id='allproj', figure=plotall(), responsive=True,
              style={'justify': 'center', 'width': '80vw', 'height': '80vh'}),
    html.H1(id='H5', children='Now we can look thought the w-axis projections:', style={'textAlign': 'center', \
                                                                          'marginTop': 40, 'marginBottom': 40}),

    dcc.Graph(id='knotprojection', figure=plotpoints(0), responsive=True, style={'justify': 'center','width': '80vw', 'height': '80vh'}),
    html.Div([dcc.Slider(-10, 10, id='waxis', value=0, marks=None, step=.1)],style= {'transform': 'scale(.8)'}),
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