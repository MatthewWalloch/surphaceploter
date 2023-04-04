import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import cos, sin, solve, Symbol, Interval, solveset

global ax
p = np.pi
ax = plt.figure().add_subplot(projection='3d')
plt.xlabel("x")
plt.ylabel("y")


def plottangle(k,l1,l2):
    for i in (k, l1, l2):
        ax.plot(i[0], i[1], i[2])
    plt.show()

#bridge trisection mayer and zupan
def plotroationbad(k,l1,l2):
    #https://www.heldermann-verlag.de/jgg/jgg01_05/jgg0404.pdf
    rotate = []
    theta = [0, p, 2*p]
    tfirst = fsolve(trefoilx, np.linspace(0, p, 100))
    tcheckdoup = []
    for q in tfirst:
        if trefoilx(q) < 1e-7:
            if trefoilx(q) > -1e-7:
                tcheckdoup.append(q)
                tfirst = fsolve(trefoilx, np.linspace(p, 2*p, 100))
    for q in tfirst:
        if trefoilx(q) < 1e-7:
            if trefoilx(q) > -1e-7:
                tcheckdoup.append(q)
    tcheck = []
    for q in tcheckdoup:
        check = True
        if q < 0 or q > 2*p:
            continue
        for item in tcheck:
            if abs(q-item) < 1e-5:
                check = False
        if check:
            tcheck.append(q)
    for i in theta:
        x = []
        y = []
        z = []
        for t in range(0, 100):
            point =trefoil(t/100.0,i)
            print(t)
            print(point)
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        ax.plot(x,y,z)
    # for i in tcheck:
    #     ax.plot(trefoil(i,timescale))
    # for i in (k, l1, l2):
    #     for j in range(0, 100):
    #         ax.plot((np.cos(j * 2*p / 10)*i[0],i[1], i[2]))
    #         rotate.append((np.cos(j * 2*p / 10)*i[0], i[1], i[2], np.sin(j * 2*p / 10)*i[0]))
    plt.show()


def trefoilx(t):
    return (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 2)


def trefoil(t, theta):
    t = t % 1
    start = 1.0 / 12
    stop = 11.0 / 12
    k0 = (np.cos(4 * p * start) * (2+np.cos(2*p*start))-4, np.sin(4 * p * start) * (2 + np.cos(6 * p * start)), np.sin(6 * p * start), 0)
    k1 = (np.cos(4 * p * stop) * (2+np.cos(2*p*stop))-4, np.sin(4 * p * stop) * (2 + np.cos(6 * p * stop)), np.sin(6 * p * stop), 0)
    if t <=start:
        return [np.cos(theta * 2*p) * 12 * k0[0]*t1, 12 * k0[1]*t1, (k0[2]*12 *t1+(1-12 * t1)*-1), np.sin(theta * 2*p)* 12 * k0[0]*t1 ]
    elif t >= stop:
        return [np.cos(theta * 2*p) *12 * k1[0]*t1, 12 * k1[1]*t1, (k1[2]*12 *t1+(11+12 * t1)*-1), np.sin(theta * 2*p)* 12 * k1[0]*t1 ]
    else:
        return [np.cos(theta * 2*p) * (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4), np.sin(4 * p * t) * (2 + np.cos(6 * p * t)),
         np.sin(6 * p * t), np.sin(theta * 2*p)* (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 4) ]



# Prepare arrays x, y, z
start=1.0/12
stop=11.0/12
t = np.linspace(start,stop, 100)
t1 = np.linspace(0,1, 100)
t2 = np.linspace(0,1, 100)
k = ((np.cos(4*p*t)*(2+np.cos(2*p*t))-4), np.sin(4*p*t)*(2+np.cos(6*p*t)), np.sin(6*p*t), 0)
r = (k[0][-1]*t1, k[1][-1]*t1, (k[2][-1]*t1+(1-t1)*-1), 0)
s = (k[0][0]*t1, k[1][0]*t1, (k[2][0]*t1+(1-t1)*1), 0)
plotroationbad(k,r,s)