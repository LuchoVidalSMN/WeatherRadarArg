Instalar wradlib puede ser complicado (o no). Con esta guía _made in SMN_ instalé Anaconda y wradlib en Ubuntu 14.04LTS x86_64.

Descargar e instalar Anaconda

```
bash Anaconda2-2.5.0-Linux-x86_64.sh 
```

Por las dudas, previamente instalé PyART con sus dependencias y requerimientos (hay que buscar el paquete con los dos primeros comandos y se instala con el tercero; los dos primeros es por si a alguien se le ocurrió actualizar algo y el tercer comando no sirve de entrada)

```
anaconda search -t conda pyart
anaconda show jjhelmus/pyart
conda install --channel https://conda.anaconda.org/jjhelmus pyart
```

Instalar gdal **desde conda** (para que no falten dependencias, requerimientos o lo que a gdal se le ocurra que falte)

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

Probar ejecutando el siguiente comando en una terminal. La salida debería ser 0 si se instaló correctamente.

```
ipython -c "import wradlib"; echo $?
```
