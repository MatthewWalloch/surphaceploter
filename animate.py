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
file = 'plotallw.json'
my_dir = os.path.dirname(__file__)
json_file_path = os.path.join(my_dir, file)
with open(json_file_path, 'r') as f:
    plotdict = json.load(f)

def plotpoints(w):
    list = plotdict[w]
    fig = go.Figure(data=go.Scatter3d(mode='lines', showlegend=True))
    for coords in list:
        fig.add_trace(go.Scatter3d(x=coords[0], y=coords[1], z=coords[2], mode='lines', showlegend=True))
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




if __name__ == '__main__':
    count = 0
    keys = list(plotdict.keys())
    for i in range(0,len(keys),10):
        plotpoints(keys[i]).write_image(f"AnimateFrames/frame {count}.png")
        count += 1