import numpy as np
import physics as ph
import display as dp
import os
import matplotlib.pyplot as plt

def create_circle(x0, y0, r, rho_0):
    rho_prime = np.zeros((N,N))
    points = np.zeros((0,2))
    r2 = r**2
    for i in range(N):
        for j in range(N):
            y = i*hy
            x = j*hx
            if ( ((x-x0)**2 + (y-y0)**2) < r2 ):
                rho_prime[i][j] = rho_0
                pnew = [  [x, y ] ]
                points = np.concatenate( (points, pnew) )
    return rho_prime, points

def create_rectangle(x1, y1, x2, y2, rho_0):
    rho_prime = np.zeros((N,N))
    points = np.zeros((0,2))
    for y in np.arange(y1, y2, hy):
        for x in np.arange(x1, x2, hx):
            i = int(y/hy)
            j = int(x/hx)
            rho_prime[i][j] = rho_0
            pnew = [  [x, y ] ]
            points = np.concatenate( (points, pnew) )
    return rho_prime, points

lvl = 9
name = os.path.join( 'levels', (str(lvl) + '.npz') )
Lx = 400.
Ly = 300.
N = 512
start = [50, 250]
dim = [Lx, Ly]

rho = np.zeros((N,N), dtype=complex)
#fx = np.zeros((N,N))
#fy = -10*np.ones((N,N))
win = np.zeros((0,2))
lose = np.zeros((0,2))
portal1 = np.zeros((0,2))
portal2 = np.zeros((0,2))
hx = Lx / N
hy = Ly / N

rho_temp, p_temp = create_circle(350, 70, 20, 5)
rho += rho_temp
win = np.concatenate( (win, p_temp) )
rho_temp, p_temp = create_circle(200, 190, 50, 5)
rho += rho_temp
lose = np.concatenate( (lose, p_temp) )
#rho_temp, p_temp = create_rectangle(330, 30, 370, 70, 0)
#rho += rho_temp
#win = np.concatenate( (win, p_temp) )
#rho_temp, p_temp = create_rectangle(190, 00, 210, 200, 0)
#rho += rho_temp
#lose = np.concatenate( (lose, p_temp) )
x1, y1, x2, y2 = 200, 50, 50, 90
theta1, theta2 = 0, -90
rho_temp, p_temp = create_circle(x1, y1, 10, 15)
rho += rho_temp
portal1 = np.concatenate ( ([ [x1, y1] ], [ [theta1, theta2] ], p_temp) ) 
rho_temp, p_temp = create_circle(x2, y2, 10, 15)
portal2 = np.concatenate ( ([ [x2, y2] ], [ [theta2, theta1] ], p_temp) ) 
rho += rho_temp


V = ph.poisson_fft(rho, hx, hy)
fx, fy = ph.field(V, hx, hy)
fig = plt.figure()
dp.display(dim, start, fx, fy, win, lose, portal1, portal2)
plt.show()

np.savez(name, dim=dim, start=start, fx=fx, fy=fy, win=win, lose=lose, portal1=portal1, portal2=portal2)

