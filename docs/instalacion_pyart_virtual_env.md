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

El primer comando crea el entorno `steve_pyart` clonando anaconda base.

### Instalación de un fork de PyART

El problema si quería bajar PyART usando `conda install` es que descarga la última versión _estable_. Lo que necesitamos es un archivo read_sinarame_h5 que ya está en Github pero no está en la estable.

Como ya está activado el entorno nuevo, primero instalo netCDF4 con conda

```conda install netCDF4```

Después viene este comando mágico para clonar e instalar desde Github

```
pip install git+git://github.com/swnesbitt/pyart@master
```

Pip descarga el master de PyART y lo instala sin intervención del usuario.

_Aclaración:_ Yo bajé el fork de Steve pero la versión de ARM-DOE ya tiene el archivo que necesitamos. Se puede bajar ese y no debería haber problema. Yo no lo hice.

Instalamos basemap porque después va a hacer falta.

```conda install basemap```
