# -*- coding: utf-8 -*-
"""PlotresPHX.ipynb

"""

import numpy as np
import matplotlib.pyplot as plt
from Main import UrbanCanyon

# Assuming 'th', 'HG_UCM', 'LEG_UCM', 'H_UCM', 'LE_UCM', 'TGe_UCM', 'Tcan_UCM',
# 'Ts_UCM', 'TRe_UCM', 'WG_UCM', 'IRRI_UCM' are defined as NumPy arrays

# Define parameters
ni = UrbanCanyon.ni  # Set appropriate values
np_ = UrbanCanyon.np_  # Set appropriate values
nd = UrbanCanyon.nd  # Example value, should be set based on actual data

# Convert time axis
time_days = UrbanCanyon.th / 24
start_index = ni * np_ + 1
end_index = start_index + nd * np_

# Plot 1: Turbulent heat fluxes
plt.figure(1)
plt.plot(time_days[start_index:end_index], HG_UCM[start_index:end_index], 'r', label='HG_UCM')
plt.plot(time_days[start_index:end_index], LEG_UCM[start_index:end_index], 'g', label='LEG_UCM')
plt.plot(time_days[start_index:end_index], H_UCM[start_index:end_index], 'b', label='H_UCM')
plt.plot(time_days[start_index:end_index], LE_UCM[start_index:end_index], 'k', label='LE_UCM')
plt.xlabel('Simulation time (day)', fontsize=16, fontname='Times New Roman')
plt.ylabel('Turbulent heat fluxes (W/m²)', fontsize=16, fontname='Times New Roman')
plt.xlim([0, nd])
plt.ylim([-200, 400])
plt.legend()
plt.grid()
plt.show()

# Plot 2: Temperature
plt.figure(2)
plt.plot(time_days[start_index:end_index], TGe_UCM[start_index:end_index], 'g', label='TGe_UCM')
plt.plot(time_days[start_index:end_index], Tcan_UCM[start_index:end_index], 'b', label='Tcan_UCM')
plt.plot(time_days[start_index:end_index], Ts_UCM[start_index:end_index], 'k', label='Ts_UCM')
plt.plot(time_days[start_index:end_index], TRe_UCM[start_index:end_index], 'r', label='TRe_UCM')
plt.xlabel('Simulation time (day)', fontsize=16, fontname='Times New Roman')
plt.ylabel('Temperature (°C)', fontsize=16, fontname='Times New Roman')
plt.xlim([0, nd])
plt.ylim([0, 70])
plt.legend()
plt.grid()
plt.show()

# Plot 4: Top layer soil moisture
plt.figure(4)
plt.plot(time_days[start_index:end_index], WG_UCM[start_index:end_index, 0], 'r')
plt.xlabel('Simulation time (day)', fontsize=16, fontname='Times New Roman')
plt.ylabel('Top layer soil moisture', fontsize=16, fontname='Times New Roman')
plt.xlim([0, nd])
plt.grid()
plt.show()

# Plot 5: Irrigation
plt.figure(5)
plt.plot(time_days[start_index:end_index], IRRI_UCM[start_index:end_index, 0], 'r')
plt.xlabel('Simulation time (day)', fontsize=16, fontname='Times New Roman')
plt.ylabel('Irrigation', fontsize=16, fontname='Times New Roman')
plt.xlim([0, nd])
plt.grid()
plt.show()
