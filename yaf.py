import sys
import numpy as np
import physics as ph
import display as dp

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

lvl = sys.argv[1]
data = np.load(lvl)
dim = data['dim']
start = data['start']
fx = data['fx']
fy = data['fy']
win = data['win']
lose = data['lose']

Lx, Ly = dim[0], dim[1]
N = len(fx)
hx, hy = Lx/N, Ly/N

dp.display(dim, start, fx, fy, win, lose)
v_i = float(input(" Enter initial velocity: "))
theta_i = float(input(" Enter initial angle: "))

tau = 0.1
nStep = 1000
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


for iStep in range(nStep):
    if ( p[1] <= 0 or p[1] >= Lx or p[2] <= 0 or p[2] >= Ly ):
        print "You lose!"
        break
    for point in win:
        if ( (abs(p[1]-point[0]) < hx) and (abs(p[2]-point[1]) < hy) ):
            print "You win!"
            flag = 1
            break
    for point in lose:
        if ( (abs(p[1]-point[0]) < hx) and (abs(p[2]-point[1]) < hy) ):
            print "You lose!"
            flag = 2
            break
    if (flag != 0):
        break
    t_.append( p[0] )
    x_.append( p[1] )
    y_.append( p[2] )
    ph.RK4_step( p, tau, flow)


dp.display(dim, start, fx, fy, win, lose, x_, y_)

