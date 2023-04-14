import math
from scipy.spatial import KDTree
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import cos, sin, solve, Symbol, Interval, solveset
import pprint
global ax
global w
w=-3
p = np.pi
ax = plt.figure().add_subplot(projection='3d')
plt.xlabel("x")
plt.ylabel("y")


def plottangle(k,l1,l2):
    for i in (k, l1, l2):
        ax.plot(i[0], i[1], i[2])
    plt.show()

#bridge trisection mayer and zupan

def plotrotate():
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
                print(2)
                xline.append(x[i])
                yline.append(y[i])
                zline.append(z[i])
            if x[i-1] > 0:
                print(1)
                xline.append(x[i - 1])
                yline.append(y[i - 1])
                zline.append(z[i - 1])
    pprint.pprint(xline)
    pprint.pprint(yline)
    pprint.pprint(zline)
    # pprint.pprint(x)
    # pprint.pprint(y)
    # pprint.pprint(z)
    t = np.arange(0, len(z))
    #ax.scatter(x, y, z, c=t, cmap=plt.viridis())
    newx=[x[0]]
    newy=[y[0]]
    newz=[z[0]]
    i = 1
    print(len(x))
    for i in range(len(xline)):
        for q in range(0, 10):
            x.append(xline[i] + (1 - q * 1e-1) * (-2 * xline[i]))
            y.append(yline[i])
            z.append(zline[i])
    for i in range(1,len(x)):
        distance = {}
        for j in range(len(x)):
            distance[np.sqrt((newx[i-1] - x[j]) ** 2 + (newy[i-1] - y[j]) ** 2 + (newz[i-1] - z[j]) ** 2)]=(x[j],y[j],z[j])
        key = min(distance.keys())
        newx.append(distance[key][0])
        newy.append(distance[key][1])
        newz.append(distance[key][2])
        x.remove(distance[key][0])
        y.remove(distance[key][1])
        z.remove(distance[key][2])
    # while i < len(x):
    #     check = True
    #     print(i)
    #     for j in range(len(xline)):
    #         dist = np.sqrt((x[i] - xline[j]) ** 2 + (y[i] - yline[j]) ** 2 + (z[i] - zline[j]) ** 2)
    #         if dist < (1e-20):
    #             print(dist)
    #             for q in range(0,10):
    #                 newx.append(xline[j] + (1 - q * 1e-1) * (-2 * xline[j]))
    #                 newy.append(yline[j])
    #                 newz.append(zline[j])
    #             check = False
    #             for q in range(len(x)):
    #                 print(q, "t")
    #                 print(newx[-1], newy[-1], newz[-1])
    #                 dist = np.sqrt((x[q] - newx[-1]) ** 2 + (y[q] - newy[-1]) ** 2 + (z[q] - newz[-1]) ** 2)
    #                 print(dist)
    #                 if dist < 1e-1:
    #                     print(dist)
    #                     i = j + 1
    #                     break
    #     if check:
    #         newx.append(x[i])
    #         newy.append(y[i])
    #         newz.append(z[i])
    #         i = i + 1
    # t = np.linspace(0, 1, 10)
    # templine = []
    # templine.append((1 - t) * newx[-1] + t * (-1 * newx[-1]))
    # templine.append(0 * t + newy[-1])
    # templine.append(0 * t + newz[-1])
    # for j in range(len(templine)):
    #     newx.append(templine[0][j])
    #     newy.append(templine[1][j])
    #     newz.append(templine[2][j])

    # for i in range(0, len(xline)):
    #     if x[i] > 0:
    #         t = np.linspace(0, 1, 10)
    #         templine = []
    #         # templine.append((1 - t) * xline[i] + t * (-1 * xline[i]))
    #         # templine.append(0*t + yline[i])
    #         # templine.append(0*t + zline[i])
    #         for j in range(len(templine)):
    #             x.append(templine[0][j])
    #             y.append(templine[1][j])
    #             z.append(templine[2][j])
    #         #ax.scatter(templine[0], templine[1], templine[2], c='r', alpha=1)
    ax.plot(newx,newy,newz)
    plt.show()

def sinsol(t):
    return np.sin(2*p*t)-w
def trefoilx(t):
    return (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) -4)


def trefoil(t, theta):
    start = 1.0 / 12
    stop = 11.0 / 12
    k0 = (np.cos(4 * p * start) * (2+np.cos(2*p*start))-4, np.sin(4 * p * start) * (2 + np.cos(6 * p * start)), np.sin(6 * p * start), 0)
    k1 = (np.cos(4 * p * stop) * (2+np.cos(2*p*stop))-4, np.sin(4 * p * stop) * (2 + np.cos(6 * p * stop)), np.sin(6 * p * stop), 0)
    if t <=start:
        return [0,0,0,0]
    elif t >= stop:
        return [0,0,0,0]
    else:
        return [np.cos(theta) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4),
                np.sin(4 * p * t) * (2 + np.cos(6 * p * t)),
                np.sin(6 * p * t),
                np.sin(theta)* (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4) ]


start=1.0/12
stop=11.0/12
t = np.linspace(start,stop, 100)
t1 = np.linspace(0,1, 100)
t2 = np.linspace(0,1, 100)
k = ((np.cos(4*p*t)*(2+np.cos(2*p*t))-4), np.sin(4*p*t)*(2+np.cos(6*p*t)), np.sin(6*p*t), 0)
r = (k[0][-1]*t1, k[1][-1]*t1+(1-t1)*-1, k[2][-1]*t1, 0)
s = (k[0][0]*t1, k[1][0]*t1+(1-t1)*1, k[2][0]*t1, 0)
# plottangle(k,r,s)
plotrotate()
