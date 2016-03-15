#!/usr/bin/ python

# -*- coding: utf-8 -*-
"""
Created on Fri Feb 26 10:42:18 2016

@author: Luciano Vidal
"""
#------------------------------------------------------------------------------
#------------------------------------------------------------------------------

import wradlib
import numpy as np
#import pylab as pl

#pl.interactive(True)
import datetime as dt
import os
import matplotlib.pyplot as plt

# Path datos
filename='./EZE-PPIVol-20160207-181006.hdf'

# Leemos el archivo usando la libreria WRADLIB, ya que el formato es OPERA-H5
raw = wradlib.io.read_OPERA_hdf5(filename)

# Extraigo las coordenadas del sitio del radar (Lat/Lon y Altura)
sitecoords = (raw["where"]["lon"], raw["where"]["lat"],raw["where"]["height"])

# Extraigo la reflectividad horizontal [dBZ]
where = raw["dataset%d/where"%1]
what  = raw["dataset%d/data2/what"%1]
ref = what["offset"] + what["gain"] * raw["dataset%d/data2/data"%1]

# Extraigo el campo de velocidad Doppler [m/s]
where = raw["dataset%d/where"%1]
what  = raw["dataset%d/data3/what"%1]
vr  = what["offset"] + what["gain"] * raw["dataset%d/data3/data"%1]

# Grafico reflectividad B-scope
fig=plt.figure(1,figsize=(8,6))
plt.pcolor(ref[:,:],vmin=-32,vmax=70,cmap=plt.cm.jet)
plt.show()

# Grafico velocidad Doppler B-scope
fig=plt.figure(2,figsize=(8,6))
plt.pcolor(vr[:,:],vmin=-6,vmax=6,cmap=plt.cm.jet)
plt.show()

#------------------------------------------------------------------------------
#------------------------------------------------------------------------------
