#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 18:09:35 2020

@author: diego
"""


import glob
import os
import cv2
import pickle
import errno

def save_obj(obj, name ):
    with open('datos_del_ventaneado/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

    
        
        
path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/RESULTADOS_dia2/img_diego_dia2/'
path_guarda_imagenes_ventaneadas='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/img_ventaneadas_para_deteccion_dia2'

path_datos_del_ventaneado='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/datos_del_ventaneado/'

try:
    os.mkdir(path_datos_del_ventaneado) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
try:
    os.mkdir(path_guarda_imagenes_ventaneadas) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
        
nom_img=[]
x_min_v=[]
y_min_v=[]

imagenes_de_prueba=glob.glob(path_imagenes+'/*.jpg')  
for nombre_de_la_imagen in imagenes_de_prueba:
    a=1
    img=cv2.imread(nombre_de_la_imagen)
    alto=img.shape[0]
    ancho=img.shape[1]
    ancho_v=1248
    alto_v=1248
    
    
    num_v_verti=alto//alto_v
    num_v_horiz=ancho//ancho_v
    
    
    parte_hori_restante=ancho-num_v_horiz*ancho_v
    parte_verti_restante= alto-num_v_verti*alto_v
    
    i=0
    for verti in range(num_v_verti):
        y=alto-(verti+1)*alto_v
        h=alto_v        
        for hori in range(num_v_horiz):
            x=hori*ancho_v
            w=ancho_v
            img_g=img[y:y+h,x:x+w]
            filename_1=nombre_de_la_imagen.split("/")[-1]
            filename_1=filename_1[0:len(filename_1)-4]+'_v'+str(i)+'.jpg'
            i=i+1
            cv2.imwrite(os.path.join(path_guarda_imagenes_ventaneadas,filename_1),img_g)
            x_min_v.append(x)
            y_min_v.append(y)
            nom_img.append(nombre_de_la_imagen.split("/")[-1])
            
            if parte_hori_restante>200 and hori==num_v_horiz-1:
                x=ancho-ancho_v
                img_g=img[y:y+h,x:x+w]
                filename_1=nombre_de_la_imagen.split("/")[-1]
                filename_1=filename_1[0:len(filename_1)-4]+'_v'+str(i)+'.jpg'
                i=i+1
                cv2.imwrite(os.path.join(path_guarda_imagenes_ventaneadas,filename_1),img_g)
                x_min_v.append(x)
                y_min_v.append(y)
                nom_img.append(nombre_de_la_imagen.split("/")[-1])
                
                
                
        if parte_verti_restante>500 and verti== num_v_verti-1:
            y=0
            h=alto_v
            for hori in range(num_v_horiz):
                x=hori*ancho_v
                w=ancho_v
                img_g=img[y:y+h,x:x+w]
                filename_1=nombre_de_la_imagen.split("/")[-1]
                filename_1=filename_1[0:len(filename_1)-4]+'_v'+str(i)+'.jpg'
                i=i+1
                cv2.imwrite(os.path.join(path_guarda_imagenes_ventaneadas,filename_1),img_g)
                x_min_v.append(x)
                y_min_v.append(y)
                nom_img.append(nombre_de_la_imagen.split("/")[-1])
                
                
                if parte_hori_restante>200 and hori==num_v_horiz-1:
                    x=ancho-ancho_v
                    img_g=img[y:y+h,x:x+w]
                    filename_1=nombre_de_la_imagen.split("/")[-1]
                    filename_1=filename_1[0:len(filename_1)-4]+'_v'+str(i)+'.jpg'
                    i=i+1
                    cv2.imwrite(os.path.join(path_guarda_imagenes_ventaneadas,filename_1),img_g)
                    x_min_v.append(x)
                    y_min_v.append(y)
                    nom_img.append(nombre_de_la_imagen.split("/")[-1])
                    
                    
                    

dicci_ventaneado={'imagen':nom_img,
                  'xmin_v':x_min_v,
                  'ymin_v':y_min_v,
                  'ancho_ve':ancho_v,
                  'alto_ve':alto_v}
save_obj(dicci_ventaneado,'datos_ventaneado_dia2')