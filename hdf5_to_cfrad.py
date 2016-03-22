# -*- coding: utf-8 -*-
"""
Created on Tue Mar 22 12:25:55 2016

@author: sofia
"""
import os
import numpy as np
import wradlib
import pyart
###filename es la ruta del archivo hdf5 Opera Odim del radar de Ezeiza
def hdf5_to_cfrad(filename):
    path=str('')
    barra='/'
    nombre=filename.split('/')[-1]
    for elemento in filename.split('/')[1:-1]:
        path=path+barra+str(elemento)
    
    os.chdir(path)
    os.system('RadxConvert -f '+nombre+' -outname archivoNc -outdir '+path)
    Nc=path+'/archivoNc'

    radar=pyart.io.read(Nc)
    raw = wradlib.io.read_OPERA_hdf5(filename)
    ##completamos los datos azimuth
    N=radar.nsweeps
    start=0
    for n in range(0,N): 
        r = radar.extract_sweeps([n])
        j=n+1
        radar.azimuth['data'][start:start+r.nrays] = raw['dataset%d/data1/how'%j]['startazA'] ###Suponiendo que todos los starrA son los mismos para todas las variables
        start=start+r.nrays
   
    
#espejamos los datos

    prods = radar.fields.keys()
    for elemento in prods:
        start=0
        data_new=np.ones(radar.fields[str(elemento)]['data'].shape)
    
        for n in range(0,N): 
            r = radar.extract_sweeps([n])
            data=r.fields[str(elemento)]['data']
            nrays=r.nrays
            M=nrays/2
            for i in range(1,nrays):
                if i<M:
                    data_new[i+M+start,]=data[i,]
                if i>=M:
                    data_new[i-M+start,]=data[i,]
                start=start+nrays      
        radar.add_field_like(str(elemento),'New_'+str(elemento),data_new)        
    
    
 ###Eliminar .nc viejo??
    os.remove(path+'/archivoNc')
    name=nombre[:-4]
    pyart.io.cfradial.write_cfradial(name,radar, format='NETCDF4',time_reference=None, arm_time_variables=False)    
    

