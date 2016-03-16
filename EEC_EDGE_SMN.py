
# coding: utf-8

# # Reading and plotting EEC EDGE radar data

# In[119]:

get_ipython().magic(u'matplotlib inline')
import wradlib
import shapefile
import gc
from matplotlib import pyplot as plt
import numpy as np
import matplotlib.colors as colors


# ## Read and inspect data from Ezeiza (Argentina)

# In[120]:

filename='EZE-PPIVol-20151014-232005.hdf'
print filename


# In[121]:

raw = wradlib.io.read_OPERA_hdf5(filename)


# In[122]:

# Here you can inspect whichever directory you want, e.g.
print "where...\n", raw['where'],"\n"
print "what...\n", raw['what'],"\n"
print "dataset1/data1/what...\n", raw['dataset1/data2/what']


# ## Convert selected fields to target units

# In[123]:

def convert(dset, dir):
    """Converts ODIM_H5 data representations to values in target unit and masks missing values.
    
    Parameters
    ----------
    dset : the hdf5 object returned by wradlib.read_OPERA_hdf5
    dir : the corresponding directory tree in dset for which the data should be processed
    
    """
    res = dset[dir+"/data"].astype(np.uint16)
    try:
        res = res * dset[dir+"/what"]["gain"] + dset[dir+"/what"]["offset"]
    except:
        pass
    try:
        res[dset[dir+"/data"]==dset[dir+"/what"]["nodata"]] = np.nan
    except:
        pass
    try:
        res[dset[dir+"/data"]==dset[dir+"/what"]["undetect"]] = np.nan
    except:
        pass    

    return res  


# In[124]:

# Extract specific data arrays from ODIM_h5 objects
# dBZH elev1
PPI_ZH = convert(raw, "dataset1/data2")
PPI_V  = convert(raw, "dataset1/data3")


# ## Collect all the information required for georeferencing

# In[125]:

# Collect all the georeferencing information we need
#   First gate
r0 = raw['dataset1/where']["rstart"]*1000.
#   Gate length
rscale = raw['dataset1/where']["rscale"]
#   Number of bins per beam
nbins = raw['dataset1/where']["nbins"]
#   Maximum range
maxr = r0 + (nbins)*rscale
# Construct array of range gates
r = np.linspace(r0, maxr, nbins)
r = r*0.001
# Construct array of azimuth angles (quick and dirty)
az = np.linspace(0, 359, raw['dataset1/where']["nrays"])
# Site coordinates (lon,lat)
site = raw["where"]["lon"], raw["where"]["lat"]
# Define a projection (Azimuthal Equidistant)
proj = wradlib.georef.create_osr("aeqd", lon_0=site[0], lat_0=site[1])


# In[92]:

nws_reflectivity_colors = [
    "#646464", # ND
    "#ccffff", # -30
    "#cc99cc", # -25
    "#996699", # -20
    "#663366", # -15
    "#cccc99", # -10
    "#999966", # -5
    "#646464", # 0
    "#04e9e7", # 5
    "#019ff4", # 10
    "#0300f4", # 15
    "#02fd02", # 20
    "#01c501", # 25
    "#008e00", # 30
    "#fdf802", # 35
    "#e5bc00", # 40
    "#fd9500", # 45
    "#fd0000", # 50
    "#d40000", # 55
    "#bc0000", # 60
    "#f800fd", # 65
    "#9854c6", # 70
    "#fdfdfd" # 75
    ]
cmap2 = colors.ListedColormap(nws_reflectivity_colors)


# ## Plot a PPI

# In[118]:

f = plt.figure(figsize = [15,12])

ax = plt.subplot(221, aspect="equal")

ax, pm = wradlib.vis.plot_ppi(np.ma.masked_invalid(PPI_ZH), ax=ax, r=r, az=az, site=site, proj=proj, vmin=-35, vmax=80, cmap=cmap2)
ax = wradlib.vis.plot_ppi_crosshair(site=site, ranges=[60, 120, 180, 240], angles=[0, 45, 90, 135, 180, 225, 270], 
                                        proj=proj, elev=0.0, ax=ax)

# set axes labels
plt.xlabel("X-distance (km)", fontsize="large")
plt.ylabel("Y-distance (km)", fontsize="large")
# set axes range
plt.xlim(-250, 250)
plt.ylim(-250, 250)
# set colorbar
cbar = plt.colorbar(pm, orientation="vertical", pad=0.05, extend="neither")
cbar.set_label("dBZ", fontsize="large")
# set title
plt.title("Horizontal reflectivity", fontsize="16")



ax = plt.subplot(222, aspect="equal")

ax, pm = wradlib.vis.plot_ppi(np.ma.masked_invalid(PPI_V), ax=ax, r=r, az=az, site=site, proj=proj, vmin=-6, vmax=6)
ax = wradlib.vis.plot_ppi_crosshair(site=site, ranges=[60, 120, 180, 240], angles=[0, 45, 90, 135, 180, 225, 270], 
                                        proj=proj, elev=0.0, ax=ax)

# set axes labels
plt.xlabel("X-distance (km)", fontsize="large")
plt.ylabel("Y-distance (km)", fontsize="large")
# set axes range
plt.xlim(-250, 250)
plt.ylim(-250, 250)
# set colorbar
cbar = plt.colorbar(pm, orientation="vertical", pad=0.05, extend="neither")
cbar.set_label("m/s", fontsize="large")
# set title
plt.title("Radial velocity", fontsize="16")

plt.savefig('prueba.png',dpi=100,transparent=False)

