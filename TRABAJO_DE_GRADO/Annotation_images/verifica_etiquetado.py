import numpy as np
import cv2
import glob
import os
import pandas as pd
import errno
import time

def VERIFICA_ETIQUETADO(VoTT_csv,path_resultado_de_verifica,path_im_prueba):
    multi_df = pd.read_csv(VoTT_csv)
    #COLOR PARA CLASE 0
    color_0 = (255,0,0)
    #COLOR PARA CLASE 1
    color_1 = (0,255,0)
    #COLOR PARA CLASE 2
    color_2 = (0,0,255)
    nombre_de_la_imagen_anterior=''
    
    for index, row in multi_df.iterrows():
        nombre_de_la_imagen=(row[["image"]].tolist())
        info=(row[["xmin", "ymin", "xmax", "ymax"]].tolist())
        clase=(row[["label"]].tolist())
        if nombre_de_la_imagen != nombre_de_la_imagen_anterior:
            img = cv2.imread(path_im_prueba+nombre_de_la_imagen[0])
        
        if clase[0]=='libro':
            #AZUL
            color=color_0
        if clase[0]=='libro_cerrado':
            #VERDE
            color=color_1
        if clase[0]=='libro_abierto':
            #ROJO
            color=color_2                           
        cv2.rectangle(img, (int(info[0]), int(info[1])),(int(info[2]), int(info[3])), color, 8)
        cv2.putText(img, clase[0], (int(info[0]), int(info[1])-30), cv2.FONT_HERSHEY_SIMPLEX, 3, color, 4)
        nombre_de_la_imagen_anterior=nombre_de_la_imagen
        
        img_g=cv2.resize(img,(1000,700))
        cv2.imwrite(os.path.join(path_resultado_de_verifica,nombre_de_la_imagen[0]),img_g)
    
    
    todas_las_images_en_la_carpeta = glob.glob(path_im_prueba+'*.jpg')
    aux=[]
    for fnames in todas_las_images_en_la_carpeta:
        aux.append(fnames.lstrip(path_im_prueba))
    
    todas_las_images_en_la_carpeta=aux
    imagenes_con_clases_de_interes=multi_df["image"].unique()
    imagenes_con_clases_de_interes=imagenes_con_clases_de_interes.tolist()
    
    imagenes_sin_clases_de_interes=[]
    for n in todas_las_images_en_la_carpeta:
        si_esta_la_imagen=False
        no_toma_la_imagen=False
        for k in imagenes_con_clases_de_interes:
            if n==k:
                si_esta_la_imagen=True
            if n!=k and si_esta_la_imagen==False:
                aux1=n
            if si_esta_la_imagen==True:
                no_toma_la_imagen=True
                    
        if no_toma_la_imagen==False:
            imagenes_sin_clases_de_interes.append(aux1)
            
    print(len(todas_las_images_en_la_carpeta))
    print(len(imagenes_sin_clases_de_interes))
    print(len(imagenes_con_clases_de_interes))
    for n in range(len(imagenes_sin_clases_de_interes)):
        img = cv2.imread(path_im_prueba+imagenes_sin_clases_de_interes[n])
        img_g=cv2.resize(img,(1000,700))
        cv2.imwrite(os.path.join(path_resultado_de_verifica,imagenes_sin_clases_de_interes[n]),img_g)

path_im_prueba='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/resultados/'

VoTT_csv='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/vott-csv-export/test_libros2.0-export.csv'
path_resultado_de_verifica='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/verifica_etiquetado'
try:
    os.mkdir(path_resultado_de_verifica) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
tmstmp1 = time.time()
VERIFICA_ETIQUETADO(VoTT_csv,path_resultado_de_verifica,path_im_prueba)   
tmstmp2 = time.time()
print('Total time elapsed = ', tmstmp2 - tmstmp1)


















