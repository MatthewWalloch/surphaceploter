import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import fsolve
from sympy import cos, sin, solve, Symbol, Interval, solveset

global ax
global w
w=0
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
    theta = fsolve(sinsol, np.linspace(0, 1, 100))
    tfirst = fsolve(trefoilx, np.linspace(0, 1, 100))
    thetacheckdoup = []
    tcheckdoup = []
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
    for q in theta:
        if np.sin(q) < 1e-7:
            if np.sin(q) > -1e-7:
                thetacheckdoup.append(q)
    thetacheck = []
    for q in thetacheckdoup:
        check = True
        if q < 0 or q > 2*p:
            continue
        for item in thetacheck:
            if abs(q-item) < 1e-5:
                check = False
        if check:
            thetacheck.append(q)
    print(thetacheck)
    for i in thetacheck:
        x = []
        y = []
        z = []
        for t in range(0, 100):
            point = trefoil(t/100.0,i)
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        ax.plot(x,y,z)
    for i in tcheck:
        x = []
        y = []
        z = []
        for t in range(0, 100):
            point = trefoil(i, t / 100.0)
            x.append(point[0])
            y.append(point[1])
            z.append(point[2])
        ax.plot(x, y, z)
    plt.show()



def sinsol(t):
    return np.sin(t)-w
def trefoilx(t):
    return (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - w)


def trefoil(t, theta):
    t = t % 1
    start = 1.0 / 12
    stop = 11.0 / 12
    k0 = (np.cos(4 * p * start) * (2+np.cos(2*p*start))-4, np.sin(4 * p * start) * (2 + np.cos(6 * p * start)), np.sin(6 * p * start), 0)
    k1 = (np.cos(4 * p * stop) * (2+np.cos(2*p*stop))-4, np.sin(4 * p * stop) * (2 + np.cos(6 * p * stop)), np.sin(6 * p * stop), 0)
    if t <=start:
        return [np.cos(theta * 2*p) * 12 * k0[0]*t, 12 * k0[0]*t,  k0[2]*12*t+(1-12*t)*-1, np.sin(theta * 2*p)* 12 * k0[0]*t]
    elif t >= stop:
        return [np.cos(theta * 2 * p) *12 * k1[0]*(t-stop), 12 * k1[1]*(t-stop), k1[2]*12 *(t-stop)+(1-12 * t)*1, np.sin(theta * 2*p)* 12 * k1[0]*(t-stop) ]
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