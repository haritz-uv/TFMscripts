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


fig, axs = plt.subplots(2, 2, figsize=(15,13))

ax_afm= axs[0, 0]
ax_intensity= axs[0, 1]
ax_r2= axs[1, 0]
ax_empty= axs[1, 1] 

# --- Mapa 2: Posición del Pico (Desplazamiento / Strain) ---
image=plt.imread(r"G:\Mi unidad\Experiments\Materials\Multiferroic\hm_zarcillo\08_measurements\20260721\zone01_id11_position_fromAFM.png")
ax_afm.imshow(image, extent=ax_limits)
ax_afm.set_title("AFM image", pad=5)
#ax_afm.set_xlabel("scanner position x (um)")
ax_afm.set_ylabel("scanner position y (um)")
##ax_afm.secondary_xaxis('top', functions=(lambda x: x*(xsize/ax_limits[1]), lambda x:x*(ax_limits[1]/xsize))).set_xlabel("scanner position x (u.a.)")
##ax_afm.secondary_yaxis('right', functions=(lambda y: y*(ysize/ax_limits[3]), lambda y: y*(ax_limits[3]/ysize))).set_ylabel("scanner position y (u.a.)")


im2 = ax_intensity.imshow(intensity_map, cmap='RdBu_r', interpolation='bicubic',origin='lower', vmax=limit_up, vmin=limit_down, extent=ax_limits)
ax_intensity.set_title("Intensity map", pad=5)
ax_intensity.set_xlabel("scanner position x (um)")
#ax_intensity.set_ylabel("scanner position y (um)")
ax_intensity.tick_params(labelleft=False)
#ax_intensity.secondary_xaxis('top', functions=(lambda x: x*(xsize/ax_limits[1]), lambda x:x*(ax_limits[1]/xsize))).set_xlabel("scanner position x (u.a.)")
#ax_intensity.secondary_yaxis('right', functions=(lambda y: y*(ysize/ax_limits[3]), lambda y: y*(ax_limits[3]/ysize))).set_ylabel("scanner position y (u.a.)")
fig.colorbar(im2, ax=ax_intensity, orientation='vertical').ax.set_title("Counts", pad=5, fontsize=10)

im3 = ax_r2.imshow(r2_map, cmap='RdYlGn', origin='lower', vmin=0.85, vmax=1.0, extent=ax_limits)
ax_r2.set_title("Fit Quality (R²)", pad=5)
ax_r2.set_xlabel("scanner position x (um)")
#ax_r2.secondary_xaxis('top', functions=(lambda x: x*(xsize/ax_limits[1]), lambda x:x*(ax_limits[1]/xsize)))
#ax_r2.secondary_yaxis('right', functions=(lambda y: y*(ysize/ax_limits[3]), lambda y: y*(ax_limits[3]/ysize))).set_ylabel("scanner position y (u.a.)")
ax_r2.set_ylabel("scanner position y (um)")
fig.colorbar(im3, ax=ax_r2, orientation='vertical').ax.set_title("R² score", pad=5, fontsize=10)

fig.colorbar(im3, ax=ax_afm).ax.set_visible(False)  # Hide the colorbar for the AFM image

image2=plt.imread(r"G:\Mi unidad\Experiments\Materials\Multiferroic\hm_zarcillo\images\50x_with_borders&letters.png")
ax_empty.imshow(image2, extent=ax_limits)
ax_empty.axis('off')  # Hide the empty subplot
ax_empty.set_title("Device overview", pad=5)
fig.colorbar(im3, ax=ax_empty).ax.set_visible(False)  # Hide the colorbar for the empty subplot
plt.tight_layout()
plt.show()

