
import sys
### general purpose
import os
import numpy as np
import xarray as xr
import pandas as pd
### palette
import matplotlib.cm as mplcm
import matplotlib.ticker as mticker
#import matplotlib.cm as cm
#div_cmap = mplcm.seismic
import cmocean
from cmocean import cm
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import scipy.io as sio



# Recherche de la position - Pour un tourbillon cyclonique


def position(box,Dim):
    
    ### Recherche la position du centre par le maximum de SSH ###
    
    max = -100
    a = 0
    b = 0

    for i in range(Dim[0], Dim[1]+1):                            #Horizontale
        for j in range(Dim[2], Dim[3]+1):                        #Verticale
            if box[j][i] > max:
                max = box[j][i]
                a = i
                b = j
            
    return (a,b)  # (H,V)

def Tracking(m, box, path, PosIni):
    
    ### Suivi du tourbillon sur le mois m (string),
    ### pour une boite de 'box' pixels qui recherche le nouveau centre (i+1) 
    ### dans la boite centree sur le centre a l etape i
    ### Path : chemin incomplet vers le fichier a analyser
    ### PosIni : position initiale du tourbillon que l on veut suivre
    
    DimBoite = [0,0,0,0]
    ListePosition = []
    nbjours = 0

    if (m == '01' or m == '03' or m == '05' or m == '07' or m == '08' or m == '10' or m == '12'):
        nbjours = 31
    elif (m == '02'):
        nbjours = 28
    else:
        nbjours = 30
        
    for i in range(1, nbjours+1):
        day = i
        if i<10:
            d = '0' + str(day)
        else:
            d = str(day)
        SSHfile = path + m + 'd' + d + '.1d_SSHMXL.nc'
        from netCDF4 import Dataset
        f = Dataset(SSHfile, "r", format="NETCDF4")
        SSH = f.variables['sossheig'][0]
        if i == 1:
            DimBoite = PosIni
            (hor, ver) = position(SSH, DimBoite)
        else:
            (hor, ver) = position(SSH, DimBoite)
        ListePosition.append([hor,ver])
        DimBoite = [hor-box,hor+box,ver-box,ver+box]
        
    return ListePosition
