import copy
import math

import numpy as np
from matplotlib import pyplot as plt

def gaussian_pulse(t, A=1.0, tau=50):
    alpha = (4/tau)**2
    pulse = A * np.exp(-alpha*(t - tau)**2)
    return pulse

def show_result(arr):
    print(*list(map(lambda x: '{0:>8.2f}'.format(x), arr)))

def draw_plot(E, B, lines_E, lines_B, ax, ylim=1):
    lines_E.set_data(X, E)
    lines_B.set_data(X, B)
    ax[0].set_xlim((X.min(), X.max()))
    ax[1].set_xlim((X.min(), X.max()))
    ax[0].set_ylim((-ylim, ylim))
    ax[1].set_ylim((-ylim, ylim))
    plt.draw()
    plt.pause(0.01)


if __name__ == "__main__":

    c = 1.0
    dx = 1.0
    dt = 0.5
    mu = 1.0
    delta = 1.0
    num_time = 2000
    num_space = 100

    E = [0 for _ in range(num_space)]
    B = [0 for _ in range(num_space)]

    refrection = False
    pulse_point = num_space//2

    fig, ax = plt.subplots(2, 1)
    X = np.arange(-(num_space//2), (num_space//2), dx)
    lines_E, = ax[0].plot(X, E)
    lines_B, = ax[1].plot(X, B)

    # simulation
    for t in range(num_time-1):
        pre_E = copy.deepcopy(E)
        pre_B = copy.deepcopy(B)

        # update E
        for x in range(1, num_space):
            if t == 0:
                break
            if x == num_space-1 and not(refrection):
                E[x] = pre_E[x-1] + ((c*dt-dx)/(c*dt+dx))*(E[x-1] - pre_E[x])
            else:
                E[x] = pre_E[x] + (c**2)*(dt/dx)*(pre_B[x] - pre_B[x-1])
        if not(refrection):
            E[0] = pre_E[1] + ((c*dt-dx)/(c*dt+dx))*(E[1] - pre_E[0])
        E[pulse_point] += gaussian_pulse(t)

        # update B
        for x in range(num_space-1):
            B[x] = pre_B[x] + (dt/dx)*(E[x+1]-E[x])

        
        # draw
        draw_plot(E, B, lines_E, lines_B, ax)