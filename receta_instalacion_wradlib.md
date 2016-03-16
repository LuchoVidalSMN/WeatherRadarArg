Este archivo se puede pasar a un markdown para que quede mejor con códigos, etc.

Funciona en Ubuntu 14.04LTS x86_64

Descargar e instalar Anaconda

bash Anaconda2-2.5.0-Linux-x86_64.sh 


Por las dudas, previamente ya instalar PyART con sus dependencias y requerimientos
(hay que buscar el paquete con los dos primeros comandos y se instala con el tercero)

```
anaconda search -t conda pyart
anaconda show jjhelmus/pyart
conda install --channel https://conda.anaconda.org/jjhelmus pyart
```

Instalar gdal **desde conda** (sino van a faltar dependencias)

```
conda install gdal
```

Instalar como hizo Lucho con pip forzando la actualización

```
pip install --upgrade gdal
```

Finalmente instalar wradlib (idem PyART)

```
anaconda search -t conda wradlib
anaconda show jjhelmus/wradlib
conda install --channel https://conda.anaconda.org/jjhelmus wradlib
```
