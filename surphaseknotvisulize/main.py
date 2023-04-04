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

#bridge trisection mayer and zupan bruh m,an
def plotroationbad(k,l1,l2):
    #https://www.heldermann-verlag.de/jgg/jgg01_05/jgg0404.pdf
    theta = np.linspace(0, 2*p, 100)
    rotate = []
    x = Symbol('x', real=True)
    y = Symbol('y', real=True)
    #eq = sin(2 * p * x) * (cos(4 * p * y) * (2 + cos(2 * p * y)) - 4)
    #eq = (cos(4 * p * y) * (2 + cos(2 * p * y))-4)
    print(fsolve(trefoil, p))
    for q in fsolve(trefoil , p):
        print(p)
        print(trefoil(q))

    # sol = solveset(eq, y, Interval(0, 2*p))
    # for q in sol:
    #     print(q)
    # print("Dfs")
    for i in (k, l1, l2):
        for j in range(0, 10):
            #np.cos(4*p*t)*(2+np.cos(2*p*t))-4)
            rotate.append((np.cos(j * 2*p / 10)*i[0], i[1], i[2], np.sin(j * 2*p / 10)*i[0]))
    #plt.show()


def trefoil(t):
    return (np.cos(4 * p * t) * (2 + np.cos(2 * p * t)) - 2)


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