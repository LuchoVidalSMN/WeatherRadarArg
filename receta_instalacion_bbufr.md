La instalación de la librería bbufr tiene muchas dependencias y requerimientos previos. Este es un merge de lo que le pasó a Lucho y después a mi (Martin) al 	querer instalarlo.

Primero hay que clonar el repositorio de git donde está la librería. Recomendación que vi en varios lugares, crear una carpeta tmp en el home y clonar ahí (la carpeta tmp no tiene mucho sentido en principio pero todo termina funcionando):

```
cd ~; mkdir tmp; cd tmp;
git clone git://git.baltrad.eu/bbufr.git
cd bbufr
```

Dentro de la carpeta hay un ejecutable ```configure``` al cual hay que darle un par de opciones.

*OJO*, es altamente probable que este instalador falle algunas veces porque falten dependencias. El siguiente comando es el ejecutable, después van todos los requerimientos que hizo falta instalar para que funcione.

```sudo ./configure --prefix=/usr/local/```

- Proj library
```sudo apt-get install libproj-dev```

- Zlib
Descargar de www.zlib.net el .tar.gz. Descomprimir y compilar con:
```
cd zlib-1.2.8
sudo ./configure --prefix=/usr/local/
sudo make
sudo make install
```

- HDF5
Se pueden hacer dos cosas, instalar por terminal con apt-get o descargar y compilar. El segundo paso es idéntico al de zlib descargando de www.hdfgroup.org/HDF5/release/obtainsrc. Por terminal:

```sudo apt-get install libhdf5-serial-dev```

Con todo esto debería funcionar el ejecutable ```configure``` y así generar los makefile.

Para estos make encontré varias maneras de ejecutarlos. Voy a poner las 2 que funcionaron.

- Lucho
```
sudo make install
sudo make check
```

- Martin
```
sudo make
cd tests
make check
make install
```

_Aclaración_: Para poder convertir los bufr de los RMA hace falta unas tablas. En la carpeta ```bbufr``` hay una carpeta ```tables```. Renombrarla a ```tables_backup``` y copiar la carpeta con las tablas necesarias.

La conversión se realiza de la siguiente manera:

```
cd ~/tmp/bbufr/tests/
./bufr2hdf5 -d /path-to/tables/ /path-to/in_file.BUFR /path-to/out_file.H5
```
