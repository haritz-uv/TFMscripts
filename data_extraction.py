# -*- coding: utf-8 -*-
"""
Created on Tue May  5 09:43:35 2026

@author: hment
"""

import qcodes as qc
from qcodes.dataset import load_by_id
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.optimize import curve_fit
from scipy.signal import medfilt
from peak_track_functions import pv, peak_track
import os


qc.config['core']['db_location'] = r"G:\Mi unidad\Experiments\Materials\Multiferroic\hm_zarcillo\08_measurements\20260721\Ferroelectric_CIPS_WSe2_zarcillo.db"
dataset=load_by_id(11)
xr_data=dataset.to_xarray_dataset()

y_matrix=xr_data['camera_spectrum'].values
x_data=xr_data['camera_pixel_x_axis'].values

xsize=y_matrix.shape[0]
ysize=y_matrix.shape[1]

intensity_map=np.zeros((xsize,ysize))
position_map=np.zeros((xsize,ysize))
r2_map = np.zeros((xsize,ysize))

conversion_px_to_um= 5/429.225  #conversion factor from pixels to micrometers (um) based on AFM calibration

ax_limits = [0, 1944 * conversion_px_to_um, 0, 1957 * conversion_px_to_um]  # [xmin, xmax, ymin, ymax]


for i in range(xsize):
    for j in range(ysize):
        y_data=y_matrix[i,j,:]
        popt, pcov, r2= peak_track(x_data, y_data)
        intensity_map[i,j]=popt[0]
        position_map[i,j]=popt[2]
        r2_map[i,j]=r2
print('peak mean value is ', np.round(np.mean(position_map),2))

deviation=np.round(position_map-np.mean(position_map),2)

limit_up = np.nanpercentile(intensity_map, 100)
limit_down = np.nanpercentile(intensity_map, 30)


fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18,5), layout='constrained')

# --- Mapa 2: Posición del Pico (Desplazamiento / Strain) ---
image=plt.imread(r"G:\Mi unidad\Experiments\Materials\Multiferroic\hm_zarcillo\08_measurements\20260721\zone01_id11_position_fromAFM.png")
ax1.imshow(image, extent=ax_limits)
ax1.set_title("AFM image")
ax1.set_xlabel("scanner position x (um)")
ax1.set_ylabel("scanner position y (um)")

im2 = ax2.imshow(intensity_map, cmap='RdBu_r', interpolation='bicubic',origin='lower', vmax=limit_up, vmin=limit_down, extent=ax_limits)
ax2.set_title("Intensity map")
ax2.set_xlabel("scanner position x (um)")
ax2.tick_params(labelleft=False)
#ax2.set_ylabel("scanner position y (um)")
fig.colorbar(im2, ax=ax2, label="Counts")

im3 = ax3.imshow(r2_map, cmap='RdYlGn', origin='lower', vmin=0.85, vmax=1.0, extent=ax_limits)
ax3.set_title("Fit Quality (R²)")
ax3.set_xlabel("scanner position x (um)")
#ax3.set_ylabel("scanner position y (um)")
ax3.tick_params(labelleft=False)  
fig.colorbar(im3, ax=ax3, label="R² score")

#for i in range(xsize):
#    for j in range(ysize):
#        # Escribe el número con 3 decimales
#        if r2_map[i, j] > 0.85:
#            ax3.text(j, i, f"{r2_map[i, j]:.3f}", 
#                    ha="center", va="center", 
#                    color="black" if r2_map[i, j] > 0.92 else "white", 
#                    fontsize=5, fontweight='bold')

plt.show()

