import time
import numpy as np

def poisson_fft(rho, hx, hy): #return potential for a certain density
    N = len(rho)
    start_time = time.clock()
    # FFT rows of rho
    f = [ 0.0 ] * N                 # to store rows and columns
    for j in range(N):
        for k in range(N):
            f[k] = rho[j][k]
        f = np.fft.fft(f)
        for k in range(N):
            rho[j][k] = f[k]

    # FFT columns of rho
    for k in range(N):
        for j in range(N):
            f[j] = rho[j][k]
        f = np.fft.fft(f)
        for j in range(N):
            rho[j][k] = f[j]

    # Solve equation in Fourier space
    V = np.zeros((N, N), dtype=complex)
    W = np.exp(1.0j * 2 * np.pi / N)
    Wm = Wn = 1.0 + 0.0j
    for m in range(N):
        for n in range(N):
            denom = 4.0 - Wm - 1 / Wm - Wn - 1 / Wn
            if abs(denom) != 0.0:
                V[m][n] = rho[m][n] * (hx*hy) / denom
            Wn *= W
        Wm *= W

    # Inverse FFT rows of V
    need_inverse = True             # to store rows and columns
    for j in range(N):
        for k in range(N):
            f[k] = V[j][k]
        f = np.fft.ifft(f)
        for k in range(N):
            V[j][k] = f[k]

    # Inverse FFT columns of V
    for k in range(N):
        for j in range(N):
            f[j] = V[j][k]
        f = np.fft.ifft(f)
        for j in range(N):
            V[j][k] = f[j]

    total_time =  time.clock() - start_time
    return(np.real(V))

def RK4_step(x, dt, flow):   #copied from cpt
    """replaces x(t) by x(t + dt) using fourth order Runge-Kutta
    with derivative vector flow
    """
    n = len(x)
    k1 = [ dt * k for k in flow(x) ]
    x_temp = [ x[i] + k1[i] / 2.0 for i in range(n) ]
    k2 = [ dt * k for k in flow(x_temp) ]
    x_temp = [ x[i] + k2[i] / 2.0 for i in range(n) ]
    k3 = [ dt * k for k in flow(x_temp) ]
    x_temp = [ x[i] + k3[i] for i in range(n) ]
    k4 = [ dt * k for k in flow(x_temp) ]
    for i in range(n):
        x[i] += (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) / 6.0

def field(V, hx, hy):      #returns field when given potential
    fx = np.gradient(V, hx, axis=1)
    fy = np.gradient(V, hy, axis=0)
    return fx, fy 
