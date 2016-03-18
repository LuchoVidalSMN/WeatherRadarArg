## Entorno virtual e instalación de módulo no-Anaconda

Esta guía muestra los pasos que seguí para descargar PyART "beta" que no está en ninguno de los repositorios de Anaconda. Además, al final comento lo que hice para arreglar la conversión de los .BUFR de los RMA a .H5

Resumen de lo que hice:

1. Cree un entorno virtual en Anaconda
2. Active el entorno
3. Instale netCDF4
4. Instale PyART (el fork de Steve)
5. Modifiqué bufr2hdf5.c
6. Listo!

### Creación de un entorno virtual en Anaconda

La idea de crear un entorno virtual es no romper nada de lo que ya sabemos que anda. Lo que hice fue duplicar anaconda e instalar las dependencias necesarias para instalar PyART

```
conda create --name steve_pyart anaconda
source activate steve_pyart
```

El primer comando crea el entorno `steve_pyart` clonando `anaconda` base (i.e. 0 km!).

### Instalación de un fork de PyART

El problema si quería bajar PyART usando `conda install` es que descarga la última versión *estable*. Lo que necesitamos es un archivo read_sinarame_h5 que ya está en la versión de Github ("beta") pero que no está en la estable.

Como ya está activado el entorno nuevo, primero instalo netCDF4 con conda `conda install netCDF4`

Después viene este comando mágico para clonar e instalar desde Github

```
pip install git+git://github.com/swnesbitt/pyart@master
```

Pip descarga el master de PyART y lo instala sin intervención del usuario.

*Aclaración:* Yo bajé el fork de Steve pero la versión de ARM-DOE ya tiene el archivo que necesitamos. Se puede bajar ese y no debería haber problema. Yo no lo hice.

Instalamos basemap porque después (siempre) va a hacer falta.

```conda install basemap```

### Arreglando el conversor de BUFR a HDF5

En la [otra receta](https://github.com/LuchoVidalSMN/WeatherRadarArg_SMN_INTA/blob/master/docs/receta_instalacion_bbufr.md) se descarga e instala la versión común de `bbufr`. Los RMA necesitan algunos ajustes previo a la compilación para que después reconozca todas las variables. Existe el documento donde muestra las líneas exactas que hay que cambiar. Acá dejo asentado cuales son los números y las variables que le corresponden

Variable | Parámetro |
:---: | :---:
CM | 243
KDP | 240
PHIDP | 239
RHOHV | 241
TH | 230
TV | 231
VRAD | 40
WRAD | 60

