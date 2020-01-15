import copy
import math
from tqdm import tqdm

import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

def gaussian_pulse(t, A=1.0, tau=50):
    alpha = (4/tau)**2
    pulse = A * np.exp(-alpha*(t - tau)**2)
    return pulse

def save_Ez():
    zarray = np.array(Ez_list)
    zarray = zarray.transpose()
    plot = [ax.plot_surface(X, Y, zarray[:,:,0], color='0.75', rstride=1, cstride=1)]
    ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(zarray, plot), interval=1000/fps)
    s = ani.to_jshtml()
    with open('Ez.html', 'w') as f:
        f.write(s)
def save_Bx():
    zarray = np.array(Bx_list)
    zarray = zarray.transpose()
    plot = [ax.plot_surface(X, Y, zarray[:,:,0], color='0.75', rstride=1, cstride=1)]
    ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(zarray, plot), interval=1000/fps)
    s = ani.to_jshtml()
    with open('Bx.html', 'w') as f:
        f.write(s)
def save_By():
    zarray = np.array(By_list)
    zarray = zarray.transpose()
    plot = [ax.plot_surface(X, Y, zarray[:,:,0], color='0.75', rstride=1, cstride=1)]
    ani = animation.FuncAnimation(fig, update_plot, frn, fargs=(zarray, plot), interval=1000/fps)
    s = ani.to_jshtml()
    with open('By.html', 'w') as f:
        f.write(s)

def update_plot(frame_number, zarray, plot):
    plot[0].remove()
    plot[0] = ax.plot_surface(X, Y, zarray[:,:,frame_number], cmap="magma")

c = 1.0
dx = 1.0
dy = 1.0
dt = 0.5
num_time = 100
num_space = 50

Ez_list = []
Bx_list = []
By_list = []
Ez = [[0 for _ in range(num_space)] for _ in range(num_space)]
Bx = [[0 for _ in range(num_space)] for _ in range(num_space)]
By = [[0 for _ in range(num_space)] for _ in range(num_space)]

px, py = num_space//2, num_space//2

X = np.linspace(-(num_space//2),num_space//2,num_space)
X, Y = np.meshgrid(X, X)
fig = plt.figure(figsize=(8, 8))
fps = 20 # frame per -1c
frn = num_time-1 # frame number of the animation
ax = fig.add_subplot(111, projection='3d')
ax.set_zlim(-0.5, 0.5)

if __name__ == "__main__":

    # simulation
    for t in tqdm(range(num_time-1)):
        pre_Ez = copy.deepcopy(Ez)
        pre_Bx = copy.deepcopy(Bx)
        pre_By = copy.deepcopy(By)


        # update E
        for x in range(1, num_space):
            for y in range(1, num_space):
                Ez[x][y] = pre_Ez[x][y] + (c**2)*((dt/dx)*(pre_By[x][y] - pre_By[x-1][y]) - (dt/dy)*(pre_Bx[x][y] - pre_Bx[x][y-1]))
        Ez[px][py] += gaussian_pulse(t)

        # update B
        for x in range(num_space-1):
            for y in range(num_space-1):
                Bx[x][y] = pre_Bx[x][y] - (dt/dy)*(Ez[x][y+1] - Ez[x][y])
                By[x][y] = pre_By[x][y] + (dt/dx)*(Ez[x+1][y] - Ez[x][y])

        Ez_list.append(pre_Ez)
        Bx_list.append(pre_Bx)
        By_list.append(pre_By)
    # draw graph
    save_Bx()
    save_By()