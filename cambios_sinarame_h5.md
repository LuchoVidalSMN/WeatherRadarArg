#### For english version [see below](https://github.com/LuchoVidalSMN/WeatherRadarArg_SMN_INTA/blob/master/cambios_sinarame_h5.md#english-version)

### sinarame_h5


En el archivo `pyart/pyart/aux_io/sinarame_h5.py` las siguientes líneas deberían ser cambiadas para poder leer los H5 de los RMA.

- línea 118: agregar al paréntesis

```python
datasets.sort(key=lambda i: '{0:0>9}'.format(i))
```
Originalmente no había nada entre los paréntesis indicando que Python ordenaba la lista sin argumentos. Esto hacía que el orden fuese lexicográfico resultando que `dataset10` estuviese antes que `dataset2` debido a que se compara caracter a caracter; entonces siendo iguales todos los caracteres en `dataset`, al comparar el elemento siguiente (número) el 1 viene antes que el 2. El problema es que al armar el array con los datos, este se basa en el orden de la lista `datasets` haciendo que la décima elevación estuviese antes que la segunda.

Como entender lo que hace pide sort con esta función lambda me fue bastante complejo voy a detallarlo:
- `key` itera sobre los i elementos de la lista datasets.
- Las llaves indican una sustitución.
- Cada elemento i sera formateado siguiendo lo que hay entre las llaves.
 - El primer `0` indica al elemento 0 (o sea, el primero) dentro de `format` (en este caso el único).
 - Después del `:` viene el formato que se aplicará.
 - Los 3 caracteres siguientes indican *fill, align y minimumwidth* respectivamente según [PEP3101](https://www.python.org/dev/peps/pep-3101); en este caso completa con ceros, alineando a la derecha hasta llegar a un mínimo de 9 caracteres.

El orden finalmente queda lexicográfico pero los keys para ordenar ahora son: `0dataset1`,`0dataset2`, ..., `0dataset9`,`dataset10` debido a que ahora la comparación del primer caracter no es solamente con la letra `d` (como sucedía previamente) sino con los caracteres `0` y `d`, donde los números vienen antes que las letras.

Vale aclarar que los elementos en `datasets` no se alteran y queda todo como antes, aunque ordenado como corresponde.

- línea 284: agregar nueva línea (o sea, 285)

```python
if file_field_names is True: fields[field_name].update(filemetadata.get_metadata(field_names[field_name]))
```
En caso de usar nombres distintos de las variables (o sea, TH en vez de total_power por ejemplo) el diccionario perdía todos los metadatos. Como esos datos todavía existen en el diccionario filemetadata los añado a cada key del diccionario fields (field_names es el diccionario con los nombres modificados y originales; field_name es el nombre modificado que le queda a la variable)

Entiendo que este archivo igualmente está incompleto en algunos de los requerimientos de los desarrolladores de PyART para ponerlo finalmente en io en vez de aux_io.

### sinarame_to_cfradial

En un archivo distinto aproximo lo que ya hizo [Steve](https://github.com/ARM-DOE/pyart/blob/493c53e2aec7c9e2e889ea62c319a2e470a38423/scripts/sinarame_to_cfradial.py) para generar un objeto radar que contenga a todas las variables (y sus metadatos). Hay que definir cómo queda el nombre del archivo, aparentemente es bastante abierto.

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

### English version

### sinarame_h5

On the file `pyart/pyart/aux_io/sinarame_h5.py` the following lines *should* be changed in order to read SINARAME H5.

- line 118: add key in sort

```python
datasets.sort(key=lambda i: '{0:0>9}'.format(i))
```
On the original file there was nothing within the parenthesis and Python sorted the list without arguments. The order was lexicographic so `dataset10` was before `dataset2` (this happened because strings were compared character to character and since `dataset` is the same for all fields, the `1` from `10` is before `2`). The issue comes when the array for data is made because 10th elevation is 'below' 2nd.

That key was some random answer posted in stackoverflow and here I explain what it does.

- `key` iterates on *i* elements of `datasets` list.
- Curly brackets indicate a substitution.
- Each element *i* will be formatted following what's inside the brackets.
 - First `0` indicates the first element inside `format` (in this case, the only one)
 - After the `:` comes the format that will be applied.
 - The three next characters are  *fill, align y minimumwidth* according to [PEP3101](https://www.python.org/dev/peps/pep-3101); in this case completes with zeros, aligning to the right until reaching at least 9 characters.

The new order is: `0dataset1`, `0dataset2`, ..., `0dataset9`, `dataset10` because now the first character to compare in the first nine datasets is the `0`, not the `d`. `datasets` is not altered, just sorted the right way.

- line 284: add new line (i.e., 285)

```python
if file_field_names is True: fields[field_name].update(filemetadata.get_metadata(field_names[field_name]))
```
When using different names for the variables (e.g. TH instead of the original total_power) the radar object loses almost every metadata. But those still exist in the `filemetadata` dictionary, so I add them to each key in the fields dictionary where `field_names` is the dictionary with original and custom variable names, `field_name` is the custom name that the variable will keep.

Although this is incomplete to PyART requirements for moving the script from aux_io to io.

### sinarame_to_cfradial

This is a separate file that completes what [Steve already did](https://github.com/ARM-DOE/pyart/blob/493c53e2aec7c9e2e889ea62c319a2e470a38423/scripts/sinarame_to_cfradial.py) to generate a radar object in PyART that contains all the fields (except KDP). The *final* file name still remains a mystery.

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

cal_temps = u"gregorian" # How is this useful?
cdftime = utime(radar.time['units'])

time1=cdftime.num2date(radar.time['data'][0]).strftime('%Y%m%d_%H%M%S')
time2=cdftime.num2date(radar.time['data'][-1]).strftime('%Y%m%d_%H%M%S')

cffile='cfrad.{time1}.0000_to_{time2}.0000_{b1}_SUR.nc'.format(time1=time1,time2=time2,b1=bs[0])
print cffile

radar._DeflateLevel=5
print('writing to {path}{cffile}'.format(path=path,cffile=cffile))
pyart.io.write_cfradial(path+cffile,radar,format='NETCDF4_CLASSIC')
```
