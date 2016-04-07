## Receta para instalar la librería bbufr

La instalación de la librería bbufr tiene muchas dependencias y requerimientos previos. Este es un merge de lo que le pasó a Lucho y después a mi (Martin) al 	querer instalarlo.

Primero hay que clonar el repositorio de git donde está la librería. Recomendación que vi en varios lugares, crear una carpeta tmp en el home y clonar ahí (la carpeta tmp no tiene mucho sentido en principio pero todo termina funcionando):

```bash
cd ~; mkdir tmp; cd tmp;
git clone git://git.baltrad.eu/bbufr.git
cd bbufr
```

---
### IMPORTANTE PARA RMA

Si se quiere usar bbufr para convertir los BUFR de los RMA en H5 es necesario editar bufr2hdf5.c con la tabla que se encuentra en la [receta para instalar PyART en un entorno virtual](https://gitlab.smn.gov.ar/ID/RadarMeteo/blob/master/docs/instalacion_pyart_virtual_env.md#arreglando-el-conversor-de-bufr-a-hdf5).

En la carpeta [RadarMeteo/conversores/RMA/bbufr](https://gitlab.smn.gov.ar/ID/RadarMeteo/tree/master/conversores/RMA/bbufr) se encuentra el archivo .c con las correcciones necesarias y se puede copiar en la carpeta local `~/tmp/bbufr/tests` **ANTES** de correr el configure y compilar.

---


Dentro de la carpeta hay un ejecutable `configure` al cual hay que darle un par de opciones.

**OJO**, es altamente probable que este instalador falle algunas veces porque falten dependencias. El siguiente comando es el ejecutable, después van todos los requerimientos que hizo falta instalar para que funcione.

```bash
sudo ./configure --prefix=/usr/local/
```

---
### Dependencias
- Proj library

```bash
sudo apt-get install libproj-dev
```

- Zlib

Descargar de www.zlib.net el .tar.gz. Descomprimir y compilar con:
```bash
cd zlib-1.2.8
sudo ./configure --prefix=/usr/local/
sudo make
sudo make install
```

- HDF5

Se pueden hacer dos cosas, instalar por terminal con apt-get o descargar y compilar. El segundo paso es idéntico al de zlib descargando de www.hdfgroup.org/HDF5/release/obtainsrc.html. Por terminal:

```bash
sudo apt-get install libhdf5-serial-dev
```
---

Antes de seguir hay que verificar que se puede consultar la librería de HDF5. Esto se consigue revisando el archivo `~/.bashrc` (o bashprofile en algunos casos). La siguiente línea debería estar, sino se puede agregar al final

```bash
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/bin
```

Luego de editar hay que 'activar' bashrc en la terminal con la siguiente línea

```bash
source ~/.bashrc
```

Con todo esto debería funcionar el ejecutable `configure` y así generar los makefile.

Para estos make encontré varias maneras de ejecutarlos. Voy a poner las 2 que funcionaron.

- Lucho
```bash
sudo make install
sudo make check
```

- Martin
```bash
sudo make
cd tests
make check
make install
```

_Aclaración_: Para poder convertir los bufr de los RMA hace falta unas tablas. En la carpeta `bbufr` hay una carpeta `tables`. Renombrarla a `tables_backup` y copiar la carpeta que contiene las tablas necesarias.

La conversión se realiza de la siguiente manera:

```bash
~/tmp/bbufr/tests/bufr2hdf5 -d /path-to/tables/ /path-to/in_file.BUFR /path-to/out_file.H5
```
