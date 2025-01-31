# -*- coding: utf-8 -*-
"""ASLUMPy.py

"""

from google.colab import drive
drive.mount('/content/drive')

# Commented out IPython magic to ensure Python compatibility.
# %cd '/content/drive/MyDrive/ASLUMpy'

import numpy as np
import scipy.io as sio
import pandas as pd
import  pickle
import matplotlib.pyplot as plt
from scipy.integrate import trapz
from scipy.spatial.distance import cdist
from scipy.io import loadmat
from scipy.special import erfc
from datetime import datetime
from dateutil.parser import parse
from datetime import datetime, timedelta
from decimal import Decimal, getcontext
import math
np.random.seed(30)
pause = int(32) # just for debugging purposes
# 1. load meteorological forcing data from EC station

!pip install seaborn

!pip install flake8

# Commented out IPython magic to ensure Python compatibility.
# %%capture
# !pip install black

import seaborn as sns
sns.set(style="whitegrid")

#np.random.seed(30)
#pause = int(32) # just for debugging purposes
#getcontext().prec = 20

#you can use the loadmat for loading your data regarding your directory
Phoenix_calibrate_Pre3 = sio.loadmat(r'/content/drive/MyDrive/ASLUMpy/Phoenix_calibrate_Pre3.mat')
Phoenix_irri_2012 = sio.loadmat(r'/content/drive/MyDrive/ASLUMpy/Phoenix_irri_2012.mat')
irri_input = sio.loadmat(r'/content/drive/MyDrive/ASLUMpy/Irri_input.mat')

LWDEC = Phoenix_irri_2012['LWDEC']
SWDEC = Phoenix_irri_2012['SWDEC']
LWUEC = Phoenix_irri_2012['LWUEC']
SWUEC = Phoenix_irri_2012['SWUEC']
HEC = Phoenix_irri_2012['HEC']
LEEC = Phoenix_irri_2012['LEEC']
TaEC = Phoenix_irri_2012['TaEC']
TsEC = Phoenix_irri_2012['TsEC']
uEC = Phoenix_irri_2012['uEC']
pEC = Phoenix_irri_2012['pEC']
SMEC = Phoenix_irri_2012['SMEC']
SMEC2 = Phoenix_irri_2012['SMEC2']
SMEC3 = Phoenix_irri_2012['SMEC3']
raEC = Phoenix_irri_2012['raEC']
PEC = Phoenix_irri_2012['PEC']
qaEC = Phoenix_irri_2012['qaEC']
tEC = Phoenix_irri_2012['tEC']
RHEC = Phoenix_irri_2012['RHEC']
qa_in = irri_input['qa_in']
Pa_in = irri_input['Pa_in']
LD_in = irri_input['LD_in']
SD_in = irri_input['SD_in']
Ta_in = irri_input['Ta_in']
ra_in = irri_input['ra_in']
Ua_in = irri_input['Ua_in']
pd_in = irri_input['pd_in']

Nd = 6
ny = 48 * Nd
npp = 288 * Nd
nd = 366                             # number of days with re-initialization
tm = (tEC-tEC[0])*24                # adjust time format for EC data
nnd = math.floor(nd / Nd)
ty = np.arange(1, nd+1, Nd)

for i in range(36):  # Loop from 1 to 6 (inclusive)
    day = ((i - 1) * Nd + 1) % 366  # Current day of year
# Write results into one-year vectors
TRe= np.array(TRe_UCM[(i - 1) * npp:i * npp + 1, :])
TG=np.array(TGe_UCM[(i - 1) * npp:i * npp + 1, :])
TWe=np.array(TWe_UCM[(i - 1) * npp:i * npp + 1])
Tu=np.array(Ts_UCM[(i - 1) * npp:i * npp + 1, :])
Hu=np.array(H_UCM[(i - 1) * npp:i * npp + 1])
LEu=np.array(LE_UCM[(i - 1) * npp:i * npp + 1])
HRe=np.array(HR_UCM[(i - 1) * npp:i * npp + 1])
IRRI=np.array(IRRI_UCM[(i - 1) * npp:i * npp + 1, :])
HGe=np.array(HG_UCM[(i - 1) * npp:i * npp + 1])
LEGe=np.array(LEG_UCM[(i - 1) * npp:i * npp + 1])
Tcan=np.array(Tcan_UCM[(i - 1) * npp:i * npp + 1])
ReR=np.array(RnR_UCM[(i - 1) * npp:i * npp + 1])
QIN=np.array(QIN_UCM[(i - 1) * npp:i * npp + 1])
WRv=np.array(WR_UCM[(i - 1) * npp:i * npp + 1, :])
WGv=np.array(WG_UCM[(i - 1) * npp:i * npp + 1, :])
LERe=np.array(LER_UCM[(i - 1) * npp:i * npp + 1])
TWe=np.array(TWe_UCM[(i - 1) * npp:i * npp + 1])
HWe=np.array(HW_UCM[(i - 1) * npp:i * npp + 1])
LWe=np.array(LW_UCM[(i - 1) * npp:i * npp + 1])
SWe=np.array(SW_UCM[(i - 1) * npp:i * npp + 1])

# Canyon dimensions with partitioned facets
TB = 24  # building temperature [oC]
nR = 2  # roof types: normal||green
nW = 2  # wall types: brick||glass
nG = 3  # ground types: asphalt||concrete||vegetated

fR = [1.0, 0]  # fraction for each type of roof
fW = [1.0, 0]  # fraction for each type of wall
fG = [0.65, 0, 0.35]  # fraction for each type of ground

Za = 21.95  # reference height [m]
Zr = 4.5  # roof level (building height)[m]
r = 0.5  # normalized roof width
w = 1 - r  # normalized road width
h = 0.20  # normalized building height

ZmR = 0.005  # momentum roughness length above roof [m]
Zmc = 0.05  # momentum roughness length above canyon [m]
ZhR = ZmR / 10  # heat roughness length above roof [m]
Zhc = Zmc / 10  # heat roughness length above canyon [m]

# Canyon orientation and location ! don't change
qc = np.pi / 8  # canyon orientation [rad]
Lat = 34.419939  # Latitude (positive north)
Lon = 111.931380  # Longitude (postive west)
phi = Lat * np.pi / 180  # latitude positive north [rad]
lam = Lon * np.pi / 180  # longitude positive west [rad]

# Surface thermal properties: 2nd roof properties are of green roof
aR = np.array([0.10, 0.20])  # roof surface albedo
aW = np.array([0.17, 0.20])  # wall surface albedo
aG = np.array([0.17, 0.40, 0.15])  # ground surface albedo

eR = np.array([0.95, 0.93])  # roof surface emissivity
eW = np.array([0.95, 0.95])  # wall surface emissivity
eG = np.array([0.95, 0.98, 0.93])  # ground surface emissivity

# Modified as three-layer composite roof
dR = np.array([[0.1, 0.1, 0.1]])  # thickness of conventional roof
dG = np.array([[0.1, 0.15, 0.2]]) # thickness of green roof
dW = np.array([[0.06, 0.06], [0.06, 0.06], [0.06, 0.06]])  # partition of wall layer

# Modified as three-layer composite roof
cR = 1e6 * np.array([[1.4, 1.4, 1.4], [2.1, 2.1, 2.8]])  # heat capacity of conventional roof [J/K/m3]
cW = 1.4e6 * np.ones((3, 2))  # heat capacity of wall [J/K/m3]
cG = 1e6 * np.array([1.4, 2.5, 2.0])  # heat capacity of ground [J/K/m3]

# Modified as three-layer composite roof
kR = np.array([[0.7, 0.7, 0.7], [1, 1.2, 1.2]])  # thermal conductivity of conventional roof [W/K/m]
kW = 0.7 * np.ones((3, 2))  # thermal conductivity of wall [W/K/m]
kG = np.array([0.7, 0.7, 1.0])  # thermal conductivity of ground [W/K/m]

nL = 10  # number of discrete layers (for soil moisture)

# Soil parameters
Ws = 0.48  # saturated soil water content (soil porosity)
qmc = SMEC * Ws * 100  # volumetric soil moisture in percentage
Wr = 0.08  # residual soil water content
Ks = 3.38e-6  # saturated conductivity [m/s]
dwG = 0.005  # depth of water-holding ground pavements
dwR = 0.05  # depth of roof gravel layer
dvR = 0.1  # depth of green roof soil
poR = 0.5  # porosity of roof gravel
b = np.array([5.25, 5.0])  # parameter b in bc model [Veg. Ground|Green Roof]
Hs = [0.36, 0.05]  # parameter Hs in bc model [Veg. Ground|Green Roof]

RnEC = LWDEC + SWDEC - LWUEC - SWUEC

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

"""**In this part, i range depends on which day is considered for computations**"""

for i in range(1:36):  # Loop from 1 to 6 (inclusive)
    day = ((i - 1) * Nd + 1) % 366  # Current day of year
# Using Initial arrays:
qmR = np.zeros((1, 5))
qmG = np.zeros((1, 10))
GW = np.zeros((nt, 3, nW))
for i in range(1, nnd + 1):
    day = ((i - 1) * Nd + 1) % 366  # current day of year

    # Initializing surface temperatures and soil moisture
    TGi = np.zeros(nG)
    TWi = np.zeros((3, nW))
    GWi = np.zeros((3, nW))
    TRi = np.zeros(nR)

    if i == 1:
        TWi[0, :] = 20
        GWi[0, :] = 0
        TGi[0] = 20
        TRi[0] = 20
    #else:
        #TWd = TWi[0]
        #GW = GWi[0]
        #TG_1 = TGi[0]
        #TG_2 = TGi[1]
        #TG_3 = TGi[2]
       # TR = TRi[0]
        #TRm = TRi[0]

    #if i == 1:
        qmR[0] = 12  # initial volumetric SWC in ground vegetation
        qmG[0] = 12
   # else:
        #WRv = qmR[0] / 100
        #WGv = qmG[0] / 100

    # qmi = qmc[(i - 1) * 48]  # initial roof/wall temperature from EC

if 38 <= i <= 50:
    pd = pd_in[(i - 1) * npp: i * npp + 1] * 0  # precipitation rate [m/s]
else:
    pd = pd_in[(i - 1) * npp: i * npp + 1]  # precipitation rate [m/s]

qa = qa_in[(i - 1) * npp: i * npp + 1]  # specific humidity [kg/kg]
Pa = Pa_in[(i - 1) * npp: i * npp + 1]  # atmospheric pressure [Pa]
LD = LD_in[(i - 1) * npp: i * npp + 1]  # downwelling longwave radiation
SD = SD_in[(i - 1) * npp: i * npp + 1]  # downwelling shortwave radiation
Ta = Ta_in[(i - 1) * npp: i * npp + 1]  # virtual air temperature [°C]
ra = ra_in[(i - 1) * npp: i * npp + 1]  # air density
Ua = Ua_in[(i - 1) * npp: i * npp + 1]  # wind speed

# 1-day averaged data
TGey_UCM = np.zeros(nnd)
HGy_UCM = np.zeros(nnd)
HRy_UCM = np.zeros(nnd)
LEGy_UCM = np.zeros(nnd)
Tcany_UCM = np.zeros(nnd)
TRy_UCM = np.zeros(nnd)
Ty_UCM = np.zeros(nnd)
Hy_UCM = np.zeros(nnd)
LEy_UCM = np.zeros(nnd)
RnRy_UCM = np.zeros(nnd)
for i in range(1, nnd):
    start_idx = (i - 1) * npp
    end_idx = i * npp + 1

    TGey_UCM[i-1] = np.nanmean(TGe_UCM[start_idx:end_idx])
    HRy_UCM[i-1] = np.nanmean(HR_UCM[start_idx:end_idx])
    HGy_UCM[i-1] = np.nanmean(HG_UCM[start_idx:end_idx])
    LEGy_UCM[i-1] = np.nanmean(LEG_UCM[start_idx:end_idx])
    Tcany_UCM[i-1] = np.nanmean(Tcan_UCM[start_idx:end_idx])
    TRy_UCM[i-1] = np.nanmean(TRe_UCM[start_idx:end_idx])
    Ty_UCM[i-1] = np.nanmean(Ts_UCM[start_idx:end_idx])
    Hy_UCM[i-1] = np.nanmean(H_UCM[start_idx:end_idx])
    LEy_UCM[i-1] = np.nanmean(LE_UCM[start_idx:end_idx])
    RnRy_UCM[i-1] = np.nanmean(RnR_UCM[start_idx:end_idx])

Tsy_m = np.zeros(nnd)
Hy_m = np.zeros(nnd)
LEy_m = np.zeros(nnd)
Rny_m = np.zeros(nnd)
for i in range(1, nnd):
    start_idx = (i - 1) * ny
    end_idx = i * ny

    Tsy_m[i-1] = np.nanmean(TsEC[start_idx:end_idx])
    Hy_m[i-1] = np.nanmean(HEC[start_idx:end_idx])
    LEy_m[i-1] = np.nanmean(LEEC[start_idx:end_idx])
    Rny_m[i-1] = np.nanmean(RHEC[start_idx:end_idx])

TGey_UCM = np.zeros(nnd)
HGy_UCM = np.zeros(nnd)
HRy_UCM = np.zeros(nnd)
LEGy_UCM = np.zeros(nnd)
Tcany_UCM = np.zeros(nnd)
TRy_UCM = np.zeros(nnd)
Ty_UCM = np.zeros(nnd)
Hy_UCM = np.zeros(nnd)
LEy_UCM = np.zeros(nnd)
RnRy_UCM = np.zeros(nnd)
for i in range(1, nnd):
    start_idx = (i - 1) * npp
    end_idx = i * npp + 1

    TGey_UCM[i-1] = np.nanmean(TGe_UCM[start_idx:end_idx])
    HRy_UCM[i-1] = np.nanmean(HR_UCM[start_idx:end_idx])
    HGy_UCM[i-1] = np.nanmean(HG_UCM[start_idx:end_idx])
    LEGy_UCM[i-1] = np.nanmean(LEG_UCM[start_idx:end_idx])
    Tcany_UCM[i-1] = np.nanmean(Tcan_UCM[start_idx:end_idx])
    TRy_UCM[i-1] = np.nanmean(TRe_UCM[start_idx:end_idx])
    Ty_UCM[i-1] = np.nanmean(Ts_UCM[start_idx:end_idx])
    Hy_UCM[i-1] = np.nanmean(H_UCM[start_idx:end_idx])
    LEy_UCM[i-1] = np.nanmean(LE_UCM[start_idx:end_idx])
    RnRy_UCM[i-1] = np.nanmean(RnR_UCM[start_idx:end_idx])
Tsy_m = np.zeros(nnd)
Hy_m = np.zeros(nnd)
LEy_m = np.zeros(nnd)
Rny_m = np.zeros(nnd)
for i in range(1, nnd):
    start_idx = (i - 1) * ny
    end_idx = i * ny

    Tsy_m[i-1] = np.nanmean(TsEC[start_idx:end_idx])
    Hy_m[i-1] = np.nanmean(HEC[start_idx:end_idx])
    LEy_m[i-1] = np.nanmean(LEEC[start_idx:end_idx])
    Rny_m[i-1] = np.nanmean(RHEC[start_idx:end_idx])

"""**Sample graph - time series**"""

# Plotting the data
plt.figure(1)
th = np.arange(0, 367, 300/3600/24) * 24   # time in hours
th = th[:105409]
# Plotting
plt.plot(th, TGe_UCM, 'g', label='TGe_UCM', linewidth=0.5)
plt.plot(th, Tcan_UCM, 'b', label='Tcan_UCM', linewidth=0.5)
plt.plot(th, Ts_UCM, 'k', label='Ts_UCM', linewidth=0.5)
plt.plot(th, TRe_UCM, 'r', label='TRe_UCM', linewidth=0.5)

# Setting labels and limits
plt.xlabel('Simulation time (day)', fontsize=16, fontname='times')
plt.ylabel('Temperature (°C)', fontsize=16, fontname='times')
plt.xlim([0, nd]) #day
plt.ylim([-20, 70])

# Setting font properties
plt.tick_params(axis='both', which='major', labelsize=16)
plt.legend(fontsize=16)

# Setting font for the legend
plt.legend(fontsize=16, frameon=False)

# Show plot
plt.show()
