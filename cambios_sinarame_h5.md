###sinarame_h5


En el archivo `pyart/pyart/aux_io/sinarame_h5.py` las siguientes líneas deberían ser cambiadas para poder leer los H5 de los RMA.

línea 118: agregar al paréntesis
```python
datasets.sort(key=lambda i: '{0:0>9}'.format(i))
```
Esto hace que los datasets estén ordenados de forma natural (originalmente están dataset1, dataset10, dataset 2, etc. porque lee los nombres como strings)

línea 284: agregar nueva línea (o sea, 285)
```python
if file_field_names is True: fields[field_name].update(filemetadata.get_metadata(field_names[field_name]))
```
En caso de usar nombres distintos de las variables (o sea, TH en vez de total_power por ejemplo) el diccionario perdía todos los metadatos. Como esos datos todavía existen en el diccionario filemetadata los añado a cada key del diccionario fields (field_names es el diccionario con los nombres modificados y origniales; field_name es el nombre modificado que le queda a la variable)

Entiendo que este archivo igualmente está incompleto en algunos de los requerimientos de los desarrolladores de PyART para ponerlo finalmente en io en vez de aux_io.

###sinarame_to_cfradial

En un archivo distinto aproximo lo que ya hizo [Steve](https://github.com/ARM-DOE/pyart/commit/3e3349b515670defe8907d1f6f3f144f7bfd662a) para generar un objeto radar que contenga a todas las variables (y sus metadatos). Hay que definir cómo queda el nombre del archivo, aparentemente es bastante abierto.

```python
import pyart
import glob, os, sys
import datetime #from datetime import datetime
from netcdftime import utime
import numpy as np

files=glob.glob('/home/martin/Escritorio/RMA1_ejemplo/*.H5')
path='/home/martin/Escritorio/RMA1_ejemplo/'

for i in np.arange(len(files)):
    basename=os.path.basename(files[i])
    bs=basename.split('_')
    base1='{b1}_{b2}_{b3}_{fn}_{b4}'.format(b1=bs[0],b2=bs[1],b3=bs[2],fn=bs[3],b4=bs[4])
    file='{path}{base1}'.format(path=path,base1=base1)
    if i==0:
        radar=read_sinarame_h5(file,file_field_names=True)
    else:
        radar_prov=read_sinarame_h5(file,file_field_names=True)
        radar.fields.update(radar_prov.fields)

cal_temps = u"gregorian" # Se usa esto?
cdftime = utime(radar.time['units'])

time1=cdftime.num2date(radar.time['data'][0]).strftime('%Y%m%d_%H%M%S')
time2=cdftime.num2date(radar.time['data'][-1]).strftime('%Y%m%d_%H%M%S')

cffile='cfrad.{time1}.0000_to_{time2}.0000_{b1}_SUR.nc'.format(time1=time1,time2=time2,b1=bs[0])
print cffile

radar._DeflateLevel=5
print('writing to {path}{cffile}'.format(path=path,cffile=cffile))
pyart.io.write_cfradial(path+cffile,radar,format='NETCDF4_CLASSIC')
```
