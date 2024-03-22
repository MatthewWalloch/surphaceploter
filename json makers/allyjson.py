import math
import numpy as np
import plotly.graph_objs as go
import os
import dash
from dash import html, dcc, Input, Output
import json
from scipy.optimize import fsolve
p = np.pi

def plotrotate(w):
    rotate = []
    tfirst = fsolve(trefoily, np.linspace(0, 1, 100), args=(w))
    tcheckdoup = []
    for q in tfirst:
        if trefoily(q, w) < 1e-5:
            if trefoily(q, w) > -1e-5:
                tcheckdoup.append(q)
    tcheck = []
    for q in tcheckdoup:
        check = True
        for item in tcheck:
            if abs(q - item) < 1e-5:
                check = False
        if check:
            tcheck.append(q)
    newnewx=[]
    newnewy=[]
    newnewz=[]
    for i in tcheck:
        x = []
        y = []
        z = []
        for theta in range(0, 50):
            x.append(trefoiltangel(i, 2 * p * theta / 50)[0])
            y.append(trefoiltangel(i, 2 * p * theta / 50)[2])
            z.append(trefoiltangel(i, 2 * p * theta / 50)[3])
        newx = []
        newy = []
        newz = []
        for i in range(len(x)):
            newx.append(x[i])
            newy.append(y[i])
            newz.append(z[i])
        newx.append(x[0])
        newy.append(y[0])
        newz.append(z[0])
        if len(newx) > 0 and abs(newx[0]) > 0:
            newnewx.append(x)
            newnewy.append(y)
            newnewz.append(z)
    newnewx.append(newnewx[0])
    newnewy.append(newnewy[0])
    newnewz.append(newnewz[0])
    return [newnewx, newnewy, newnewz]

# the x of trefoil parameterization used to determine the invese sin
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

pointdict = {}
for i in np.arange(-2.8, 2.8, .05):
    pointdict[f"{i:.2f}"]=plotrotate(i)

file = './plotally.json'

with open(file, 'w') as f:
    json.dump(pointdict, f)