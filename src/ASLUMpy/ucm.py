# -*- coding: utf-8 -*-
"""UCM.py

"""

# constants
opt = 1                # option for radiative model: 1-Kusaka; 2-Masson
KK = 273.15            # Celsius-Kelvin conversion
Rd = 287               # gas constant for dry air [J/kg/K]
Rv = 461.5             # gas constant for vapor
rW = 1e3               # density of water [kg/m3]
Cpd = 1005             # heat capacity of dry air [J/kg/K]
Lv = 2.26e6            # latent heat of vaporization [J/kg]
# LAI = 1.0              # leaf area index for short grass
# discretization of ground soil for hydrological modeling
dgG = np.ones(nL) * 1.0 / nL  # vegetated ground
dgR = np.ones(nL // 2) * dR[-1, 1] / (nL / 2)  # green roof

# parameters in bc model for water content diffusion
bG = b[0] # b is a list containing the parameters from previous cell
bR = b[1] # b is a list containing the parameters from previous cell
HsG = Hs[0]
HsG = Hs[0]
HsR = Hs[1]

# number of layers of a composite roof
nRL = kR.shape[1]

#-----------------------------------------------------------------
# atmospheric forcing
dt = 300                           # time interval
th = np.arange(0, 367, 300/3600/24) * 24   # time in hours
th = th[:105409]
nt = len(th)                      # # of samples in modeling
tS = th                           # local<->standard time
Sq = np.zeros((nt, 1))           # diffusive
beR = np.ones((nt, 1))              # evaporation efficiency coeff for green roof
beG = np.ones((nt, 1))              # evaporation efficiency coeff for green roof
RoR = np.zeros((nt, nR))         # roof surface runoff
RoG = np.zeros((nt, nG))         # ground runoff
#-----------------------------------------------------------------
# computation of roughness length and zero displacement height
# Macdonald et al 1998 Atmospheric Environment 32(11): 1857-1864
k = 0.4
a = 4.43
b = 1.0
CD = 1.2
d = Zr * (1 + a ** (-r) * (r - 1))
Z0 = Zr * (1 - d / Zr) * np.exp(-((0.5 * b * CD * (1 - d / Zr) * h / k ** 2) ** (-0.5)))

# Define initial values for certain variables
Ws = 0.5  # Example for Ws (soil moisture or another constant)
dwR = 0.2  # Example for dwR (roof layer constant)
dwG = 0.3  # Example for dwG (ground layer constant)

#Efective thermal material properties
# Calculations
#alW = kW / cW #diffusivity
alR = kR / cR  # Thermal diffusivity for roof
alG = kG / cG  # Thermal diffusivity for ground
eWe = np.dot(fW, eW)  # Effective emissivity for wall
eGe = np.dot(fG, eG)  # Effective emissivity for ground
aWe = np.dot(fW, aW)  # Effective albedo for wall
aGe = np.dot(fG, aG)  # Effective albedo for ground

# Initialize kWb matrix
nW = 3  # Number of subdivisions for wall (example)
kWb = np.zeros((3, nW))  # Initialize the kWb matrix with zeros

# Initialize kWb as an array of zeros with the correct shape
kWb = np.zeros(dW.shape[0] - 2)

# Loop to perform the calculation, iterating through the first dimension of dW and kW
for j in range(dW.shape[0] - 2):
    # Perform element-wise division for the denominator, ensuring scalar values are used
    denominator = (dW[j, 0] / kW[j, 0]) + (dW[j + 1, 0] / kW[j + 1, 0])

    # Calculate the numerator (element-wise addition), ensuring scalar values are used
    numerator = dW[j, 0] + dW[j + 1, 0]

    # Perform element-wise division to get the result
    kWb[j] = numerator / denominator

# Output the results
print("kWb:", kWb)

"""Zenith's function"""

# Constants
dy = 365.25  # Number of days per year
dr = 170     # Day of the summer solstice
phR = 0.409  # Latitude of the Tropic of Cancer [rad]

# Solar declination angle
Del = phR * np.cos(2 * np.pi * (d - dr) / dy)
# Solar hour angle
Omt = np.pi * tS / 12 - lam
# Cosine of the zenith angle
a = np.sin(phi) * np.sin(Del) - np.cos(phi) * np.cos(Del) * np.cos(Omt)
a[a < 0] = 0  # Ensure a is non-negative

# Zenith angle
qz = np.arccos(a)

# Auxiliary calculations for solar azimuth angle
with np.errstate(divide='ignore', invalid='ignore'):  # Suppress warnings temporarily
    b = (np.cos(qz) * np.sin(phi) - np.sin(Del)) * (1 / np.sin(Del)) / np.sin(qz)

# Clamp b values to the range [-1, 1]
b = np.clip(b, -1, 1)

# Compute solar azimuth angle
qs = np.arccos(b)

# Outputs
print("Zenith angle (qz):", qz)
print("Solar azimuth angle (qs):", qs)

"""Viewfac's function"""

#Viewfac's function
def Viewfac(h, w):
    """
    Compute view factors for a street canyon.

    Parameters:
    h (float): Normalized building height
    w (float): Normalized road width

    Returns:
    FSG, FGS, FWW, FGW, FWG, FWS: View factors for different configurations
    """
    FSG = np.sqrt(1 + (h / w)**2) - h / w  # Sky-Ground (road) Fr in Masson
    FGS = FSG
    FWW = np.sqrt(1 + (w / h)**2) - w / h  # Wall-Wall
    FGW = (1 - FGS) / 2                    # Ground-Wall
    FWG = (1 - FWW) / 2
    FWS = FWG

    return FSG, FGS, FWW, FGW, FWG, FWS

FSG, FGS, FWW, FGW, FWG, FWS = Viewfac(h, w)

print("FSG (Sky-Ground):", FSG)
print("FGS (Ground-Sky):", FGS)
print("FWW (Wall-Wall):", FWW)
print("FGW (Ground-Wall):", FGW)
print("FWG (Wall-Ground):", FWG)
print("FWS (Wall-Sky):", FWS)

# Initialize arrays
gW = np.zeros((nt, 2, nW))
gG = np.zeros((nt, nG))
gR = np.zeros((nt, 2, nR, nRL))
TG = np.zeros((nt, nG))
TR = np.zeros((nt, nR))
TWd = np.zeros((nt, 3, nW))
GW = np.zeros((nt, 3, nW))
TRm = np.zeros((nt, nR, nRL-1))  # inner surface temperature of roofs
TWe = np.zeros((nt, 1))
TGe = np.zeros((nt, 1))
TRe = np.zeros((nt, 1))
LW = np.zeros((nt, nW))
LG = np.zeros((nt, nG))
LR = np.zeros((nt, nR))
SW = np.zeros((nt, nW))
SG = np.zeros((nt, nG))
SR = np.zeros((nt, nR))
HW = np.zeros((nt, nW))
HG = np.zeros((nt, nG))
HR = np.zeros((nt, nR))
HWe = np.zeros((nt, 1))
HGe = np.zeros((nt, 1))
HRe = np.zeros((nt, 1))
SWe = np.zeros((nt, 1))
LWe = np.zeros((nt, 1))
LEC = np.zeros((nt, 1))
LEG = np.zeros((nt, nG))
LER = np.zeros((nt, nR))
RW = np.zeros((nt, 1))
RG = np.zeros((nt, 1))
RR = np.zeros((nt, nR))
Rcan = np.zeros((nt, 1))
Hcan = np.zeros((nt, 1))
Tcan = np.zeros((nt, 1))
LEGe = np.zeros((nt, 1))
LERe = np.zeros((nt, 1))
Ur = np.zeros((nt, 1))
Us = np.zeros((nt, 1))
RnW = np.zeros((nt, nW))
RnG = np.zeros((nt, nG))
RnR = np.zeros((nt, nR))
ReW = np.zeros((nt, 1))
ReG = np.zeros((nt, 1))
ReR = np.zeros((nt, 1))
QW = np.zeros((nt, nW))
QG = np.zeros((nt, nG))
QR = np.zeros((nt, nR))
qR = np.zeros((nt, nR))
qsR = np.zeros((nt, nR))
qRe = np.zeros((nt, 1))
qG = np.zeros((nt, nG))
qsG = np.zeros((nt, nG))
qGe = np.zeros((nt, 1))
qcan = np.zeros((nt, 1))
QIN = np.zeros((nt, 1))
QOUT = np.zeros((nt, 1))
qW1 = np.zeros((nt, nW))
qR1 = np.zeros((nt, nR, nRL))

# Soil moisture
DGe = np.zeros((nt, nL))
KGe = np.zeros((nt, nL))
DRe = np.zeros((nt, nL // 2))
KRe = np.zeros((nt, nL // 2))

# Vegetated
WGv = Ws * np.ones((nt, nL))
WRv = Ws * np.ones((nt, nL // 2))

# Gravel roof
WRi = np.ones((nt, max(1, nR-1)))
delWR = dwR * np.ones((nt, max(1, nR-1)))

# Impervious ground
WGi = np.ones((nt, nG-1))
IRRI = np.zeros((nt, 1))
delWG = dwG * np.ones((nt, nG-1))

# Nondimensionalized soil vwc
WG_nd = np.zeros((nt, nL))
WR_nd = np.zeros((nt, 1))

# SWG and SWR
SWG = np.zeros((nt, nG))
SWR = np.zeros((nt, nR))

# Infiltration
DWG = np.zeros((nt, nL))

# Stomatal resistance
RsR = np.zeros((nt, 1))

"""shortwave radiation"""

def shortrad(opt, qz, qs, qcan, SD, Sq, w, h, aW, aWe, aG, aGe, aR, FGS, FWW, FGW, FWG, FWS, nW, nG, nR):
    """
    Compute shortwave radiation budget for street canyon using Python
    for each subdivided type of surface, using individual albedo
    of its own type and effective albedo of other surfaces.

    Parameters:
    opt: int
        Option for the calculation method (1 for Kusaka, 2 for Masson).
    qz: float
        Zenith angle of the sun.
    qs: float
        Solar azimuth angle.
    qcan: float
        Canyon azimuth angle.
    Sd, Sq: float
        Direct and diffuse solar radiation.
    w, h: float
        Canyon width and height.
    aW, aG, aR: arrays
        Albedos for wall, ground, and roof surfaces respectively.
    FGS, FWW, FGW, FWG, FWS: floats
        View factors.
    nW, nG, nR: int
        Number of wall, ground, and roof subdivisions.

    Returns:
    SW, SG, SR: arrays
        Shortwave radiation for walls, ground, and roof surfaces.
    """

    FG = FGS
    FW = FWS
          # Shadow length calculation
    qn = abs(qcan - qs)
    lsh = h * np.tan(qz) * np.sin(qn)
    lsh = np.minimum(lsh, w)  # Limit shadow length to canyon width

    # Initialize radiation arrays
    SR = np.zeros((SD.shape[0], nR))  # Roof radiation, adjusted shape
    SW1 = np.zeros((SD.shape[0], nR))  # Wall radiation (part 1), adjusted shape
    SW2 = np.zeros((SD.shape[0], nR))  # Wall radiation (part 2), adjusted shape
    SG1 = np.zeros(nG)  # Ground radiation (part 1)
    SG2 = np.zeros(nG)  # Ground radiation (part 2)

    # Compute radiation based on selected method
    if opt == 1:  # Kusaka method
        # Iterate through roof types and calculate radiation
        for i in range(nR):
            SR[:, i] = SD[:, 0] * (1 - aR[i]) + Sq[:, 0] * (1 - aR[i])
        for i in range(nW):
            SW1[:, i] = SD[:, 0] * lsh * (1 - aW[i]) / (2 * h) + Sq[:, 0] * FWS * (1 - aW[i])  # Using SD[:, 0] and Sq[:, 0]
            SW2[:, i] = (
                SD_in[:, 0] * (w - lsh) * aGe * FWG * (1 - aW[i]) / w
                + Sq[:, 0] * FWG * (1 - aW[i])
                + SD[:, 0] * lsh * aW[i] * FWW * (1 - aW[i]) / (2 * h)
                + Sq[:, 0] * FWS * aW[i] * FWW * (1 - aW[i])
        )  # Using SD_in[:, 0] and Sq[:, 0]
        SG1[:] = SD[:, 0] * (w - lsh) * (1 - aG[0]) / w + Sq[:, 0] * FGS * (1 - aG[0])  # Using SD[:, 0] and Sq[:, 0]
        SG2[:] = (
            SD_in[:, 0] * lsh * aWe * FGW * (1 - aG[0]) / (2 * h) +
            Sq[:, 0] * FWS * aWe * FGW * (1 - aG[0])
        )  # Using SD_in[:, 0] and Sq[:, 0]

    # Sum the components
    SW = SW1 + SW2
    SG = SG1 + SG2

    return SW, SG, SR

"""Green's function"""

def Green( Fo, dR, kR, alR, ts, n):
    #------------------------------------------------------------------------
    #  Purpose:
    #     compute Green's fucntion for solid layers
    #  Synopsis:
    #     [g] = Green(Fo,d,k,a,t,n)
    #  Variable Description:
    #     Fo    - Fourier number
    #     d     - thickness
    #     k,a   - thermal conductivity and diffusivity
    #     t     - time
    #------------------------------------------------------------------------
    Fo_cr = 1.0/np.pi/np.sqrt(2)   #characteristic Fourier number
    x     = np.array([ 0, dR])
    nt    = len(ts)
    g     = np.zeros(shape=(nt,2))
    I1 = np.where((Fo<=Fo_cr)&(Fo!=0))
    I2 = np.where( (Fo>Fo_cr)&(Fo!=0))

    if len(I1) > 0:
        # compute small time solution
        R          = np.arange( -math.floor((n-1)/2), math.ceil((n-1)/2) + 1, 1)
        xx, tt, nn = np.meshgrid(x, ts[I1], R)
        #xx = xx.T; tt = tt.T; nn = nn.T;
        K          = np.sqrt( alR * tt / np.pi) * np. exp(-((xx-2 * nn * dR)**2) / 4.0 /alR / tt ) - ( abs(xx-2 * nn * dR)/2.0 ) * special.erfc(abs(xx-2*nn*dR)/2.0/np.sqrt(alR * tt))
        g[I1,:]    = 2.0/kR * K.sum(axis=2)

    if len(I2) > 0:
        # solution based on eigenfunction
        R          =  np.arange( 1, n+1, 1)
        xx, tt, nn = np.meshgrid( x, ts[I2], R)
        K          = np.exp( -alR * ( nn * np.pi / dR )**2.0 * tt )/nn**2.0*np.cos(nn*np.pi*xx/dR)
        xx,tt      = np.meshgrid( x, ts[I2] )
        g[I2,:]    = alR * tt/kR/dR + dR/6./kR*(3*(1-xx/dR)**2-1) - 2*dR/np.pi**2/kR*K.sum(axis=2)

    return g

n = 20
tl = th * 3600  # Convert time to seconds (th should be defined earlier)
nt = 10  # Example value for nt (number of time steps)
nW = 5  # Number of weather stations (example value)
nR = 5  # Number of rows (example value)
nRL = 4  # Number of regions (example value)
nG = 3  # Number of green areas (example value)
icr = 576  # Critical time steps

# Loop over the regions and calculate the Green's functions for roads
for i in range(nR):
    for j in range(nRL):
        FoR[:, i, j] = alR[i, j] * tl / dR[i, j]**2
        gR[:, i, j] = Green(FoR[:, i, j], dR[i, j], kR[i, j], alR[i, j], tl, n, icr)

# Loop over the green areas and calculate the Green's functions
for i in range(nG):
    gG[:, i] = 2 * np.sqrt(alG[i] * tl / np.pi) / kG[i]  # For green areas

# Initialize temperature and soil moisture
TR = np.copy(TRi)
TRm = np.copy(TRi)
TG = np.array([TGi[0], TGi[1], TGi[2]])
TWd = np.copy(TWi) + KK
TG += KK
TR += KK
TRm += KK
Tcan += KK

WGv = qmG / 100
WRv = qmR / 100

if Pd[0] == 0:
    delWR = np.zeros_like(WRv)
    delWG = np.zeros_like(WGv)
    WRi = poR * delWR / dwR
    WGi = delWG / dwG

"""Surface model using time iterations"""

niter = 0
Maxi = 300
tol = 1.0E-3

for i in range(nt):  # time looping
    nit0 = 0
    ok = False
    while not ok and (nit0 < Maxi):
        nit0 += 1

        x1 = qW1[i, 0]
        x2 = qR1[i, 0]
        x4 = Tcan[i]
        x3 = WGv[i, 0]
        xW = WRv[i]

        QW[i, :] = SW[i, :] + LW[i, :] - HW[i, :]
        QR[i, :] = SR[i, :] + LR[i, :] - HR[i, :] - LER[i, :]
        QG[i, :] = SG[i, :] + LG[i, :] - HG[i, :] - LEG[i, :]

        for j1 in range(nG):
            SWG[i, j1] = Pd[i] - LEG[i, j1] / Lv / rW - RoG[i, j1]
        for j1 in range(nR):
            SWR[i, j1] = Pd[i] - LER[i, j1] / Lv / rW - RoR[i, j1]

        if i > 0:
            TW0 = TWd[i - 1, :, :]
            TWd[i, :, :] = Tdiscrete(dt, QW[i, :], GW[i, :, :], dW, cW, 3, nW, TW0)
            GW[i, :, :] = Conduct(kWb, 3, dW, TB, TWd[i, :, :], nW)

            for j in range(nR):
                TR[i, j] = TR[0, j] + 0.5 * gG[2, j] * QG[i, j] + np.trapz(gG[1:i, j], [0] + list(QG[i-1::-1, j]))

            DGe[i, :], KGe[i, :] = DKeffect(dgG, WGv[i, :], Ws, Ks, bG, HsG, nL)
            DRe[i, :], KRe[i, :] = DKeffect(dgR, WRv[i, :] - Wr, Ws - Wr, Ks, bR, HsR, nL / 2)

            WGi[i, :] = WGi[i - 1, :] + dt * SWG[i, :nG - 1] / dwG
            WRi[i, :] = WRi[i - 1, :] + dt * SWR[i, 0] / dwR

            WRv[i, :] = WCdiff(SWR[i, -1] / 3, KRe[-1], WRv[i - 1, :], DRe[i, :], KRe[i, :], dgR, nL / 2, dt)
            WGv[i, :] = WCdiff(SWG[i, -1], 0, WGv[i - 1, :], DGe[i, :], KGe[i, :], dgG, nL, dt)

        WGv[i, :] = np.clip(WGv[i, :], Wr, Ws)
        WGi[i, :] = np.clip(WGi[i, :], 0, 1)
        WRv[i, :] = np.clip(WRv[i, :], Wr, Ws)
        WRi[i, :] = np.clip(WRi[i, :], 0, poR)

        WG_nd[i, :] = (WGv[i, :] - Wr) / (Ws - Wr)
        WR_nd[i] = (WRv[i] - Wr) / (Ws - Wr)

        beR[i] = 0.4
        beG[i] = WG_nd[i]

        Tcan[i] = (Ta[i] / Rcan[i] + 2 * h * TWe[i] / RW[i] / w + TGe[i] / RG[i]) / (1 / Rcan[i] + 2 * h / RW[i] / w + 1 / RG[i])

        for j in range(nW):
            HW[i, j] = Cpd * ra[i] * (TWd[i, 1, j] - Tcan[i]) / RW[i]
        for j in range(nG):
            HG[i, j] = Cpd * ra[i] * (TG[i, j] - Ta[i]) / RG[i]

        for j in range(nR):
            qsR[i, j] = qsat(Lv, Rv, Rd, TR[i, j], Pa[i])

              # Compute saturation specific humidity

         for j in range(nG):
             qsG[i, j] = qsat(Lv, Rv, Rd, TG[i, j], Pa[i])

         qG[i, nG - 1] = qsG[i, nG - 1]
         qGe[i] = beG[i] * fG[nG - 1] * qsG[i, nG - 1] + np.dot(WGi[i, :], qsG[i, :nG - 1] * fG[:nG - 1])
         temp = beG[i] * fG[nG - 1] + np.dot(WGi[i, :], fG[:nG - 1])
         qcan[i] = (qa[i] / Rcan[i] + qGe[i] / RG[i]) / (1 / Rcan[i] + temp / RG[i])

         # Compute latent heat fluxes
         LEG[i, :] = ra[i] * Lv * (qsG[i, :] - qa[i]) / RG[i]
         LEG[i, :nG - 1] = WGi[i, :] * LEG[i, :nG - 1]
         LEG[i, nG - 1] = beG[i] * LEG[i, nG - 1]

        # Compute effective heat budgets
        RnR[i, :] = LR[i, :] + SR[i, :]
        RnW[i, :] = LW[i, :] + SW[i, :]
        RnG[i, :] = LG[i, :] + SG[i, :]

       ReW[i] = np.dot(RnW[i, :], fW)
       ReG[i] = np.dot(RnG[i, :], fG)
       ReR[i] = np.dot(RnR[i, :], fR)
       HRe[i] = np.dot(HR[i, :], fR)
       HWe[i] = np.dot(HW[i, :], fW)
       HGe[i] = np.dot(HG[i, :], fG)
       LERe[i] = np.dot(LER[i, :], fR)
       LEGe[i] = np.dot(LEG[i, :], fG)

       # Check convergence
      err = np.array([abs(x1 / qW1[i, 0] - 1), abs(x2 / qR1[i, 0] - 1), abs(x4 / Tcan[i] - 1)])
      emax = np.max(err)

      if emax < tol:
          ok = 1
          break

      # Check max iterations
      if nit0 >= Maxi:
          print("Maximum number of iterations exceeded.")

      niter += nit0  # Total number of iterations

"""Add the below function for flood irrigation"""

if day in [1, 43, 85]:
    if (i - 253) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.01

if day == 343:
    if (i - 541) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.01

if day in [13, 55]:
    if (i - 829) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.01

if day in [313, 355]:
    if (i - 1117) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.01

if day in [25, 67]:
    if (i - 1405) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.01

if day == 325:
    if (i - 1693) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.01

if day in [127, 169, 211, 253, 295]:
    if (i - 253) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.02

if day in [91, 133, 175, 217, 259, 301]:
    if (i - 541) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.02

if day in [97, 139, 181, 223, 265]:
    if (i - 829) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.02

if day in [103, 145, 187, 229, 271]:
    if (i - 1117) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.02

if day in [109, 151, 193, 235, 277]:
    if (i - 1405) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.02

if day in [115, 157, 199, 241, 283]:
    if (i - 1693) % 1728 == 0:
        IRRI[i, 0] = 0.5 - WGv[i, 0]
        WGv[i, 0] += IRRI[i, 0]
        deltaWG[i, 0] += 0.02


# Compute final results
TWd -= KK
TG -= KK
TR -= KK
Tcan -= KK
TWe -= KK
TGe -= KK
TRe -= KK

Tu = r * TRe + w * Tcan
Hu = r * HRe + w * Hcan
LEu = r * LERe + w * LEGe
