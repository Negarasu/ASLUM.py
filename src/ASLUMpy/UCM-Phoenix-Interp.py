from UCM-Phoenix-Interp import interp
import numpy as np

def interp(x, t, T):
    N = len(T)
    n = len(t)
    X = np.zeros(N)
    tmax = t[-1]
    tmin = t[0]
    
    for i in range(N):
        tt = T[i]
        for j in range(n - 1):
            t0 = t[j]
            tf = t[j + 1]
            x0 = x[j]
            xf = x[j + 1]
            
            if tt < tmin:
                X[i] = x[0]
            elif tt >= t0 and tt <= tf:
                X[i] = x0 + (tt - t0) * (xf - x0) / (tf - t0)
            elif tt > tmax:
                X[i] = x[-2] + (tt - t[-2]) * (x[-1] - x[-2]) / (tmax - t[-2])
    
    return X

