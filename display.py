import numpy as np
import matplotlib.pyplot as plt

def display(dim, start, fx, fy, win, lose, x_=[], y_=[]):
    Lx = dim[0]
    Ly = dim[1]
    N = len(fx)
    x = np.linspace(0, Lx, N)
    y = np.linspace(0, Ly, N)
    sx = N//40
    sy = N//30
    X, Y = np.meshgrid(x,y)
    plt.quiver(X[::sy, ::sx], Y[::sy, ::sx], fx[::sy, ::sx], fy[::sy, ::sx])
    plt.scatter( win[:,0], win[:,1], c='g')
    plt.scatter( lose[:,0], lose[:,1], c='r')
    plt.scatter( [start[0]], [start[1]] )
    plt.scatter( x_, y_, s=10, c='b')
    plt.show()

