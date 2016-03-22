Estas son las cosas que habría que cambiar/arreglar

118: agregar al paréntesis
```python
datasets.sort(key=lambda i: '{0:0>9}'.format(i))
```

284: agregar nueva línea (o sea, 285)
```python
if file_field_names is True: fields[field_name].update(filemetadata.get_metadata(field_names[field_name]))
```

Con estas líneas aproximo lo que ya hizo Steve

```python
import glob, os, sys
import datetime #from datetime import datetime
from netcdftime import utime

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

cal_temps = u"gregorian" 
cdftime = utime(radar.time['units'])

time1=cdftime.num2date(radar.time['data'][0]).strftime('%Y%m%d_%H%M%S')
time2=cdftime.num2date(radar.time['data'][-1]).strftime('%Y%m%d_%H%M%S')

# Hay que definir que se hace aca con el nombre
cffile='cfrad.{time1}.0000_to_{time2}.0000_{b1}_SUR.nc'.format(time1=time1,time2=time2,b1=bs[0])
print cffile

radar._DeflateLevel=5
print('writing to {path}{cffile}'.format(path=path,cffile=cffile))
pyart.io.write_cfradial(path+cffile,radar,format='NETCDF4_CLASSIC')
```
