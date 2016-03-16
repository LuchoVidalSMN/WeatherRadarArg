# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import pyart
import wradlib
import numpy as np
import matplotlib.pyplot as plt
filename='/home/sofia/interferencia/cfrad.20151014_232005.000_to_20151014_232005.000_unknown_v1_object:PVOL_SUR_2.nc'
radar=pyart.io.read(filename)

# Georeferencing and projection
r1=radar.extract_sweeps([0])
ref=r1.fields[u'TH']['data'].data


radar_location = (-58.536512, -34.787591, 57) # (lon, lat, alt) in decimal degree and meters
elevation = 0.38452148 # in degree
ranges = np.arange(0, 240000., 500.) # in meters

azis_1era_ele=radar.get_azimuth(0)
polargrid = np.meshgrid(ranges, azis_1era_ele)
lon, lat, alt = wradlib.georef.polar2lonlatalt_n(polargrid[0], polargrid[1], elevation, radar_location)




# Grafico reflectividad PPI
fig=plt.figure(2,figsize=(8,6))
plt.pcolor(lon,lat,ref,vmin=-32,vmax=70,cmap=plt.cm.jet)
plt.show()


##############con wradlib


filename2='/home/sofia/interferencia/EZE_PPIVol_20151014_232005.hdf'

# Leemos el archivo usando la libreria WRADLIB, ya que el formato es OPERA-H5
raw = wradlib.io.read_OPERA_hdf5(filename2)

# Extraigo las coordenadas del sitio del radar (Lat/Lon y Altura)
sitecoords = (raw["where"]["lon"], raw["where"]["lat"],raw["where"]["height"])

# Extraigo la reflectividad horizontal [dBZ]
where = raw["dataset%d/where"%1]
what  = raw["dataset%d/data2/what"%1]
ref = what["offset"] + what["gain"] * raw["dataset%d/data2/data"%1]


startAZ = raw[u'dataset1/data1/how']['startazA']
stopAZ  = raw[u'dataset1/data1/how']['stopazA']
AZ = (startAZ + stopAZ)/2.0

# Georeferencing and projection
radar_location = (-58.536512, -34.787591, 57) # (lon, lat, alt) in decimal degree and meters
elevation = 0.38452148 # in degree
azimuths = AZ # in degrees
ranges = np.arange(0, 240000., 500.) # in meters
polargrid = np.meshgrid(ranges, azimuths)
lon, lat, alt = wradlib.georef.polar2lonlatalt_n(polargrid[0], polargrid[1], elevation, radar_location)

# Grafico reflectividad PPI
fig=plt.figure(1,figsize=(8,6))
plt.pcolor(lon,lat,ref,vmin=-32,vmax=70,cmap=plt.cm.jet)
plt.show()

