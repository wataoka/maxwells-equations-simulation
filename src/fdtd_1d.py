import math

def gaussian_pulse(idx, E, A=1.0, tau=1.0, alpha=(4/1.0)**2):
    pulse = A * (math.e ** (-alpha*(tau**2)))
    E[0][idx] = pulse
    return E

def show_result(arr):
    for a in arr:
        print(*list(map(lambda x: '{0:>8.2f}'.format(x), a)))
    print()

if __name__ == "__main__":

    c = 1.0
    dx = 1.0
    dt = 0.5
    mu = 1.0
    delta = 1.0
    num_time = 10
    num_space = 10

    E = [[0.0]*num_space for _ in range(num_time)]
    B = [[0.0]*(num_space-1) for _ in range(num_time)]

    # simulation
    for t in range(num_time-1):
        # update E
        for x in range(num_space):
            if t == 0:
                E = gaussian_pulse(idx=len(E)//2, E=E, A=10**7)
                continue
            if x == 0:
                E[t][x] = ((c*dt-dx)/(c*dt+dx))*(E[t][x+1] - E[t-1][x])
            elif x == num_space-1:
                E[t][x] = ((c*dt-dx)/(c*dt+dx))*(E[t][x] - E[t-1][x-1])
            else:
                E[t][x] = ((dx)/(dt))*(B[t][x-1] - B[t-1][x-1])*E[t][x-1]
            
        # update B
        for x in range(num_space-1):
            B[t][x] +=   ((2/(pow(c,2)*dx))+mu*delta)*E[t+1][x]
            B[t][x] +=  (-(2/(pow(c,2)*dx))+mu*delta)*E[t][x]
            if x != 0:
                B[t][x] += B[t][x-1]

show_result(E)
show_result(B)