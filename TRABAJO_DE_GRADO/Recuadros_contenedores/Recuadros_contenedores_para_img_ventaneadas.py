#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 11:59:56 2020

@author: diego
"""

import numpy as np
import cv2
import pandas as pd
import math
import pickle
import os
import errno

def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)
    
dicci_ventaneado=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/datos_del_ventaneado/datos_ventaneado_dia2.pkl')    
detection_images= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/darknet/detect_images_info/informacion_imagenes_dia2.pkl')
path_imagenes_boundingbox='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Recuadros_contenedores/resultados_con_recuadros_4'

path_imagenes_grandes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/RESULTADOS_dia2/img_diego_dia2/'
try:
    os.mkdir(path_imagenes_boundingbox) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
color_0 = (0,0,255)

detection_big_images=[]
imagen_anterior=''
for n in range(len(detection_images)):
    imagen_grande=(detection_images[n]['image_name'].split("/")[-1]).split("_")[0]
    indice=dicci_ventaneado['imagen'].index(imagen_grande+'.jpg')
    if(imagen_grande!=imagen_anterior):
        conta=0
        det_aux=[]
        while(imagen_grande+'.jpg'==dicci_ventaneado['imagen'][indice+conta]):            
            x_min_v=dicci_ventaneado['xmin_v'][indice+conta]
            y_min_v=dicci_ventaneado['ymin_v'][indice+conta]
            for x in range(len(detection_images[n+conta]['detections'])):
                deteccion_aux=detection_images[n+conta]['detections'][x]
                _aux=(deteccion_aux[2][0]+x_min_v,deteccion_aux[2][1]+y_min_v,deteccion_aux[2][2],deteccion_aux[2][3])
                det_aux.append((deteccion_aux[0],deteccion_aux[1],_aux))
            conta=conta+1
            if indice+conta==len(detection_images):
                break
       
            
        detection_big_im={'detections':det_aux,
                              'image_name':path_imagenes_grandes+imagen_grande+'.jpg'}
        detection_big_images.append(detection_big_im)
    imagen_anterior=imagen_grande 





for imagen_info in detection_big_images:
    if imagen_info['detections']:
        img=cv2.imread(imagen_info['image_name'])
        for detection_number in range(len(imagen_info['detections'])):
            yExtent=int(imagen_info['detections'][detection_number][2][3])
            xEntent=int(imagen_info['detections'][detection_number][2][2])
            xCoord=int(imagen_info['detections'][detection_number][2][0]-imagen_info['detections'][detection_number][2][2]/2)
            yCoord=int(imagen_info['detections'][detection_number][2][1]-imagen_info['detections'][detection_number][2][3]/2)
            sup_izq=(xCoord, yCoord)
            inf_der=(xCoord + xEntent, yCoord + yExtent)
            sup_izq_titulo=(xCoord, yCoord-30)
            cv2.rectangle(img,sup_izq,inf_der, color_0, 5)
            clase=imagen_info['detections'][detection_number][0]
            proba=imagen_info['detections'][detection_number][1]
            #cv2.putText(img,clase+' '+str("{:.2f}".format(proba*100))+'%', sup_izq_titulo, cv2.FONT_HERSHEY_SIMPLEX, 2, color_0, 3)
        
#        img_g=cv2.resize(img,(2500,1500))
        cv2.imwrite(os.path.join(path_imagenes_boundingbox,imagen_info['image_name'].split("/")[-1]),img)
        
    if not imagen_info['detections']:    
        img=cv2.imread(imagen_info['image_name'])
 #       img_g=cv2.resize(img,(2500,1500))
        cv2.imwrite(os.path.join(path_imagenes_boundingbox,imagen_info['image_name'].split("/")[-1]),img)
        

