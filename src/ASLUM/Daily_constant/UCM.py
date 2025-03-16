# -*- coding: utf-8 -*-
"""Copy of UCM

"""

import numpy as np
import pandas as pd
from functions import *
from ASLUMpy import Constants, UrbanCanyon

def UCM():
    """
    Urban Canopy Model (UCM).
    """

    # Initialize arrays based on new list
    (SR, SG, SW, SWe, LWe, QW, QG, QR, LR, LW, LG, HW, HG, HR,
     LEC, LEG, LER, qR1, Hcan, RnW, RnG, RnR, ReW, ReG, ReR,
     HWe, HGe, HRe, LEGe, LERe, RW, RG, RR, Rcan, FoW, FoR,
     gW, gR, gG, TW, TG, TR, Tcan, TWe, TGe, TRe, TRm, TWd, GW,
     WGv, WRv, delWR, delWG, WRi, WGi, qcan, qW1, SWG, SWR,
     DGe, KGe, RoR, RoG, qsG, DRe, KRe, WG_nd, WR_nd, DWG,
     RsR, QOUT, QIN, IRRI, Ur, Us, qsG, qsR) = arrays(nt)

    # ====================================================
    # Initialize kWb as a 3 x nW array of zeros
    kWb = np.zeros((3, UrbanCanyon.nW))

    # Compute kWb values using Keff function
    for i in range(UrbanCanyon.nW):
        kWb[:, i] = Keff(UrbanCanyon.dW[:, i], UrbanCanyon.kW[:, i], 3)
    # -----------------------------------------------------------------
    # Compute zenith angle and radiative view factors
    qz, qs = Zenith(df['day'], df['tS'], UrbanCanyon.phi, UrbanCanyon.lam, nt)
    FGS, FWW, FGW, FWG, FWS = Viewfac(UrbanCanyon.h, UrbanCanyon.w)

    # Compute solar radiation on different surfaces
    for i in range(nt):
        SW[i, :], SG[i, :], SR[i, :] = Shortrad(
            Constants.opt, qz[i], qs[i], UrbanCanyon.qc, df['Sd'].iloc[i], df['Sq'].iloc[i],
            UrbanCanyon.w, UrbanCanyon.h, UrbanCanyon.aW, UrbanCanyon.aWe,
            UrbanCanyon.aG, UrbanCanyon.aGe, UrbanCanyon.aR, FGS, FWW, FGW, FWG, FWS,
            UrbanCanyon.nW, UrbanCanyon.nG, UrbanCanyon.nR
        )

    # ====================================================
    # compute Green's functions:
    # will be used later to solve the heat equation
    n  = 20
    tl = th * 3600
    FoW = zeros(UrbanCanyon.nt, UrbanCanyon.nW)
    FoR = zeros(UrbanCanyon.nt, UrbanCanyon.nR, UrbanCanyon.nRL)
    icr = 576      #Critical time steps

    # For wall
    for i in range(UrbanCanyon.nW):
        FoW[:, i] = UrbanCanyon.alW[i] * tl / UrbanCanyon.dW[i] ** 2
        gW[i] = Green(FoW[:, i], UrbanCanyon.dW[i], UrbanCanyon.kW[i], UrbanCanyon.alW[i], tl, n, icr)

    # For roof
    for i in range(UrbanCanyon.nR):
        for j in range(UrbanCanyon.nRL):
            FoR[:, i, j] = UrbanCanyon.alR[i, j] * tl / UrbanCanyon.dR[i, j] ** 2
            gR[(i, j)] = Green(FoR[:, i, j], UrbanCanyon.dR[i, j], UrbanCanyon.kR[i, j], UrbanCanyon.alR[i, j], tl, n, icr)

    # Ground
    for i in range(UrbanCanyon.nG):
        gG[i] = 2 * np.sqrt(UrbanCanyon.alG[i] * tl / np.pi) / UrbanCanyon.kG[i]


    # Initial temperature and soil moisture
    TR = TRi[:]  # Assign values from TRi
    TRm = TRi[0]  # Roof mean temperature

    TG = np.array([UrbanCanyon.TGi[0], UrbanCanyon.TGi[1], UrbanCanyon.TGi[2]])  # Ground temperature

    TWd = TWi[:]  # Assign values from TWi (avoid modifying the original)
    TWd += KK  # Convert to Kelvin

    # Adjust temperature for all components
    TG += KK
    TR += KK
    TRm += KK
    Tcan += KK  # Canyon temperature

    # Soil moisture initialization
    WGv = UrbanCanyon.qmG / 100  # Ground water content
    WRv = UrbanCanyon.qmR / 100  # Roof water content

    # Handling precipitation cases
    if Pd[0] == 0:  # Adjusted for Python's zero-based indexing
        delWR = np.zeros(WRv.shape)  # Create zero array with same shape
        delWG = np.zeros(WGv.shape)  # Create zero array with same shape

        WRi = UrbanCanyon.poR * delWR / UrbanCanyon.dwR  # Roof water input (zero if no rain)
        WGi = delWG / UrbanCanyon.dwG  # Ground water input (zero if no rain)
    # Initialize iteration parameters
    niter = 0
    Maxi = 300  # Maximum iterations
    tol = 1.0E-3  # Convergence tolerance

    # Time loop
    for i in range(nt):
        nit0 = 0
        ok = False  # Convergence flag

    while not ok and nit0 < Maxi:
        nit0 += 1

        # Store previous values for convergence check
        x1, x2, x3, x4 = qW1[i, 0], qR1[i, 0], WGv[i, 0], Tcan[i]
        xW = WRv[i]

        # **Energy Balance Computation**
        QW[i, :] = SW[i, :] + LW[i, :] - HW[i, :]
        QR[i, :] = SR[i, :] + LR[i, :] - HR[i, :] - LER[i, :]
        QG[i, :] = SG[i, :] + LG[i, :] - HG[i, :] - LEG[i, :]

        # **Soil Moisture Balance**
        for j in range(UrbanCanyon.nG):
            SWG[i, j] = df['Pd'].iloc[i] - LEG[i, j] / Constants.Lv / Constants.rW - RoG[i, j]
        for j in range(UrbanCanyon.nR):
            SWR[i, j] = df['Pd'].iloc[i] - LER[i, j] / Constants.Lv / Constants.rW - RoR[i, j]

            # Compute temperatures and soil moisture for walls, road, and roof
            if i > 0:
               # Previous time step temperature for walls
               TW0 = TWd[i - 1, :, :]

              # Update wall temperature using the discrete heat equation solver
               TWd[i, :, :] = Tdiscrete(UrbanCanyon.dt, QW[i, :], GW[i, :, :],
                             UrbanCanyon.dW, UrbanCanyon.cW,
                             3, UrbanCanyon.nW, TW0)

             # Update conductive heat flux for each solid layer
               GW[i, :, :] = Conduct(kWb, 3, UrbanCanyon.dW, UrbanCanyon.TB,
                          TWd[i, :, :], UrbanCanyon.nW)

            # Roof temperature update
               for j in range(UrbanCanyon.nR):
                 TR[i, j], TRm[i, j, :], qR1[i, j, :] = TGFm(gR[:, :, j, :],
                                                     QR[:, j],
                                                     qR1[:, j, :], i, icr)

          # Adjust roof temperatures
                 TR[i, :] += TR[0, :]
                 TRm[i, :, :] += TRm[0, :, :]

          # Ground temperature update using numerical integration
               for j in range(UrbanCanyon.nG):
                 TG[i, j] = (TG[0, j] + 0.5 * gG[1, j] * QG[i, j] +
                    np.trapz(np.squeeze(gG[:i, j]),
                             np.concatenate(([0], QG[i - 1::-1, j]))))

               # **Corsby-Chen (LSM) Model for Soil Moisture**
                 DGe[i, :], KGe[i, :] = DKeff(UrbanCanyon.dgG, WGv[i, :],
                                 UrbanCanyon.Ws, UrbanCanyon.Ks,
                                 UrbanCanyon.bG, UrbanCanyon.HsG,
                                 UrbanCanyon.nL)

                 DRe[i, :], KRe[i, :] = DKeff(UrbanCanyon.dgR, WRv[i, :] - UrbanCanyon.Wr,
                                 UrbanCanyon.Ws - UrbanCanyon.Wr,
                                 UrbanCanyon.Ks, UrbanCanyon.bR,
                                 UrbanCanyon.HsR, UrbanCanyon.nL // 2)

                 # **Impervious Surface Update**
                 WGi[i, :] = np.clip(WGi[i - 1, :] + UrbanCanyon.dt *
                        SWG[i, : UrbanCanyon.nG - 1] / UrbanCanyon.dwG,
                        0, 1)

                 WRi[i, :] = np.clip(WRi[i - 1, :] + UrbanCanyon.dt *
                        SWR[i, 0] / UrbanCanyon.dwR,
                        0, 1)

                 # **Vegetation Moisture Update**
                 WRv[i, :] = WCdiff(SWR[i, -1] / 3, KRe[-1], WRv[i - 1, :],
                       DRe[i, :], KRe[i, :], UrbanCanyon.dgR,
                       UrbanCanyon.nL // 2, UrbanCanyon.dt)

                 WGv[i, :] = WCdiff(SWG[i, -1], 0, WGv[i - 1, :],
                       DGe[i, :], KGe[i, :], UrbanCanyon.dgG,
                       UrbanCanyon.nL, UrbanCanyon.dt)

             # Update soil moisture variables
             WGv[i, :] = np.maximum(UrbanCanyon.Wr, WGv[i, :])
             WGv[i, :] = np.minimum(UrbanCanyon.Ws, WGv[i, :])
             WGi[i, :] = np.maximum(0, WGi[i, :])
             WGi[i, :] = np.minimum(1, WGi[i, :])

             WRv[i, :] = np.maximum(UrbanCanyon.Wr, WRv[i, :])
             WRv[i, :] = np.minimum(UrbanCanyon.Ws, WRv[i, :])
             WRi[i, :] = np.maximum(0, WRi[i, :])
             WRi[i, :] = np.minimum(UrbanCanyon.poR, WRi[i, :])

             # Compute normalized water availability
             WG_nd[i, :] = (WGv[i, :] - UrbanCanyon.Wr) / (UrbanCanyon.Ws - UrbanCanyon.Wr)
             WR_nd[i] = (WRv[i] - UrbanCanyon.Wr) / (UrbanCanyon.Ws - UrbanCanyon.Wr)

             # Compute be from water availability
             beR[i] = WR_nd[i]
             beR[i] = 0.4  # Overwriting the previous value

             beG[i] = WG_nd[i, :]

             # Update energy budget
             T1 = TWd[i, 1, :]
             T2 = TG[i, :]
             T3 = TR[i, :]

             TWe[i] = np.dot(UrbanCanyon.fW, T1.squeeze())
             TGe[i] = np.dot(UrbanCanyon.fG, T2.T)
             TRe[i] = np.dot(UrbanCanyon.fR, T3.T)

             LW[i, :], LG[i, :], LR[i, :] = Longrad(Constants.opt, df['LD'].iloc[i], T1, TWe[i], T2, TGe[i],
                                       T3, UrbanCanyon.eW, UrbanCanyon.eWe, UrbanCanyon.eG, UrbanCanyon.eGe, UrbanCanyon.eR, FGS, FWW,
                                       FGW, FWG, FWS, UrbanCanyon.nW, UrbanCanyon.nG, UrbanCanyon.nR)

             Ur[i] = 2 * df['Ua'].iloc[i] * np.log(UrbanCanyon.Zr / (3 * Z0)) / np.log((UrbanCanyon.Za - UrbanCanyon.Zr + UrbanCanyon.Zr / 3) / UrbanCanyon.Z0) / np.pi
             Us[i] = Ur[i] * np.exp(-0.25 * UrbanCanyon.h / UrbanCanyon.w)

             RW[i] = Constants.Cpd * df['ra'].iloc[i] / (11.8 + 4.2 * Us[i])
             RG[i] = RW[i]


             # Compute saturation specific humidity for roof surfaces
             qsR = np.zeros(UrbanCanyon.nR)
             for j in range(UrbanCanyon.nR):
                 qsR[j] = qsat(Constants.Lv, Constants.Rv, Constants.Rd, TR[i, j], Pa[i])

             qR = qsR.copy()  # Roof specific humidity
             qRe = np.dot(qR1[i, :, 2], UrbanCanyon.fR)  # Effective roof humidity

             # Compute heat flux inside the urban canyon
             QIN = (TWd[i, 2, 0] - UrbanCanyon.TB - Constants.KK) * 60  # Heat input into the canyon

             # Compute wall contributions
             HWe = np.dot(HW[i, :], UrbanCanyon.fW)  # Sensible heat flux from walls
             SWe = np.dot(SW[i, :], UrbanCanyon.fW)  # Shortwave radiation from walls
             LWe = np.dot(LW[i, :], UrbanCanyon.fW)  # Longwave radiation from walls

             # Compute aerodynamic resistance and turbulent fluxes for roofs
             RR = np.zeros(UrbanCanyon.nR)
             HR = np.zeros(UrbanCanyon.nR)
             LER = np.zeros(UrbanCanyon.nR)

             for j in range(UrbanCanyon.nR):
                 RR[j] = Raerod(df['Ta'].iloc[i], df['Ua'].iloc[i], UrbanCanyon.Za, UrbanCanyon.Zr, UrbanCanyon.ZmR, UrbanCanyon.ZhR, TR[i, j], 0)

             # Add stomatal resistance to the last roof surface
             RR[-1] += RsR[i]

             for j in range(UrbanCanyon.nR):
                 HR[j] = Constants.Cpd * df['ra'].iloc[i] * (TR[i, j] - df['Ta'].iloc[i]) / RR[j]
                 LER[j] = Constants.Lv * df['ra'].iloc[i] * (qR[j] - df['qa'].iloc[i]) / RR[j]

             # Apply effective evaporation factors
             LER[0] = WRi[i] * LER[0]  # Effective evaporation from gravel roof
             LER[-1] = beR[i] * LER[-1]  # Effective evaporation from green roof

             # Compute aerodynamic resistance inside the canyon
             Rcan = Raerod(df['Ta'].iloc[i], df['Ua'].iloc[i], UrbanCanyon.Za, UrbanCanyon.d, UrbanCanyon.Zmc, UrbanCanyon.Zhc, Tcan[i], Us[i])

             # Compute turbulent fluxes in the canyon
             Hcan = Constants.Cpd * df['ra'].iloc[i] * (Tcan[i] - df['Ta'].iloc[i]) / Rcan
             LEC = Constants.Lv * df['ra'].iloc[i] * (qcan[i] - df['qa'].iloc[i]) / Rcan

             # Compute canyon air temperature (Tcan)
             Tcan[i] = (df['Ta'].iloc[i] / Rcan + (2 * UrbanCanyon.h * TWd[i, 2, 0]) / (RW[i] * UrbanCanyon.w) + TGe[i] / RG[i]) / \
              (1 / Rcan + (2 * UrbanCanyon.h) / (RW[i] * UrbanCanyon.w) + 1 / RG[i])

            # **Compute Turbulent Fluxes**
            for j in range(UrbanCanyon.nR):
                qsR[i, j] = qsat(TR[i, j], df['Pa'].iloc[i])
            qR[i, :] = qsR[i, :]
            qRe[i] = np.dot(qR1[i, :, 2], UrbanCanyon.fR)

            for j in range(UrbanCanyon.nR):
                RR[i, j] = Raerod(df['Ta'].iloc[i], df['Ua'].iloc[i], UrbanCanyon.Za, UrbanCanyon.Zr, UrbanCanyon.ZmR[j], UrbanCanyon.ZhR[j], TR[i, j], 0)
                HR[i, j] = Constants.Cpd * df['ra'].iloc[i] * (TR[i, j] - df['Ta'].iloc[i]) / RR[i, j]
                LER[i, j] = Constants.Lv * df['ra'].iloc[i] * (qR[i, j] - df['qa'].iloc[i]) / RR[i, j]

            # Compute sensible heat fluxes
            for j in range(UrbanCanyon.nW):
                HW[i, :] = Constants.Cpd * df['ra'].iloc[i] * (TWd[i, 0, :] - Tcan[i]) / RW[i]
             for j in range(UrbanCanyon.nG):
                 HG[j] = Constants.Cpd * df['ra'].iloc[i] * (TG[i, j] - df['Ta'].iloc[i]) / RG[i]

            # Compute saturation specific humidity for roof and ground

            for j in range(UrbanCanyon.nR):
                qsR[j] = qsat(Constants.Lv,  Constants.Rv,  Constants.Rd, TR[i, j], df['Pa'].iloc[i])

            for j in range(UrbanCanyon.nG):
                qsG[j] = qsat(Constants.Lv, Constants.Rv, Constants.Rd, TG[i, j], df['Pa'].iloc[i])

             qG = qsG.copy()
             qGe = beG[i] * UrbanCanyon.fG[-1] * qsG[-1] + np.dot(WGi[i, :], qsG[:-1] * UrbanCanyon.fG[:-1])
             temp = beG[i] * UrbanCanyon.fG[-1] + np.dot(WGi[i, :], UrbanCanyon.fG[:-1])

             qcan = (df['qa'].iloc[i] / Rcan[i] + qGe / RG[i]) / (1 / Rcan[i] + temp / RG[i])

             # Compute latent heat fluxes
             for j in range(nG):
                 LEG[j] = df['ra'].iloc[i] * Constants.Lv * (qsG[j] - df['qa'].iloc[i]) / RG[i]

                 LEG[:-1] = WGi[i, :] * LEG[:-1]
                 LEG[-1] = beG[i] * LEG[-1]

                 # Compute effective heat budgets
                 RnR = LR[i, :] + SR[i, :]
                 RnW = LW[i, :] + SW[i, :]
                 RnG = LG[i, :] + SG[i, :]
                 ReW = np.dot(RnW, fW)
                 ReG = np.dot(RnG, fG)
                 ReR = np.dot(RnR, fR)
                 HRe = np.dot(HR[i, :], fR)
                 HWe = np.dot(HW[i, :], fW)
                 HGe = np.dot(HG, fG)
                 LERe = np.dot(LER[i, :], fR)
                 LEGe = np.dot(LEG, fG)

                 # Check convergence
                  err = [
                         abs(x1 / qW1[i, 0] - 1),
                         abs(x2 / qR1[i, 0] - 1),
                         abs(x4 / Tcan[i] - 1)
                   ]
                   emax = max(err)

                   ok = 0
                   if emax < tol:
                       ok = 1

                  # Check maximum number of iterations
                  if nit0 >= Maxi:
                      print("Maximum number of iterations exceeded.")

                  niter += nit0  # Total number of iterations
                 if (i - 253) % 288 == 0:
                     adjusted_day = day + (i - 1) / 288  # Equivalent to MATLAB (day+(i-1)/288)

                     if adjusted_day <= 31:
                         IRRI[i, 0] = 0.043
                     elif adjusted_day <= 60:
                         IRRI[i, 0] = 0.037
                     elif adjusted_day <= 91:
                         IRRI[i, 0] = 0.041
                     elif adjusted_day <= 121:
                         IRRI[i, 0] = 0.037
                     elif adjusted_day <= 152:
                         IRRI[i, 0] = 0.045
                     elif adjusted_day <= 182:
                         IRRI[i, 0] = 0.047
                     elif adjusted_day <= 213:
                         IRRI[i, 0] = 0.049
                     elif adjusted_day <= 244:
                         IRRI[i, 0] = 0.105
                     elif adjusted_day <= 274:
                         IRRI[i, 0] = 0.101
                     elif adjusted_day <= 305:
                         IRRI[i, 0] = 0.093
                     elif adjusted_day <= 335:
                         IRRI[i, 0] = 0.090
                     else:
                         IRRI[i, 0] = 0.065

                     WGv[i, 0] += IRRI[i, 0]
# Adjust temperature values (converting from Kelvin to Celsius)
TW   -= Constants.KK
TG   -= Constants.KK
TR   -= Constants.KK
Tcan -= Constants.KK
TWe  -= Constants.KK
TGe  -= Constants.KK
TRe  -= Constants.KK
TWd  -= Constants.KK

# Additional calculations
Tu  = UrvanCanyon.r * TRe + UrvanCanyon.w * Tcan
Hu  = UrvanCanyon.r * HRe + UrvanCanyon.w * Hcan
LEu = UrvanCanyon.r * LERe + UrvanCanyon.w * LEGe

# ==================================================================
# Average heat fluxes from roofs (r) and from canyons (w), which include walls and roads
Hu     = UrvanCanyon.r * np.squeeze(HRe)  + UrvanCanyon.w * np.squeeze(Hcan)
LEu    = UrvanCanyon.r * LERe             + UrvanCanyon.w * LEC
WGn    = np.squeeze(WGv[:, 0])           # Model soil moisture [%]

# Saving results in a dictionary
results = {
    'Tcan': Tcan,         # Canyon temperature
    'TR1': TR,            # Roof temperature
    'TW': TW,             # Wall temperature
    'TG': TG,             # Ground temperature
    'Hu': Hu,             # Average heat flux from roofs and roads
    'LEu': LEu,           # Average sensible heat flux from roofs and roads
    'Tu': Tu,             # Weighted temperature of the roof and canyon
    'HR': HR,             # Roof sensible heat flux
    'HW': HW,             # Wall sensible heat flux
    'HG': HG,             # Ground sensible heat flux
    'LER': LER,           # Roof latent heat flux
    'LEG': LEG,           # Ground latent heat flux
    'SR': SR,             # Roof net solar radiation
    'LR': LR,             # Roof net longwave radiation
    'SW': SW,             # Wall net solar radiation
    'LW': LW,             # Wall longwave radiation
    'SG': SG,             # Ground net solar radiation
    'LG': LG,             # Ground longwave radiation
    'qcan': qcan,         # Canyon specific humidity
    'WGn': WGn,           # Water volume content in the ground
    'Hcan': Hcan,         # Canyon sensible heat flux
    'LEC': LEC,           # Canyon latent heat flux
    'QG': QG,
    'QW': QW,
    'QR': QR,
}

    return locals()