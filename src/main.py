import copy
import math

import numpy as np

def gaussian_pulse(t, A=1.0, tau=4.0):
    alpha = (4/tau)**2
    pulse = A * np.exp(-alpha*(t - tau)**2)
    return pulse

def show_result(arr):
    for a in arr:
        print(*list(map(lambda x: '{0:>8.2f}'.format(x), a)))

if __name__ == "__main__":

    c = 1.0
    dx = 1.0
    dt = 0.5
    mu = 1.0
    delta = 1.0
    num_time = 20
    num_space = 20

    E = [0 for _ in range(num_space)]
    B = [0 for _ in range(num_space)]

    refrection = False

    # simulation
    for t in range(num_time-1):
        pre_E = copy.deepcopy(E)
        pre_B = copy.deepcopy(B)

        # update E
        for x in range(num_space):
            if t == 0:
                continue
            if x == 0 and not(refrection):
                continue
            elif x == num_space-1 and not(refrection):
                continue
            if x == 0 and refrection:
                E[x] = ((c*dt-dx)/(c*dt+dx))*(E[x+1] - pre_E[x])
            elif x == num_space-1 and refrection:
                E[x] = ((c*dt-dx)/(c*dt+dx))*(E[x] - pre_E[x-1])
            else:
                E[x] = pre_E[x] + pow(c, 2)*(dx/dt)*(pre_B[x] - pre_B[x-1])
        E[num_space//2] += gaussian_pulse(t=t)
            
        # update B
        for x in range(num_space-1):
            B[x] = pre_B[x] + (dt/dx)*(E[x+1]-E[x])
        
        print(*list(map(lambda x: '{0:>8.2f}'.format(x), E)))