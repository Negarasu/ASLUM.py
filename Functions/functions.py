import numpy as np
import scipy.io as sio
import pandas as pd
import math

def Keff(d, k, n):
    kb = np.zeros(n)
    
    for j in range(n-1):
        kb[j] = (d[j] + d[j+1]) / ((d[j]/k[j]) + (d[j+1]/k[j+1]))

    kb[n-1] = k[n-1]

    return kb

#qz, qs = Zenith(d, tS, phi, lam, nt)
def Zenith(day, tS, phi, lam,nt):
    dy = 365.25  # No of days per year
    dr = 170    # day of the summer solstice
    phR = 0.409  # latitude of the Tropic of Cancer [rad]
    Del = phR * np.cos(2 * np.pi * (day - dr) / dy)  # solar declination angle
    Omt = np.pi * tS / 12 - lam
    a_zenith = np.sin(phi) * np.sin(Del) - np.cos(phi) * np.cos(Del) * np.cos(Omt)
# Assuming you have values for 'd', 't', and 'lam'
#day = Insert the value for 'd' here
#tS = Insert the value for 't' here
#lam = Insert the value for 'lam' here
    for i in range(nt):
         if a_zenith[i] < 0:
            a_zenith[i] = 0

    qz = np.arccos(a_zenith)
    b_zenith = (np.cos(qz) * np.sin(phi) - np.sin(Del)) / (np.cos(Del) * np.sin(qz)) 
    qs = np.arccos(b_zenith)
    [qz,qs] = Zenith(day,tS,phi,lam,nt)
    return qz, qs
 
def Viewfac(h,w):
              
    FSG = np.sqrt(1 + (h / w) ** 2) - h / w  
    FGS = FSG
    FWW = np.sqrt(1 + (w / h) ** 2) - w / h  
    FGW = (1 - FGS) / 2  
    FWG = (1 - FWW) / 2
    FWS = FWG
    FG = FGS
    FW = FWS
 
    return FGS, FWW, FGW, FWG, FWS

def Green(Fo, d, k, a, t, n, icr):
    """
    Compute Green's function for solid layers.

    Parameters:
    Fo  -- Fourier number
    d   -- thickness
    k,a -- thermal conductivity and diffusivity
    t   -- time
    n   -- harmonic term
    icr -- index for critical condition adjustment
    """
    Fo_cr = 1 / np.pi / np.sqrt(2)  # characteristic Fourier number
    dt = t[1] - t[0]  # time step, in s
    t_cr = 300 * icr  # critical nondimensional time

    x = np.array([0, d])

    if t[-1] < t_cr:
        nt = len(t)
    else:
        nt = int(np.ceil(t_cr / dt))

    g = np.zeros((len(t), 2))

    I1 = np.where((Fo[:nt] <= Fo_cr) & (Fo[:nt] != 0))[0]
    I2 = np.where((Fo[:nt] > Fo_cr) & (Fo[:nt] != 0))[0]

    if I1.size > 0:
        # Compute small time solution
        R = np.arange(-np.floor((n-1)/2), np.ceil((n-1)/2) + 1)
        xx, tt, nn = np.meshgrid(x, t[I1], R, indexing='ij')
        K = np.sqrt(a * tt / np.pi) * np.exp(-(xx - 2 * nn * d) ** 2 / (4 * a * tt)) -\
            np.abs(xx - 2 * nn * d) / 2 * erf(np.abs(xx - 2 * nn * d) / (2 * np.sqrt(a * tt)))
        g[I1, :] = 2 / k * np.sum(K, axis=2)

    if I2.size > 0:
        # Solution based on eigenfunction
        R = np.arange(1, n + 1)
        xx, tt, nn = np.meshgrid(x, t[I2], R, indexing='ij')
        K = np.exp(-a * (nn * np.pi / d) ** 2 * tt) / nn ** 2 * np.cos(nn * np.pi * xx / d)
        xx, tt = np.meshgrid(x, t[I2], indexing='ij')
        g[I2, :] = a * tt / k / d + d / 6 / k * (3 * (1 - xx / d) ** 2 - 1) -\
            2 * d / np.pi ** 2 / k * np.sum(K, axis=2)

    return g
def compute_Greens_functions(th, nt, nW, nR, nRL, alW, dW, kW, gW, alR, dR, kR, gR, n, icr, nG, alG, kG, gG):
    n = 20
    tl = th * 3600
    FoW = np.zeros((nt, nW))
    FoR = np.zeros((nt, nR, nRL))
    icr = 576   #critical time steps for
    for i in range(nR):
        for j in range(nRL):
            FoR = alR[i, j] * tl / dR[i, j]**2
            gR = Green(FoR[:, i, j], dR[i, j], kR[i, j], alR[i, j], tl, n, icr)

    for i in range(nG):
        gG = 2 * np.sqrt(alG[i] * tl / np.pi) / kG[i]  # for road

    return FoW, FoR, gW, gR, gG

def Ts(dt, qW, qG, qR, GW, GG, GR, dW, dG, dR, cW, cG, cR, nL, nW, nG, nR, TW0, TG0, TR0):
    TW = np.zeros((1, nL, nW))  #initial arrays
    TR = np.zeros((1, nL, nR))  #initial arrays
    TG = np.zeros((1, nL, nG))  #initial arrays

    for i in range(nW):
        TW[0, 0, i] = TW0[0, 0, i] + dt * (qW[0, i] - GW[0, 0, i]) / dW[0, i] / cW[0, i]

    for i in range(nG):
        TG[0, 0, i] = TG0[0, 0, i] + dt * (qG[0, i] - GG[0, 0, i]) / dG[0, i] / cG[0, i]

    for i in range(nR):
        TR[0, 0, i] = TR0[0, 0, i] + dt * (qR[0, i] - GR[0, 0, i]) / dR[0, i] / cR[0, i]

    for j in range(1, nL):
        for i in range(nW):
            TW[0, j, i] = TW0[0, j, i] + dt * (GW[0, j - 1, i] - GW[0, j, i]) / dW[j, i] / cW[j, i]

        for i in range(nG):
            TG[0, j, i] = TG0[0, j, i] + dt * (GG[0, j - 1, i] - GG[0, j, i]) / dG[j, i] / cG[j, i]

        for i in range(nR):
            TR[0, j, i] = TR0[0, j, i] + dt * (GR[0, j - 1, i] - GR[0, j, i]) / dR[j, i] / cR[j, i]

    return TW, TG, TR

def shortrad(opt, qz, qs, qcan, Sd, Sq, w, h, aW, aWe, aG, aGe, aR, FGS, FWW, FGW, FWG, FWS, nW, nG, nR):
    FG = FGS
    FW = FWS

    # Shadow length
    qn = np.abs(qcan - qs)
    lsh = h * np.tan(qz) * np.sin(qn)
    lsh = np.minimum(lsh, w)

    SR = np.zeros(nR)
    SW1 = np.zeros(nW)
    SW2 = np.zeros(nW)
    SG1 = np.zeros(nG)
    SG2 = np.zeros(nG)

    if opt == 1:  # Kusaka
        for j1 in range(nR):
            SR[j1] = Sd * (1 - aR[j1]) + Sq * (1 - aR[j1])

        for j2 in range(nW):
            SW1[j2] = Sd * lsh * (1 - aW[j2]) / (2 * h) + Sq * FWS * (1 - aW[j2])
            SW2[j2] = (Sd * (w - lsh) * aGe * FWG * (1 - aW[j2]) / w +
                       Sq * FWG * (1 - aW[j2]) +
                       Sd * lsh * aW[j2] * FWW * (1 - aW[j2]) / (2 * h) +
                       Sq * FWS * aW[j2] * FWW * (1 - aW[j2]))

        for j3 in range(nG):
            SG1[j3] = Sd * (w - lsh) * (1 - aG[j3]) / w + Sq * FGS * (1 - aG[j3])
            SG2[j3] = (Sd * lsh * aWe * FGW * (1 - aG[j3]) / (2 * h) +
                       Sq * FWS * aWe * FGW * (1 - aG[j3]))

        SW = SW1 + SW2
        SG = SG1 + SG2

    return SW, SG, SR

def longrad(opt, Ld, TW, TWe, TG, TGe, TR, eW, eWe, eG, eGe, eR, FGS, FWW, FGW, FWG, FWS, nW, nG, nR):
    ss = 5.67e-8  # Stephan-Boltzmann constant [J/s/m2/K4]
    FG = FGS
    FW = FWS
    LG1 = np.zeros(nG)
    LG2 = np.zeros(nG)
    LW1 = np.zeros(nW)
    LW2 = np.zeros(nW)
    Lr = np.zeros(nR)

    if opt == 1:
        for j1 in range(nR):
            Lr[j1] = eR[j1] * (Ld - ss * TR[j1]**4)

        for j2 in range(nW):
            LW1[j2] = eW[j2] * (Ld * FWS + eGe * ss * TGe**4 * FWG +
                                eW[j2] * ss * TW[j2]**4 * FWW - ss * TW[j2]**4)
            LW2[j2] = eW[j2] * ((1 - eGe) * Ld * FGS * FWG +
                                2 * (1 - eGe) * eW[j2] * ss * TW[j2]**4 * FGW * FWG +
                                (1 - eW[j2]) * Ld * FWS * FWW +
                                (1 - eW[j2]) * eGe * ss * TGe**4 * FWG * FWW +
                                eW[j2] * (1 - eW[j2]) * ss * TW[j2]**4 * FWW * FWW)

        for j3 in range(nG):
            LG1[j3] = eG[j3] * (Ld * FGS + 2 * eWe * ss * TWe**4 * FGW - ss * TG[j3]**4)
            LG2[j3] = 2 * eG[j3] * ((1 - eWe) * Ld * FWS * FGW +
                                    (1 - eWe) * eG[j3] * ss * TG[j3]**4 * FWG * FGW +
                                    eWe * (1 - eWe) * ss * TWe**4 * FWW * FGW)

        Lw = LW1 + LW2
        Lg = LG1 + LG2

    return Lw, Lg, Lr

def TGF(g, Q, q, i):
    """
    Compute solid temperatures for walls, roads, and roofs.

    Parameters:
    - g: Green's function
    - Q: net input heat flux at the exposure surface
    - q: heat flux at the inner (building) surface = QGR , QGW
    - i: index

    Returns:
    - T: solid temperature
    - q1: computed value
    """
    
    # Compute new surface temperatures
    S1 = np.trapz(np.squeeze(g[0:i, 0]), [0] + list(q[i-2::-1]))
    S2 = np.trapz(np.squeeze(g[0:i, 1]), [0] + list(Q[i-2::-1]))
    q1 = (2 * (S2 - S1) + g[1, 1] * Q[i]) / g[1, 0]
    S3 = np.trapz(np.squeeze(g[0:i, 1]), [0] + list(q[i-2::-1]))
    S4 = np.trapz(np.squeeze(g[0:i, 0]), [0] + list(Q[i-2::-1]))
    T = -0.5 * q1 * g[1, 1] + 0.5 * Q[i] * g[1, 0] + (S4 - S3)

    return T, q1

def DKeff(d, WGv, Ws, Ks, nL):
    
    for j in range(nL):
        K = Ks * (WGv / Ws)**(2 * b + 3)
        D = b * Ks * Hs * (WGv / Ws)**(b + 2) / Ws
    
    for j in range(nL - 1):
        Ke = (d[j] + d[j + 1]) / ((d[j] / K) + (d[j + 1] / K[j + 1]))
        De = (d[j] + d[j + 1]) / ((d[j] / D) + (d[j + 1] / D[j + 1]))
    
    Ke[nL - 1] = K[nL - 1]
    De[nL - 1] = D[nL - 1]
    
    return De, Ke 

def qsat(Lv, Rv, Rd, T, P):
    # Reference temperature @ 25°C
    Tref = 298
    
    # Reference saturated vapor pressure at Tref
    eref = 3167
    # Compute saturated vapor pressure using Clausius-Clapeyron Equation
    T = TR or TG
    
    es1 = Lv * (T - Tref) / Rv
    es2 = es1 / T
    es3 = es2 / Tref
    es4 = np.exp(es3)
    es5 = eref * es4
    es = es5

    rs1 = Rd / Rv
    rs2 = (Rd / Rv) * es5
    Pa[0] = np.array([[np.array([1.006442])]])
    # Extract the inner value and convert it to a non-array value
    Pa[0] = float(Pa[0][0])
    rs3 = Pa[0] - es5
    
    rs = (Rd/Rv)*es/ (Pa[0]-es)
    qs = rs/(rs+1)
    qs = qsat
    return qs

def WCdiff(inflow, outflow, WC0, D, K, d, nL, dt):
    # Initialize diffusion water content within layers
    DWG = np.zeros(nL)
    WCt = np.zeros(nL)

    # Update diffusive water transport within layers
    DWG[0] = 2 * D[0] * (WC0[0] - WC0[1]) / (d[0] + d[1]) + K[0]
    DWG[-1] = outflow

    for j in range(1, nL - 1):
        DWG[j] = 2 * D[j] * (WC0[j] - WC0[j + 1]) / (d[j] + d[j + 1]) + K[j]

    WCt[0] = WC0[0] + dt * (inflow - DWG[0]) / d[0]

    for j in range(1, nL):
        WCt[j] = WC0[j] + dt * (DWG[j - 1] - DWG[j]) / d[j]

    return WCt

def Conduct(kW, nL, dW, TB, TW, nW):
    GW = np.zeros((1, nL, nW))

    for i in range(nW):
        GW[0, nL-1, i] = 2 * kW[nL-1, i] * (TW[0, nL-1, i] - TB - 273.15) / dW[nL-1, i]

    for j in range(nL - 1):
        for i in range(nW):
            GW[0, j, i] = 2 * kW[j, i] * (TW[0, j, i] - TW[0, j+1, i]) / (dW[j, i] + dW[j+1, i])

    return GW


