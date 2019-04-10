import numpy as np
import physics as ph
import display as dp

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


name = 'lvl7.npz'
Lx = 400.
Ly = 300.
N = 512
start = [20, 100]
dim = [Lx, Ly]

rho = np.zeros((N,N), dtype=complex)
#fx = np.zeros((N,N))
#fy = -10*np.ones((N,N))
win = np.zeros((0,2))
lose = np.zeros((0,2))
hx = Lx / N
hy = Ly / N

rho_temp, p_temp = create_circle(350, 200, 20, -5)
rho += rho_temp
win = np.concatenate( (win, p_temp) )
rho_temp, p_temp = create_circle(220, 80, 40, 5)
rho += rho_temp
lose = np.concatenate( (lose, p_temp) )
#rho_temp, p_temp = create_rectangle(280, 80, 320, 120, 0)
#rho += rho_temp
#win = np.concatenate( (win, p_temp) )
#rho_temp, p_temp = create_rectangle(150, 00, 160, 180, 0)
#rho += rho_temp
#lose = np.concatenate( (lose, p_temp) )



V = ph.poisson_fft(rho, hx, hy)
fx, fy = ph.field(V, hx, hy)
dp.display(dim, start, fx, fy, win, lose)

#np.savez(name, dim=dim, start=start, fx=fx, fy=fy, win=win, lose=lose)

