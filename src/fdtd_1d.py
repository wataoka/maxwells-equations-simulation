import math

def gaussian_pulse(E, A=1.0, tau=1.0, alpha=(4/1.0)**2):
    pulse = A * (math.e ** (-alpha*(tau**2)))
    for i in range(len(E)): 
        E[0][i] = pulse
    return E

if __name__ == "__main__":

    c = 1.0
    dx = 1.0
    dt = 0.5
    num_time = 10
    num_space = 10

    E = [[0.0]*num_space for _ in range(num_time)]
    B = [[0.0]*(num_space-1) for _ in range(num_time)]

    # simulation
    for t in range(num_time-1):
        # update E
        for x in range(num_space):
            if t == 0:
                E = gaussian_pulse(E, A=10**7)
                continue
            if x == 0:
                E[t+1][x] = ((c*dt-dx)/(c*dt+dx))*(E[t+1][x+1] - E[t][x])
            elif x == num_space-1:
                E[t+1][x] = ((c*dt-dx)/(c*dt+dx))*(E[t+1][x-1] - E[t][x])
            else:
                E[t+1][x+1] = ((dx)/(dt))*(B[t+1][x] - B[t][x])*E[t+1][x]
            
        # update B
        for x in range(num_space-1):
            if t == 0:
                B[t][x] = ((dt)/(dx))*(E[t][x+1] - E[t][x])
            else:
                B[t][x] = ((dt)/(dx))*(E[t][x+1] - E[t][x]) + B[t-1][x]

for e in E:
    print(e)
for b in B:
    print(b)