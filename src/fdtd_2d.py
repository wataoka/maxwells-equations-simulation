import copy
import math

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def gaussian_pulse(t, A=1.0, tau=50):
    alpha = (4/tau)**2
    pulse = A * np.exp(-alpha*(t - tau)**2)
    return pulse

def drawing(Ez, Bx, By, fig, height=0.5):
    ax = fig.add_subplot(311, projection='3d')
    ax.set_xlim((X.min(), X.max()))
    ax.set_ylim((Y.min(), Y.max()))
    ax.set_zlim((-height/2, height/2))
    ax.plot_surface(X, Y, np.array(Ez))

    ax = fig.add_subplot(312, projection='3d')
    ax.set_xlim((X.min(), X.max()))
    ax.set_ylim((Y.min(), Y.max()))
    ax.set_zlim((-height/2, height/2))
    ax.plot_surface(X, Y, np.array(Bx))

    ax = fig.add_subplot(313, projection='3d')
    ax.set_xlim((X.min(), X.max()))
    ax.set_ylim((Y.min(), Y.max()))
    ax.set_zlim((-height/2, height/2))
    ax.plot_surface(X, Y, np.array(By))

    plt.draw()
    plt.pause(0.01)

c = 1.0
dx = 1.0
dy = 1.0
dt = 0.5
num_time = 2000
num_space = 100

Ez = [[0 for _ in range(num_space)] for _ in range(num_space)]
Bx = [[0 for _ in range(num_space)] for _ in range(num_space)]
By = [[0 for _ in range(num_space)] for _ in range(num_space)]

px, py = num_space//2, num_space//2

X = np.arange(-(num_space//2), (num_space//2), dx)
Y = np.arange(-(num_space//2), (num_space//2), dy)
fig = plt.figure(figsize=(8, 8))

if __name__ == "__main__":

    # simulation
    for t in range(num_time-1):
        pre_Ez = copy.deepcopy(Ez)
        pre_Bx = copy.deepcopy(Bx)
        pre_By = copy.deepcopy(By)

        # update E
        for x in range(1, num_space):
            if t == 0:
                break
            for y in range(1, num_space):
                Ez[x][y] = pre_Ez[x][y] + (c**2)*((dt/dx)*(pre_By[x][y] - pre_By[x-1][y]) + (dt/dy)*(pre_Bx[x][y] - pre_Bx[x][y-1]))
        Ez[px][py] += gaussian_pulse(t)

        # update B
        for x in range(num_space-1):
            for y in range(num_space-1):
                Bx[x][y] = pre_Bx[x][y] - (dt/dy)*(Ez[x][y+1] - Ez[x][y])
                By[x][y] = pre_By[x][y] - (dt/dx)*(Ez[x+1][y] - Ez[x][y])

        print(t, Ez[px][py])
        # draw graph
        # drawing(Ez, Bx, By, fig)