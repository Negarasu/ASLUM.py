# -*- coding: utf-8 -*-
"""Another copy of Main.ipynb

"""

import numpy as np
import scipy.io
from UCM import UCM

class UrbanCanyon:
    """Urban Canyon Model - Stores Parameters as Class Attributes """
    # Load meteorological data
    phoenix_data = scipy.io.loadmat('/ASU/data/Phoenix_irri_2012.mat')
    irri_data = scipy.io.loadmat('/ASU/data/Irri_input.mat')

    # Extract time data
    tEC = phoenix_data.get('tEC')
    tEC = tEC.flatten() if tEC is not None else None

    # Time-related variables
    Nd = 6  # Number of days with re-initialization
    nd = 366  # Number of days for simulation
    dt = 300  # Time step in seconds

    if tEC is not None:
        tm = (tEC - tEC[0]) * 24  # Convert time to hours
    else:
        tm = None

    np_ = 288 * Nd  # Total number of points per cycle
    th = np.arange(0, nd + dt / 3600 / 24, dt / 3600 / 24) * 24  # Time vector in hours
    nt = len(th)  # Total number of points
    nnd = nd // Nd  # Number of full cycles
    ty = np.arange(1, nd + 1, Nd)  # Time steps for each cycle
    # ------------------------------
    # Meteorological Data Arrays
    data_dict = {
        "LWDEC": phoenix_data.get("LWDEC"),
        "SWDEC": phoenix_data.get("SWDEC"),
        "LWUEC": phoenix_data.get("LWUEC"),
        "SWUEC": phoenix_data.get("SWUEC"),
        "HEC": phoenix_data.get("HEC"),
        "LEEC": phoenix_data.get("LEEC"),
        "TaEC": phoenix_data.get("TaEC"),
        "TsEC": phoenix_data.get("TsEC"),
        "uEC": phoenix_data.get("uEC"),
        "pEC": phoenix_data.get("pEC"),
        "qaEC": phoenix_data.get("qaEC"),
        "raEC": phoenix_data.get("raEC"),
        "PEC": phoenix_data.get("PEC"),
        "RHEC": phoenix_data.get("RHEC"),
        "SMEC": phoenix_data.get("SMEC"),
        "SMEC2": phoenix_data.get("SMEC2"),
        "SMEC3": phoenix_data.get("SMEC3"),
        "pd_in": irri_data.get('pd'),
        "qa_in": irri_data.get('qa'),
        "Pa_in": irri_data.get('Pa'),
        "LD_in": irri_data.get('LD'),
        "SD_in": irri_data.get('SD'),
        "Ta_in": irri_data.get('Ta'),
        "ra_in": irri_data.get('ra'),
        "Ua_in": irri_data.get('Ua'),
    }

    # Convert to DataFrame and handle missing data
    data_dict_cleaned = {
        key: value.flatten() if value is not None and value.size > 1 else value
        for key, value in data_dict.items() if value is not None
    }

    df = pd.DataFrame(data_dict_cleaned)
    # ------------------------------
    # Geographic Location & Orientation
    # ------------------------------
    Lat = 34.419939  # Latitude [°] (positive north)
    Lon = 111.931380  # Longitude [°] (positive west)
    phi = Lat * np.pi / 180  # Latitude in radians
    lam = Lon * np.pi / 180  # Longitude in radians
    qc = np.pi / 8  # Canyon orientation [rad]

    # ------------------------------
    # Canyon Dimensions
    # ------------------------------
    TB = 24  # Building temperature [°C]
    Za = 21.95  # Reference height [m]
    Zr = 4.5  # Roof level (building height) [m]
    r = 0.5  # Normalized roof width
    w = 1 - r  # Normalized road width
    h = 0.20  # Normalized building height

    # ------------------------------
    # Surface Types & Fractions
    # ------------------------------
    nR, nW, nG = 2, 2, 3  # Roof, Wall, Ground types
    fR = np.array([1.0, 0])  # Roof fractions (normal | green)
    fW = np.array([1.0, 0])  # Wall fractions (brick | glass)
    fG = np.array([0.65, 0, 0.15])  # Ground fractions (asphalt | concrete | vegetated)

    # ------------------------------
    # Roughness Lengths
    # ------------------------------
    ZmR = 0.005  # Momentum roughness length above roof [m]
    Zmc = 0.05  # Momentum roughness length above canyon [m]
    ZhR = ZmR / 10  # Heat roughness length above roof [m]
    Zhc = Zmc / 10  # Heat roughness length above canyon [m]

    # ------------------------------
    # Surface Thermal Properties
    # ------------------------------
    aR = np.array([0.20, 0.20])  # Roof surface albedo
    aW = np.array([0.17, 0.20])  # Wall surface albedo
    aG = np.array([0.17, 0.40, 0.50])  # Ground surface albedo

    eR = np.array([0.95, 0.93])  # Roof surface emissivity
    eW = np.array([0.95, 0.95])  # Wall surface emissivity
    eG = np.array([0.95, 0.98, 0.93])  # Ground surface emissivity

    # ------------------------------
    # Composite Material Properties
    # ------------------------------
    dR = np.array([[0.1, 0.1, 0.1],  # Roof layer thickness (conventional)
                   [0.1, 0.15, 0.2]])  # Roof layer thickness (green)

    dW = np.array([[0.06, 0.06],  # Wall layer thickness
                   [0.06, 0.06],
                   [0.06, 0.06]])

    cR = 1e6 * np.array([[1.4, 1.4, 1.4],  # Heat capacity (conventional roof) [J/K/m³]
                         [2.1, 2.1, 2.8]])  # Heat capacity (green roof) [J/K/m³]

    cW = 1.4e6 * np.ones((3, 2))  # Heat capacity (wall) [J/K/m³]
    cG = 1e6 * np.array([1.4, 2.5, 2.0])  # Heat capacity (ground) [J/K/m³]

    kR = np.array([[0.7, 0.7, 0.7],  # Thermal conductivity (conventional roof) [W/K/m]
                   [1.0, 1.2, 1.2]])  # Thermal conductivity (green roof) [W/K/m]

    kW = np.array([[0.7, 0.7],  # Thermal conductivity (wall) [W/K/m]
                   [0.7, 0.7],
                   [0.7, 0.7]])

    kG = np.array([0.7, 0.7, 1.0])  # Thermal conductivity (ground) [W/K/m]

    nL = 10  # Number of discrete soil layers (for moisture calculations)

    # Thermal diffusivity calculations
    alR = kR / cR
    alG = kG / cG

    # Effective thermal material properties
    eWe = np.dot(fW, eW)
    eGe = np.dot(fG, eG)
    aWe = np.dot(fW, aW)
    aGe = np.dot(fG, aG)
    # ------------------------------
    # Soil & Moisture Parameters
    # ------------------------------
    Ws = 0.48  # Saturated soil water content (soil porosity)

    # qmc = SMEC * Ws * 100  # Volumetric soil moisture in percentage (SMEC needs to be defined separately)

    Wr = 0.08  # Residual soil water content
    Ks = 3.38e-6  # Saturated soil conductivity [m/s]

    dwG = 0.005  # Depth of water-holding ground pavements [m]
    dwR = 0.05  # Depth of roof gravel layer [m]
    dvR = 0.1  # Depth of green roof soil [m]

    poR = 0.5  # Porosity of roof gravel

    # Brooks-Corey Model Parameters
    b = np.array([5.25, 5.0])  # Parameter b in Brooks-Corey model [Vegetated Ground | Green Roof]
    Hs = np.array([0.36, 0.05])  # Parameter Hs in Brooks-Corey model [Vegetated Ground | Green Roof]
    # tree parameters

    rttt = 0.15*w;
    dtt = 0.25*w;
    ht = 5.0;
    # ------------------------------
    # Roughness Length Calculations (Macdonald et al. 1998)
    # ------------------------------
    k = 0.4  # von Kármán constant
    a, b, CD = 4.43, 1.0, 1.2  # Macdonald model coefficients

    d = Zr * (1 + a ** (-r) * (r - 1))  # Displacement height
    Z0 = Zr * (1 - d / Zr) * np.exp(
        -((0.5 * b * CD * (1 - d / Zr) * h / k ** 2) ** (-0.5))
    )  # Roughness length

class Constants:
    """Physical and Environmental Constants"""
    """
    Physical and Environmental Constants
    These constants are commonly used in atmospheric and urban climate models.
    """

    # ------------------------------
    # Model Options
    # ------------------------------
    opt = 1  # Option for radiative model: 1-Kusaka; 2-Masson

    # ------------------------------
    # Fundamental Physical Constants
    # ------------------------------
    KK = 273.15  # Celsius-Kelvin conversion
    Rd = 287  # Gas constant for dry air [J/kg/K]
    Rv = 461.5  # Gas constant for vapor [J/kg/K]
    rW = 1e3  # Density of water [kg/m³]
    Cpd = 1005  # Heat capacity of dry air [J/kg/K]
    Lv = 2.26e6  # Latent heat of vaporization [J/kg]

    # ------------------------------
    # Soil & Roof Discretization (Hydrological Modeling)
    # ------------------------------
    nL = UrbanCanyon.nL  # Number of soil layers (from UrbanCanyon)
    dR = UrbanCanyon.dR  # Roof layer thicknesses (from UrbanCanyon)

    dgG = np.ones(nL) / nL  # Soil layer discretization for vegetated ground
    dgR = np.ones(nL // 2) * (dR[-1, 1] / (nL / 2))  # Green roof discretization

    # ------------------------------
    # Parameters in Brooks-Corey Model for Water Content Diffusion
    # ------------------------------
    b = UrbanCanyon.b  # Brooks-Corey parameter array
    Hs = UrbanCanyon.Hs  # Brooks-Corey Hs parameter array

    bG, bR = b[0], b[1]  # Parameters for ground and roof
    HsG, HsR = Hs[0], Hs[1]  # Parameters for ground and roof

    # ------------------------------
    # Number of Layers for Composite Roof
    # ------------------------------
    _, nRL = UrbanCanyon.kR.shape  # Number of composite roof layers

    def initialize_yearly_results():
        nt = UrbanCanyon.nt   # Total time steps
        nnd = UrbanCanyon.nnd # Number of 5-day averaged time steps

        # Normal data
        TR_UCM  = np.zeros((nt, UrbanCanyon.nR))
        TW_UCM  = np.zeros((nt, UrbanCanyon.nW))
        TG_UCM  = np.zeros((nt, UrbanCanyon.nG))
        TRe_UCM = np.zeros((nt, 1))
        TWe_UCM = np.zeros((nt, 1))
        TGe_UCM = np.zeros((nt, 1))
        H_UCM   = np.zeros((nt, 1))
        LE_UCM  = np.zeros((nt, 1))
        HR_UCM  = np.zeros((nt, 1))
        LER_UCM = np.zeros((nt, 1))
        HG_UCM  = np.zeros((nt, 1))
        LEG_UCM = np.zeros((nt, 1))
        Tcan_UCM= np.zeros((nt, 1))
        RnR_UCM = np.zeros((nt, 1))
        QR_UCM  = np.zeros((nt, 1))
        QW_UCM  = np.zeros((nt, 1))
        QIN_UCM = np.zeros((nt, 1))
        QOUT_UCM= np.zeros((nt, 1))
        IRRI_UCM= np.zeros((nt, 1))
        WR_UCM  = np.zeros((nt, 5))
        WG_UCM  = np.zeros((nt, 10))
        qmR     = np.zeros((1, 5))
        qmG     = np.zeros((1, 10))
        BG_UCM  = np.zeros((nt, 1))
        HW_UCM  = np.zeros((nt, 1))
        SW_UCM  = np.zeros((nt, 1))
        LW_UCM  = np.zeros((nt, 1))

        # 5-day averaged data
        TRey_UCM = np.zeros((nnd, 1))
        Hy_UCM   = np.zeros((nnd, 1))
        LEy_UCM  = np.zeros((nnd, 1))
        HRy_UCM  = np.zeros((nnd, 1))
        LERy_UCM = np.zeros((nnd, 1))
        RnRy_UCM = np.zeros((nnd, 1))
        QRy_UCM  = np.zeros((nnd, 1))
        QWy_UCM  = np.zeros((nnd, 1))
        QRy_abs  = np.zeros((nnd, 1))
        QWy_abs  = np.zeros((nnd, 1))
        WRy_UCM  = np.zeros((nnd, 5))
        WGy_UCM  = np.zeros((nnd, 1))

        # Measured data
        TRy_m = np.zeros((nnd, 1))
        Hy_m  = np.zeros((nnd, 1))
        LEy_m = np.zeros((nnd, 1))
        Rny_m = np.zeros((nnd, 1))

        return locals()

    RnEC=LWDEC+SWDEC-LWUEC-SWUEC
    # Main Simulation Loop
    @staticmethod
    def run_simulation():
        """Main simulation loop for urban canyon processes"""
        for i in range(1, UrbanCanyon.nnd):  # Adjust loop range as necessary
            day = ((i - 1) * UrbanCanyon.Nd + 1) % 366  # Current day of the year

            # Initializing temperatures and soil moisture
            TGi = np.zeros(UrbanCanyon.nG)
            TWi = np.zeros((3, UrbanCanyon.nW))
            GWi = np.zeros((3, UrbanCanyon.nW))
            TRi = np.zeros(UrbanCanyon.nR)

            if i == 1:
                    TWi[0, :, :] = 20
                    GWi[0, :, :] = 0
                    TGi[:] = 20
                    TRi[:] = 20
               else:
                   TWi[0, :, :] = TWd[-1, :, :]
                   GWi[0, :, :] = GW[-1, :, :]
                   TGi[:] = TG[-1, :]
                   TRi[:] = TR[-1, :]
                   deltaWGi = deltaWG[-1]
               if i == 1:
                  qmR = np.full(nR, 12)  # Initial volumetric SWC in ground vegetation
                  qmG = np.full(nG, 12)
               else:
                  qmR = WRv[-1, :] * 100
                  qmG = WGv[-1, :] * 100

              # Meteorological inputs
                 start_idx = (i - 1) * UrbanCanyon.np_
                 end_idx = i * UrbanCanyon.np_ + 1

            if 38 <= i <= 50:
                pd = np.zeros_like(UrbanCanyon.pd_in[start_idx:end_idx])  # Zero precipitation rate
            else:
                pd = UrbanCanyon.pd_in[start_idx:end_idx]  # Precipitation rate from input

            qa = UrbanCanyon.qa_in[start_idx:end_idx]  # Specific humidity
            Pa = UrbanCanyon.Pa_in[start_idx:end_idx]  # Atmospheric pressure
            LD = UrbanCanyon.LD_in[start_idx:end_idx]  # Longwave radiation
            SD = UrbanCanyon.SD_in[start_idx:end_idx]  # Shortwave radiation
            Ta = UrbanCanyon.Ta_in[start_idx:end_idx]  # Air temperature
            ra = UrbanCanyon.ra_in[start_idx:end_idx]  # Air density
            Ua = UrbanCanyon.Ua_in[start_idx:end_idx]  # Wind speed

        print("Simulation completed.")

def run_UCM(i, np_, Nd, day, Ws, Wr, Ks, dwG, dwR, dvR, poR, pd,
                   qa, Pa, LD, SD, Ta, ra, Ua, TWi, TGi, TRi,
                   nR, nW, nG, fR, fW, fG, Za, Zr, r, w, h, ZmR, Zmc, ZhR, Zhc,
                   qc, phi, lam, aR, aW, aG, eR, eW, eG, dR, dW, cR, cW, cG,
                   kR, kW, kG, qmR, qmG, nL, b, Hs, TB,
                   TR_UCM, TG_UCM, TRe_UCM, TWe_UCM, TGe_UCM, Ts_UCM, H_UCM, LE_UCM,
                   HR_UCM, LER_UCM, HG_UCM, LEG_UCM, Tcan_UCM, RnR_UCM, QIN_UCM,
                   WR_UCM, WG_UCM, IRRI_UCM, HW_UCM, LW_UCM, SW_UCM,
                   TRey_UCM, Hy_UCM, LEy_UCM, HRy_UCM, LERy_UCM, RnRy_UCM,
                   QRy_UCM, QWy_UCM, QRy_abs, QWy_abs, WGy_m, RnEC):

    # Call UCM driver function to compute surface energetics
    results = UCM(Nd, day, Ws, Wr, Ks, dwG, dwR, dvR, poR, pd,
                         qa, Pa, LD, SD, Ta, ra, Ua, TWi, TGi, TRi,
                         nR, nW, nG, fR, fW, fG, Za, Zr, r, w, h, ZmR, Zmc, ZhR, Zhc,
                         qc, phi, lam, aR, aW, aG, eR, eW, eG, dR, dW, cR, cW, cG,
                         kR, kW, kG, qmR, qmG, nL, b, Hs, TB)
    # Unpack results from UCM function
    (Hu, LEu, Tu, TR, TWd, GW, TG, TRe, TWe, TGe, Tcan, HRe, LERe,
     QG, QIN, HWe, SWe, LWe, HGe, LEGe, qcan, ReR, WGv, WRv,
     IRRI, Hcan, LEC, ReW, ReG) = results

    # Compute Recan
    Recan = ReG + ReW

    # Write results into one-year vectors
    TR_UCM[(i - 1) * np_:i * np_ + 1, :] = TR
    TG_UCM[(i - 1) * np_:i * np_ + 1, :] = TG
    TRe_UCM[(i - 1) * np_:i * np_ + 1] = TRe
    TWe_UCM[(i - 1) * np_:i * np_ + 1] = TWe
    TGe_UCM[(i - 1) * np_:i * np_ + 1] = TGe
    Ts_UCM[(i - 1) * np_:i * np_ + 1, :] = Tu
    H_UCM[(i - 1) * np_:i * np_ + 1] = Hu
    LE_UCM[(i - 1) * np_:i * np_ + 1] = LEu
    HR_UCM[(i - 1) * np_:i * np_ + 1] = HRe
    LER_UCM[(i - 1) * np_:i * np_ + 1] = LERe
    HG_UCM[(i - 1) * np_:i * np_ + 1] = HGe
    LEG_UCM[(i - 1) * np_:i * np_ + 1] = LEGe
    Tcan_UCM[(i - 1) * np_:i * np_ + 1] = Tcan
    RnR_UCM[(i - 1) * np_:i * np_ + 1] = ReR
    QIN_UCM[(i - 1) * np_:i * np_ + 1] = QIN
    WR_UCM[(i - 1) * np_:i * np_ + 1, :] = WRv
    WG_UCM[(i - 1) * np_:i * np_ + 1, :] = WGv
    IRRI_UCM[(i - 1) * np_:i * np_ + 1, :] = IRRI
    HW_UCM[(i - 1) * np_:i * np_ + 1] = HWe
    LW_UCM[(i - 1) * np_:i * np_ + 1] = LWe
    SW_UCM[(i - 1) * np_:i * np_ + 1] = SWe

    # Yearly averages
    #TRey_UCM[i] = np.nanmean(TRe, axis=0)
    #Hy_UCM[i] = np.nanmean(Hu, axis=0)
    #LEy_UCM[i] = np.nanmean(LEu, axis=0)
    #HRy_UCM[i] = np.nanmean(HRe, axis=0)
    #LERy_UCM[i] = np.nanmean(LERe, axis=0)
    #RnRy_UCM[i] = np.nanmean(ReR, axis=0)
    #QRy_UCM[i] = np.nanmean(QRe, axis=0)
    #QWy_UCM[i] = np.nanmean(QWe, axis=0)

    # Absolute building energy consumption
    #QRy_abs[i] = np.nanmean(np.abs(QRe), axis=0)
    #QWy_abs[i] = np.nanmean(np.abs(QWe), axis=0)

    # Compute mean of RnEC for the given period
    #WGy_m[i] = np.nanmean(RnEC[(i - 1) * np_:i * np_ + 1])

    # Print completion message
    print(f"UCM computation of 6-day-period # {i:3d} is completed......")

"""# **Run the code**"""

from UCM import UCM  # Import the UCM function

for i in range(1, nnd + 1):
    run_UCM(i, np_, Nd, day, Ws, Wr, Ks, dwG, dwR, dvR, poR, pd,
            qa, Pa, LD, SD, Ta, ra, Ua, TWi, TGi, TRi,
            nR, nW, nG, fR, fW, fG, Za, Zr, r, w, h, ZmR, Zmc, ZhR, Zhc,
            qc, phi, lam, aR, aW, aG, eR, eW, eG, dR, dW, cR, cW, cG,
            kR, kW, kG, qmR, qmG, nL, b, Hs, TB,
            TR_UCM, TG_UCM, TRe_UCM, TWe_UCM, TGe_UCM, Ts_UCM, H_UCM, LE_UCM,
            HR_UCM, LER_UCM, HG_UCM, LEG_UCM, Tcan_UCM, RnR_UCM, QIN_UCM,
            WR_UCM, WG_UCM, IRRI_UCM, HW_UCM, LW_UCM, SW_UCM,
            TRey_UCM, Hy_UCM, LEy_UCM, HRy_UCM, LERy_UCM, RnRy_UCM,
            QRy_UCM, QWy_UCM, QRy_abs, QWy_abs, WGy_m, RnEC)
