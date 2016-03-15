
# coding: utf-8

# Acá voy a completar el archivo que originalmente iba en bash. La idea es la siguiente:
# 
# - Ingreso y asigno las variables desde la consola (dia, hora, etc)
# - Agarro las lineas con grep
# - Copio los rvd con scp desde Sol1
# - Creo la matriz de datos con Matlab (baco o ms-36?)
# - Ejecuto el resto del código de Python (genero_figura_dsd)

# Importo las librerias necesarias
# Esta comentado tambien lo que necesitaria para la T-Matrix

import os
import sys
import datetime
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import scipy.io as sio

#from pytmatrix.tmatrix import Scatterer
#from pytmatrix import psd, orientation, radar, tmatrix_aux, refractive
#get_ipython().magic(u'matplotlib inline')


################################

# Asigno nombres a las variables de entrada (entran por consola)
#anio_entrada = sys.argv[1]
#mes_entrada = sys.argv[2]
#dia_entrada = str(sys.argv[1])
#hora_final = sys.argv[4]
#n_horas_atras = sys.argv[5]

anio_entrada = '2016'
mes_entrada = '1'
dia_entrada = '1'
hora_final = '0' #UTC
n_horas_atras = '24'

################################

# Defino algunas fechas con los datos de entrada

fecha_final = datetime.datetime(int(anio_entrada), int(mes_entrada), int(dia_entrada),int(hora_final),0)
fecha_final_str = fecha_final.strftime('%Y%m%d%H')

horas_atras = datetime.timedelta(hours=int(n_horas_atras))

# Defino antes la correccion para hora UTC
utc = datetime.timedelta(hours=3)

hora_local_final = fecha_final - utc
hora_local_final_str = hora_local_final.strftime('%Y%m%d%H')

################################

# Voy a hacer grep y scp de la primera hora así guardo los datos
# temporariamente en orden cronologico

# Primero creo el archivo input_dsd.txt y levanto los rvd para la primera hora
os.system('rm /ms-36/mrugna/disdrometro/input_dsd.txt')

# Ahora hago un array con la cantidad de horas totales 
n_horas = np.arange(int(n_horas_atras),0,-1)

for i in n_horas:
    delta = datetime.timedelta(hours=i)
    
    fecha_atras = fecha_final-delta # ya es UTC
    fecha_atras_str = fecha_atras.strftime('%Y%m%d%H')
    
    hora_local = fecha_atras - utc # CAMBIAR A HORA LOCAL
    hora_local_str = hora_local.strftime('%Y%m%d%H')
    
    # grep "DIA.MES.ANIO;HORA" SADL_DSD_ANIOMES.txt >> path/to/input_dsd.txt 
    os.system('grep -F "'+hora_local_str[6:8]+'.'+hora_local_str[4:6]+'.'+hora_local_str[0:4]+';'+hora_local_str[8:10]+'" /ms-36/mrugna/disdrometro/SADL_DSD_'+hora_local_str[0:4]+hora_local_str[4:6]+'.txt >> /ms-36/mrugna/disdrometro/input_dsd.txt')
    os.system('scp mrugna@10.10.23.168:/yanina-sol-ms1/radar/eze/'+fecha_atras_str[0:4]+fecha_atras_str[4:6]+fecha_atras_str[6:8]+'/rvd/ar1.cz240p1.'+fecha_atras_str[0:4]+fecha_atras_str[4:6]+fecha_atras_str[6:8]+'.'+fecha_atras_str[8:10]+'*.z.rvd /ms-36/mrugna/disdrometro/tmp/')
    
# Copio el ultimo dato del disdrometro y del radar
os.system('grep -F "'+hora_local_final_str[6:8]+'.'+hora_local_final_str[4:6]+'.'+hora_local_final_str[0:4]+';'+hora_local_final_str[8:10]+':00" /ms-36/mrugna/disdrometro/SADL_DSD_'+hora_local_final_str[0:4]+hora_local_final_str[4:6]+'.txt >> /ms-36/mrugna/disdrometro/input_dsd.txt')
os.system('scp mrugna@10.10.23.168:/yanina-sol-ms1/radar/eze/'+fecha_final_str[0:4]+fecha_final_str[4:6]+fecha_final_str[6:8]+'/rvd/ar1.cz240p1.'+fecha_final_str[0:4]+fecha_final_str[4:6]+fecha_final_str[6:8]+'.'+fecha_final_str[8:10]+'00*.z.rvd /ms-36/mrugna/disdrometro/tmp/')


################################

# Convierto los rvd a header y volscan
os.system('cd /ms-36/mrugna/disdrometro/tmp/; ./converte_radar_ar_2_header_vol.sh')

# Elimino los rvd
os.system('rm /ms-36/mrugna/disdrometro/tmp/*.rvd')

################################

# Llamo a Matlab y genero la matriz
os.system("ssh mrugna@10.1.7.161 'cd /ms-36/mrugna/disdrometro/tmp; /home/apps/Matlab/bin/matlab -nodisplay -r \"run /ms-36/mrugna/disdrometro/tmp/genero_EZE_dsd.m;quit\"'")

# Borro los archivos .r
os.system('rm /ms-36/mrugna/disdrometro/tmp/*.z.r')

################################

# Variables para calcular reflectividad
bins=np.array([  0.062,   0.187,   0.312,   0.437,   0.562,   0.687,   0.812,
         0.937,   1.062,   1.187,   1.375,   1.625,   1.875,   2.125,
         2.375,   2.75,   3.25 ,   3.75 ,   4.25 ,   4.75 ,   5.5 ,
         6.5  ,   7.5  ,   8.5  ,   9.5  ,  11.  ,  13.   ,  15.   ,
        17.   ,  19.   ,  21.5   ,  24.5 ])

bins_diff=[ 0.125,  0.125,  0.125,  0.125,  0.125,  0.125,  0.125,  0.125,  0.125,  0.125,
  0.25,  0.25,   0.25,   0.25,   0.25,   0.5,  0.5,   0.5,    0.5,    0.5,    1.,
  1.,     1.,     1.,     1.,     2.,    2.,     2.,     2.,     2.,     3.,    3.   ]

################################

texto = open('/ms-36/mrugna/disdrometro/input_dsd.txt','r')

# Dejo abierto el diccionario y las listas
dsd= {}
dsd['fecha'] = []
dsd['espectro_raw'] = []
dsd['DBZ_rayleigh'] = []
dsd['DBZ_Parsivel'] = []

# Leo los datos y los guardo en el diccionario
for line in texto:
    dsd['fecha'].append(datetime.datetime(int(line[6:10]),int(line[3:5]),int(line[0:2]),
                         int(line[11:13]),int(line[14:16]))+utc)
    dsd['espectro_raw'].append(line[line.index(">")+1:-12]) # la prueba fue con -12!!!

    l = len(dsd['fecha'])-1
    
    k=0
    for indice,caracter in enumerate(line):
        if line[indice:indice+1] == ';':
            if k==6 and line[indice+7]==';' and line[indice+6]!=';':
                if line[indice+1:indice+3] + '.' + line[indice+4:indice+7] == '-9.999':
                    dsd['DBZ_Parsivel'].append(float('nan'))
                    break
                else:
                    dsd['DBZ_Parsivel'].append(float(line[indice+1:indice+3] + '.' + line[indice+4:indice+7]))
                    break
            elif k==6 and line[indice+6]==';' and line[indice+5]!=';':
                dsd['DBZ_Parsivel'].append(float(line[indice+1:indice+2] + '.' + line[indice+3:indice+6]))
                break
            k=k+1

    if dsd['espectro_raw'][l] == 'ZERO':
        dsd['DBZ_rayleigh'].append(float('nan'))
    else:
        #Creo la lista y la modifico para un array de 32x32
        puntocoma=';'
        lista=[]


        for index,letra in enumerate(dsd['espectro_raw'][l]):

            if index == 0 and letra == puntocoma:
                lista.append(0)
            elif index == 0 and dsd['espectro_raw'][l][index] != puntocoma and dsd['espectro_raw'][l][index+1] == puntocoma:
                lista.append(int(letra))
            elif index == 0 and dsd['espectro_raw'][l][index] != puntocoma and dsd['espectro_raw'][l][index+1] != puntocoma and dsd['espectro_raw'][l][index+2] == puntocoma:
                lista.append(int(dsd['espectro_raw'][l][index] + dsd['espectro_raw'][l][index+1]))
            elif index == 0 and dsd['espectro_raw'][l][index] != puntocoma and dsd['espectro_raw'][l][index+1] != puntocoma and dsd['espectro_raw'][l][index+2] != puntocoma and dsd['espectro_raw'][l][index+3] == puntocoma:
                lista.append(int(dsd['espectro_raw'][l][index] + dsd['espectro_raw'][l][index+1] + dsd['espectro_raw'][l][index+2]))

            if index != 0 and letra == puntocoma and dsd['espectro_raw'][l][index-1] == puntocoma:
                lista.append(0)
            elif index != 0 and dsd['espectro_raw'][l][index] != puntocoma and dsd['espectro_raw'][l][index+1] == puntocoma and dsd['espectro_raw'][l][index-1] == puntocoma:
                lista.append(int(letra))
            elif index != 0 and dsd['espectro_raw'][l][index] != puntocoma and dsd['espectro_raw'][l][index+1] != puntocoma and dsd['espectro_raw'][l][index+2] == puntocoma and dsd['espectro_raw'][l][index-1] == puntocoma:
                lista.append(int(dsd['espectro_raw'][l][index] + dsd['espectro_raw'][l][index+1]))
            elif index != 0 and dsd['espectro_raw'][l][index] != puntocoma and dsd['espectro_raw'][l][index+1] != puntocoma and dsd['espectro_raw'][l][index+2] != puntocoma and dsd['espectro_raw'][l][index+3] == puntocoma and dsd['espectro_raw'][l][index-1] == puntocoma:
                lista.append(int(dsd['espectro_raw'][l][index] + dsd['espectro_raw'][l][index+1] + dsd['espectro_raw'][len(dsd['fecha'])-1][index+2]))

        array_1024 = np.asarray(lista)
        matriz = np.reshape(array_1024, (32,32))
        # ACA HAY QUE HACER EL QC
        NDS = np.sum(matriz, axis=0) # emulo a leo_parsivel.m

        # Mas variables para generar la DSD desde la cantidad de gotas
        t = 60
        sup = 180.*30.*np.power(10.,-6.)

        vf = -0.193 + (4.96 * bins) - (0.904 * np.power(bins,2)) + (0.0566 * np.power(bins,3))

        DG = NDS / (vf * sup * t * bins_diff)

        ray_Z = np.sum(np.multiply(DG*bins_diff,np.power(bins,6.)))
        DBZ = 10.*np.log10(ray_Z)

        dsd['DBZ_rayleigh'].append(DBZ)

texto.close()

################################

# Levanto la matriz generada anteriormente a un diccionario

EZE = {}
EZE['fecha'] = []
EZE['DBZ'] = []
EZE['sigmaDBZ'] = []
EZE['DBZ_interp'] = []

try:
	matlab = sio.loadmat('/ms-36/mrugna/disdrometro/tmp/EZE_dsd.mat')

	matriz_matlab = matlab['EZE']

	for index,data in enumerate(matriz_matlab):
	    EZE['fecha'].append(datetime.datetime(int(matriz_matlab[(index,0)]),
		                                  int(matriz_matlab[(index,1)]),
		                                  int(matriz_matlab[(index,2)]),
		                                  int(matriz_matlab[(index,3)]),
		                                  int(matriz_matlab[(index,4)])))
	    EZE['DBZ'].append(matriz_matlab[(index,5)])
	    EZE['sigmaDBZ'].append(matriz_matlab[(index,6)])
	    EZE['DBZ_interp'].append(matriz_matlab[(index,7)])

except IOError:
	pass
	
    
################################

# Estas son fechas para usar en el nombre de la figura
horaini = datetime.timedelta(hours=int(n_horas_atras))

fechaini = datetime.datetime(int(anio_entrada), int(mes_entrada), int(dia_entrada),int(hora_final),0)- horaini

fechaini_str = fechaini.strftime('%Y%m%d%H')

################################

# Creo arrays de las distintas reflectividades
dbz_ray= np.asarray(dsd['DBZ_rayleigh'])
dbz_ott = np.asarray(dsd['DBZ_Parsivel'])

dbz= np.asarray(EZE['DBZ'])
dbz_interpolado = np.asarray(EZE['DBZ_interp'])

# Edito el formato de la hora (va a ir al eje x)
horas_mdates = mdates.HourLocator()
horasfmt = mdates.DateFormatter('%d/%m/%Y %HUTC')

fig, ax = plt.subplots(figsize=(16,12))
ax.grid(True)

ax.set_title(u'Comparación de reflectividad entre \n disdrómetro La Plata (SADL) y radar Ezeiza', size=18)

ax.set_ylabel('Factor de Reflectividad (dBZ)', size=13)
#ax.set_xlabel('')

# Le digo en que formato poner la hora en el eje x
ax.xaxis.set_major_locator(horas_mdates)
ax.xaxis.set_major_formatter(horasfmt)

ax.plot(dsd['fecha'], dbz_ray,'b', label='Rayleigh', linewidth=2)
#ax.plot(dsd['fecha'], dbz_ott,'k', label='Parsivel')

#ax.plot(dsd['fecha'], dbz_ray-dbz_ott, 'k', label='Diferencia Ray-Par')

ax.plot(EZE['fecha'], dbz_interpolado,'r', linewidth=2)
ax.plot(EZE['fecha'], dbz,'or', label='Radar EZE')

ax.tick_params(axis='both', labelsize=13)

ax.set_ylim([-10,60])
ax.set_xlim(fecha_final-horas_atras, fecha_final)

fig.autofmt_xdate()
plt.legend(loc='best')

# Guardo la figura en ms-36 para despues subirla a Sol1
plt.savefig('/ms-36/mrugna/disdrometro/disdro_'+fechaini_str[0:4]+fechaini_str[4:6]+fechaini_str[6:8]+'.png',
           dpi=65,transparent=False)

################################

# Borro los archivos temporales
os.system('rm /ms-36/mrugna/disdrometro/tmp/EZE_dsd.mat')
os.system('rm /ms-36/mrugna/disdrometro/input_dsd.txt')

