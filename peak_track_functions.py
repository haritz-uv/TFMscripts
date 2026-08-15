import numpy as np
from scipy.optimize import curve_fit
from scipy.signal import medfilt

def gaussian(x, amp, x0, sigma):
    return  amp*np.exp(-(x - x0)**2/(2 * sigma**2))

def lorentzian(x, amp, x0, gamma):
    return amp*gamma**2/((x-x0)**2+gamma**2) 

def pv(x,A,eta,x0,w, offset):
    """
    PSEUDO-VOIGT
    A: Amplitude
    x0: max central position
    w: Full width at half maximum
    sigma: Gaussian width w = 2*sqrt(2*ln(2))*sigma
    gamma: Lorentzian width w = w*gamma
    eta: weigth of each component (0 = purely gaussian, 1 = purely Lorentzian)
    offset: background noise

    """
    sigma = w/2.35482
    gamma=w/2.0
    g = gaussian(x, 1, x0, sigma)
    l = lorentzian(x, 1, x0, gamma)
    return A*(eta*l+(1-eta)*g)+offset

def peak_track(x_data, y_data, roi=[300,1200], noise_treshold=25, kernel=21):
    
    '''Adjust the given data using scipy curve_fit and then 
    calculates the maximum. Returns:
        popt:[amplitude, eta, x0, w, offset]
        pcov:covariance
            '''
    
    
    A_guess = np.max(y_data)-np.min(y_data)
    x0_guess = x_data[np.argmax(y_data)]
    offset_guess = np.min(y_data)
    w_guess=50.0
    p0 = [A_guess, 0.5, x0_guess, w_guess, offset_guess]
    limits = ([0,0,0,0.1, 0],[np.inf, 1, 1600, np.inf, np.inf])

    '''Here we use a filter to try and erase the cosmic rays peaks, we do a medium filter, 
    calculate the points above some treshold and substitute them for adjusted ones, also
    a ROI filter is included
    '''
    filt=(x_data > roi[0]) & (x_data < roi[1])     
    y_mask=medfilt(y_data, kernel_size=kernel)
    dif=y_data-y_mask
    mask=dif>noise_treshold
    y_clean=y_data.copy()
    y_clean[mask]=y_mask[mask]
    y_ROI=y_clean[filt]
    x_ROI=x_data[filt]
    try:
        popt, pcov = curve_fit(pv, x_ROI, y_ROI, p0=p0, bounds = limits)
        y_fit=pv(x_ROI, *popt)
        residue=y_ROI-y_fit
        ss_res = np.sum(residue**2)
        ss_tot = np.sum((y_ROI - np.mean(y_ROI))**2)
        r2 = 1-(ss_res / ss_tot)
    except RuntimeError:
    
        print('no fit')
        popt=[np.nan,np.nan,np.nan,np.nan,np.nan]
        pcov=np.nan
        r2=0
    
    return popt, pcov, r2

