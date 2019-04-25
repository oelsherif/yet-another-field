import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

def display(dim, start, fx, fy, win, lose, portal1=np.zeros((0,2)), portal2=np.zeros((0,2))):
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
    if (len(portal1)!=0 and len(portal2)!=0):
        theta1 = portal1[1,0]
        theta2 = portal2[1,0]
        plt.scatter( portal1[2:,0], portal1[2:,1], c='b')
        t = mpl.markers.MarkerStyle(marker="^")
        t._transform = t.get_transform().rotate_deg(theta1)
        plt.scatter( portal1[0,0], portal1[0,1], marker=t, c='C1')
        plt.scatter( portal2[2:,0], portal2[2:,1], c='C1')
        t = mpl.markers.MarkerStyle(marker="^")
        t._transform = t.get_transform().rotate_deg(theta2)
        plt.scatter( portal2[0,0], portal2[0,1], marker=t, c='b')




