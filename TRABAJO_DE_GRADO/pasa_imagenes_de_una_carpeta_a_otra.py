import os
import pandas as pd
import shutil
import glob
        
        
path_1 = "/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/fh_ventanas/img_ventaneadas_dia1_fh/*.jpg"
path_2 = "/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/fh_ventanas/img_ventaneadas_dia2_diego_fh/*.jpg"
path_3 = "/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/fh_ventanas/img_ventaneadas_dia2_javi_fh/*.jpg"

path_destino="/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/fh_ventanas/imagenes_totales/"
nombres_imagenes_1=glob.glob(path_1)
nombres_imagenes_2=glob.glob(path_2)
nombres_imagenes_3=glob.glob(path_3)
nombres=nombres_imagenes_1+nombres_imagenes_2+nombres_imagenes_3
for imagen in nombres:
    imagen_copia = path_destino + imagen.split('/')[-1]
    shutil.copy(imagen,imagen_copia)
    
