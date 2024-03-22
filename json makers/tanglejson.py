import math
import numpy as np
import plotly.graph_objs as go
import os
import dash
from dash import html, dcc, Input, Output
import json
from scipy.optimize import fsolve
p = np.pi

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

def plottrefoil():
    x = []
    y = []
    z = []
    for i in range(0, 101):
        x.append(trefoiltangel(i/100, 0)[0])
        y.append(trefoiltangel(i/100, 0)[1])
        z.append(trefoiltangel(i/100, 0)[2])
    return [x,y,z]

pointdict = plottrefoil()

file = './plottangle.json'

with open(file, 'w') as f:
    json.dump(pointdict, f)