#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Sep 23 14:26:55 2020

@author: diego
"""
import numpy as np
import cv2
import glob
import os
import math
import pickle
import time
import errno
import pandas as pd
from random import randint, uniform,random


def funcion1(vott_df,labeldict):
    # Encode labels according to labeldict if code's don't exist
    if not "code" in vott_df.columns:
        vott_df["code"] = vott_df["label"].apply(lambda x: labeldict[x])
    # Round float to ints
    for col in vott_df[["xmin", "ymin", "xmax", "ymax"]]:
        vott_df[col] = (vott_df[col]).apply(lambda x: round(x))
        
def carga_img_info(path_imagenes,nombre_de_la_imagen):        
    img=cv2.imread(path_imagenes+nombre_de_la_imagen)
    alto=img.shape[0]
    ancho=img.shape[1]
    return img,alto,ancho


    
tipo=[]
def calcula_interseccion_entre_cuadrados(info,x_min,y_min,x_max,y_max):
    global tipo
    flag_es_recuadro_valido=False
    esta_en_ventana=False
    info_aux=[0,0,0,0]
    if (info[0]< x_min) and (info[1] < y_min) and (info[2]>x_min) and (info[3]>y_min) and (info[2]<=x_max) and (info[3]<=y_max):
        info_aux=([0,0,info[2]-x_min,info[3]-y_min])
        esta_en_ventana=True
        tipo.append('c0')
    
    if (info[0]>= x_min) and (info[0]< x_max) and (info[1] < y_min) and (info[2]>x_min) and (info[3]>y_min) and (info[2]<=x_max) and (info[3]<=y_max):
        info_aux=([info[0]-x_min,0,info[2]-x_min,info[3]-y_min])
        esta_en_ventana=True
        tipo.append('c1')
    
    if (info[0]>= x_min) and (info[0]< x_max) and (info[1] < y_min) and (info[3]>y_min) and (info[2]>x_max) and (info[3]<=y_max):
        info_aux=([info[0]-x_min,0,x_max-x_min,info[3]-y_min])
        esta_en_ventana=True
        tipo.append('c2')
    
    if (info[0]< x_min)  and (info[1] >= y_min)and(info[1] < y_max) and (info[2]>x_min) and (info[3]>y_min) and (info[2]<=x_max) and (info[3]<=y_max):
        info_aux=([0,info[1]-y_min,info[2]-x_min,info[3]-y_min])
        esta_en_ventana=True
        tipo.append('c3')
    
    if (info[0]>= x_min)  and (info[1] >= y_min)and (info[0]<x_max) and(info[1] < y_max) and (info[2]>x_min) and (info[3]>y_min) and (info[2]<=x_max) and (info[3]<=y_max):
        info_aux=([info[0]-x_min,info[1]-y_min,info[2]-x_min,info[3]-y_min])
        esta_en_ventana=True
        tipo.append('c4')
    
    if (info[0]>= x_min)  and (info[1] >= y_min)and (info[0]< x_max) and(info[1] < y_max) and (info[3]>y_min) and (info[2]>x_max) and (info[3]<=y_max):
        info_aux=([info[0]-x_min,info[1]-y_min,x_max-x_min,info[3]-y_min])
        esta_en_ventana=True
        tipo.append('c5')
    
    if (info[0]< x_min)  and (info[1] >= y_min) and(info[1] < y_max) and (info[2]>x_min)and (info[2]<=x_max) and (info[3]>=y_max):
        info_aux=([0,info[1]-y_min,info[2]-x_min,y_max-y_min])
        esta_en_ventana=True
        tipo.append('c6')
    
    if (info[0]>= x_min)  and (info[1] >= y_min)and (info[0]< x_max) and(info[1] < y_max) and (info[2]>x_min)and (info[2]<=x_max) and (info[3]>=y_max):
        info_aux=([info[0]-x_min,info[1]-y_min,info[2]-x_min,y_max-y_min])
        esta_en_ventana=True
        tipo.append('c7')
    
    if (info[0]>= x_min)  and (info[1] >= y_min)and (info[0]< x_max) and(info[1] < y_max) and (info[2]>=x_max) and (info[3]>=y_max):
        info_aux=([info[0]-x_min,info[1]-y_min,x_max-x_min,y_max-y_min])
        esta_en_ventana=True
        tipo.append('c8')
        
    if (info[0]< x_min)  and (info[1] < y_min) and (info[2]>x_max) and (info[3]>y_min) and (info[3]<=y_max):
        info_aux=([0,0,x_max-x_min,info[3]-y_min])
        esta_en_ventana=True
        tipo.append('c9')
        
    if (info[0]< x_min)  and (info[1] >= y_min)and (info[1] < y_max) and (info[2]>x_max) and (info[3]>y_min) and (info[3]<=y_max):
        info_aux=([0,info[1]-y_min,x_max-x_min,info[3]-y_min])
        esta_en_ventana=True
        tipo.append('c10')
        
    if (info[0]< x_min)  and (info[1] >= y_min)and (info[1] < y_max) and (info[2]>x_max)  and (info[3]>y_max):
        info_aux=([0,info[1]-y_min,x_max-x_min,y_max-y_min])
        esta_en_ventana=True
        tipo.append('c11')
        
    if (info[0]< x_min)  and (info[1] < y_min) and (info[2]>x_min)and (info[2]<x_max)  and (info[3]>y_max):
        info_aux=([0,0,info[2]-x_min,y_max-y_min])
        esta_en_ventana=True
        tipo.append('c12')
                    
    if (info[0]>= x_min)and(info[0]< x_max)  and (info[1] < y_min) and (info[2]>x_min)and (info[2]<=x_max)  and (info[3]>y_max):
        info_aux=([info[0]-x_min,0,info[2]-x_min,y_max-y_min])
        esta_en_ventana=True
        tipo.append('c13')
        
    if (info[0]>= x_min)and(info[0]< x_max)  and (info[1] < y_min) and (info[2]>x_max)  and (info[3]>y_max):
        info_aux=([info[0]-x_min,0,x_max-x_min,y_max-y_min])
        esta_en_ventana=True
        tipo.append('c14')
        
    if (info[0]<= x_min)  and (info[1] <= y_min) and (info[2]>=x_max)  and (info[3]>=y_max):
        info_aux=([0,0,x_max-x_min,y_max-y_min])
        esta_en_ventana=True
        tipo.append('c15')
    
    num_de_pix_recuadro_de_la_ventana=(info_aux[2]-info_aux[0])*(info_aux[3]-info_aux[1])
    num_de_pix_recuadro_img_grande=(info[2]-info[0])*(info[3]-info[1])
    porc_pix=(num_de_pix_recuadro_de_la_ventana*100)/num_de_pix_recuadro_img_grande
    if porc_pix>20:
        flag_es_recuadro_valido=True
    
    
    return info_aux,esta_en_ventana,flag_es_recuadro_valido
    

def encuentra_imagenes_sin_recuadros_de_interes(path_imagenes,multi_df):
    todas_las_images_en_la_carpeta = glob.glob(path_imagenes+'*.jpg')
    aux=[]
    for fnames in todas_las_images_en_la_carpeta:
        aux.append(fnames.split("/")[-1])
    
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
    
    return imagenes_sin_clases_de_interes
   
    
    
path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/UMV/Images/'
path_CSV='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/UMV/Images/etiquetas.csv'
path_guarda_imagenes_ventaneadas='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/UMV/JPEGImages'

try:
    os.mkdir(path_guarda_imagenes_ventaneadas) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
            
            
multi_df = pd.read_csv(path_CSV)
labels = multi_df["label"].unique()
labeldict = dict(zip(labels, range(len(labels))))
funcion1(multi_df, labeldict)
n_ventanas=25



nombres_de_clases_de_interes=multi_df['image'].unique()

info_del_ventaneado=[]
info_csv=[]

tmstmp1 = time.time()
for imagenes_en_el_csv in  nombres_de_clases_de_interes:
    recuadros_en_la_imagen = multi_df[multi_df['image'] == imagenes_en_el_csv]
    img,alto,ancho=carga_img_info(path_imagenes,imagenes_en_el_csv)
    j=0
    i=0
    tam_ventana=1248
    for n in range(n_ventanas):
        tam_area_elec_alto=(alto-tam_ventana)//math.ceil(math.sqrt(n_ventanas))
        tam_area_elec_ancho=(ancho-tam_ventana)//math.ceil(math.sqrt(n_ventanas))
        
        

        if i<math.ceil(math.sqrt(n_ventanas)):
            #print(i,j)
            y_min=randint(j*tam_area_elec_alto,(j+1)*tam_area_elec_alto)
            x_min=randint(i*tam_area_elec_ancho,(i+1)*tam_area_elec_ancho)
            # print('y va desde ')
            # print((j*tam_area_elec_alto,(j+1)*tam_area_elec_alto))
            # print('x va desde ')
            # print((i*tam_area_elec_ancho,(i+1)*tam_area_elec_ancho))
            i=i+1
            if i==math.ceil(math.sqrt(n_ventanas)):
                j=j+1
                i=0
        
        
        x_max=x_min+tam_ventana
        y_max=y_min+tam_ventana
        img_ventana=img[y_min:y_max,x_min:x_max]
        filename_1=imagenes_en_el_csv[0:-4]+'_v'+str(n)+'.jpg'
        cv2.imwrite(os.path.join(path_guarda_imagenes_ventaneadas,filename_1),img_ventana)
        u=0
        for index, row in recuadros_en_la_imagen.iterrows():
            info=(row[["xmin", "ymin", "xmax", "ymax"]].tolist())
            clase=(row[["label"]].tolist())
            
            recuadro,bandera,recuadro_valido=calcula_interseccion_entre_cuadrados(info,x_min,y_min,x_max,y_max)
            if bandera and recuadro_valido:
                info_csv.append([filename_1,recuadro[0],recuadro[1],recuadro[2],recuadro[3],clase[0]])
            # if bandera:
            #     if (recuadro[0]==0 and recuadro[1]==0) or (recuadro[1]==0 and recuadro[2]==(x_max-x_min)) or (recuadro[0]==0 and recuadro[3]==(y_max-y_min)) or (recuadro[2]==(x_max-x_min) and recuadro[3]==(y_max-y_min)):
            #         if recuadro[2]-recuadro[0]>20 and recuadro[3]-recuadro[1]>20:
            #             info_csv.append([filename_1,recuadro[0],recuadro[1],recuadro[2],recuadro[3],clase[0],u])
            #     if (recuadro[1]==0 and (not (recuadro[0]==0)) and (not (recuadro[2]==x_max-x_min))) or (recuadro[3]==y_max-y_min and not (recuadro[2]==(x_max-x_min)) and not (recuadro[0]==0)):
            #         if recuadro[3]-recuadro[1]>20:
            #             info_csv.append([filename_1,recuadro[0],recuadro[1],recuadro[2],recuadro[3],clase[0],u])
            #     if (not recuadro[1]==0 and (recuadro[0]==0) and not (recuadro[3]==y_max-y_min)) or (not recuadro[1]==0 and (recuadro[2]==x_max-x_min) and not (recuadro[3]==y_max-y_min)):
            #         if recuadro[2]-recuadro[0]>20:
            #             info_csv.append([filename_1,recuadro[0],recuadro[1],recuadro[2],recuadro[3],clase[0],u])
            #     if not (recuadro[0]==0 or recuadro[1]==0 or recuadro[2]==(x_max-x_min) or recuadro[3]==(y_max-y_min)):
            #         info_csv.append([filename_1,recuadro[0],recuadro[1],recuadro[2],recuadro[3],clase[0]])
                
                u=u+1

df = pd.DataFrame(info_csv)    
df=df.rename(columns={0:"image",1:"xmin",2:"ymin",3:"xmax",4:"ymax",5:"label"})
df.to_csv('etiquetas_umv_ventaneadas.csv',index=False)




imagenes_sin_clases_de_interes=encuentra_imagenes_sin_recuadros_de_interes(path_imagenes,multi_df)



for imagenes_scdi in  imagenes_sin_clases_de_interes:
    img,alto,ancho=carga_img_info(path_imagenes,imagenes_scdi)
    j=0
    i=0
    
    for n in range(n_ventanas):
        tam_area_elec_alto=(alto-tam_ventana)//math.ceil(math.sqrt(n_ventanas))
        tam_area_elec_ancho=(ancho-tam_ventana)//math.ceil(math.sqrt(n_ventanas))
        
        

        if i<math.ceil(math.sqrt(n_ventanas)):
            #print(i,j)
            y_min=randint(j*tam_area_elec_alto,(j+1)*tam_area_elec_alto)
            x_min=randint(i*tam_area_elec_ancho,(i+1)*tam_area_elec_ancho)
            # print('y va desde ')
            # print((j*tam_area_elec_alto,(j+1)*tam_area_elec_alto))
            # print('x va desde ')
            # print((i*tam_area_elec_ancho,(i+1)*tam_area_elec_ancho))
            i=i+1
            if i==math.ceil(math.sqrt(n_ventanas)):
                j=j+1
                i=0
        
        
        x_max=x_min+(tam_ventana)
        y_max=y_min+(tam_ventana)
        img_ventana=img[y_min:y_max,x_min:x_max]
        filename_1=imagenes_scdi[0:-4]+'_v'+str(n)+'.jpg'
        cv2.imwrite(os.path.join(path_guarda_imagenes_ventaneadas,filename_1),img_ventana)



tmstmp2 = time.time()
print('Total time elapsed = ', tmstmp2 - tmstmp1)           
           
            























