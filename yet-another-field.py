from __future__ import print_function
import sys
import numpy as np
import physics as ph
import display as dp
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

def play():
    fig, ax = plt.subplots()
    line, = ax.plot([], [], lw=2, c='C0')
    dp.display(dim, start, fx, fy, win, lose, portal1, portal2)

    def init():
        line.set_data([], [])
        return line,

    def animate(i):
        line.set_data( x_[0:i], y_[0:i] )
        #line.set_data( x_[i-10:i], y_[i-10:i] )
        return line,
    anim = FuncAnimation(fig, animate, init_func=init, frames= len(x_), interval=32, blit = True, repeat = False)
    plt.show()


def flow(p):
    t = p[0]
    x = p[1]
    y = p[2]
    vx = p[3]
    vy = p[4]
    i = int(y/hy)
    j = int(x/hx)
    if ( p[1] <= 0 or p[1] >= Lx or p[2] <= 0 or p[2] >= Ly ):
        ax = 0
        ay = 0
    else:
        ax = fx[i][j]
        ay = fy[i][j]
    return [ 1, vx, vy, ax, ay]

with open('splash', 'r') as f:
    print (f.read(), end="")

while(1):
    try:
        lvl = input(" Choose level number: ")
        name = os.path.join( 'levels', (str(lvl) + '.npz') )
        data = np.load(name)
        break
    except:
        print ("Level does not exist!")

dim = data['dim']
start = data['start']
fx = data['fx']
fy = data['fy']
win = data['win']
lose = data['lose']
portal1 = data['portal1']
portal2 = data['portal2']
tau = 0.1
nStep = 1000
Lx, Ly = dim[0], dim[1]
N = len(fx)
hx, hy = Lx/N, Ly/N

fig, ax = plt.subplots()
dp.display(dim, start, fx, fy, win, lose, portal1, portal2)
plt.show()

while(1):
    while(1):
        v_i = float(input(" Enter initial velocity: "))
        if (v_i>100 or v_i<0):
            print ("Velocity should be between 0 and 100")
        else:
            break
    theta_i = float(input(" Enter initial angle: "))

    p = [0.]*5
    p[0] = 0.
    p[1] = start[0]
    p[2] = start[1]
    p[3] = v_i*np.cos(np.radians(theta_i))
    p[4] = v_i*np.sin(np.radians(theta_i))
    t_ = []
    x_ = []
    y_ = []
    flag = 0

    portalused=0
    for iStep in range(nStep):
        if ( p[1] <= 0 or p[1] >= Lx or p[2] <= 0 or p[2] >= Ly ):
            flag = 2
            break
        for point in win:
            if ( (abs(p[1]-point[0]) < hx) and (abs(p[2]-point[1]) < hy) ):
                flag = 1
                break
        for point in lose:
            if ( (abs(p[1]-point[0]) < hx) and (abs(p[2]-point[1]) < hy) ):
                flag = 2
                break
        if (portalused==0):
            for point in portal1[2:]:
                if ( (abs(p[1]-point[0]) < hx) and (abs(p[2]-point[1]) < hy) ):
                    p[1] = portal2[0,0]
                    p[2] = portal2[0,1]
                    dtheta = (portal1[1,1]-portal1[1,0])
                    p[3], p[4] = ph.rotate(p[3],p[4], dtheta)
                    portalused=1
                    break
        if (portalused==0):
            for point in portal2[2:]:
                if ( (abs(p[1]-point[0]) < hx) and (abs(p[2]-point[1]) < hy) ):
                    p[1] = portal1[0,0]
                    p[2] = portal1[0,1]
                    dtheta = (portal2[1,1]-portal2[1,0])
                    p[3], p[4] = ph.rotate(p[3],p[4], dtheta)
                    portalused=1
                    break
        if (flag != 0):
            break
        t_.append( p[0] )
        x_.append( p[1] )
        y_.append( p[2] )
        ph.RK4_step( p, tau, flow)

    play()
    if (flag==1):
        if (portalused==1):
            print ("This was a triumph!")
        else:
            print ("You Win!")
        break
    elif (flag==2):
        print ("You lose!")
        print (" Try again")

