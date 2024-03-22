import math
import numpy as np
import plotly.graph_objs as go
import os
import dash
from dash import html, dcc, Input, Output
import json
from scipy.optimize import fsolve
p = np.pi
def trefoilx(t):
    return (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) -4)
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
    retlist = []
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
        retlist.append([x,y,z])
    else:
        x += fnx[::-1]
        y += fny[::-1]
        z += fnz[::-1]
        x.append(fpx[0])
        y.append(fpy[0])
        z.append(fpz[0])
        retlist.append([x, y, z])
        x = spx
        y = spy
        z = spz
        x += snx[::-1]
        y += sny[::-1]
        z += snz[::-1]
        x.append(spx[0])
        y.append(spy[0])
        z.append(spz[0])
        retlist.append([x, y, z])
    return retlist

pointdict = {}

for i in np.arange(-6, 6, .05):
    pointdict[f"{i:.2f}"] = plotpoints(i)

file = './plotallw.json'

with open(file, 'w') as f:
    json.dump(pointdict, f)
