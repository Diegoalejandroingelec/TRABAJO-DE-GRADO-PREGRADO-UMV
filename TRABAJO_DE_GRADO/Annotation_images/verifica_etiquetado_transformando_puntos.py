import numpy as np
import cv2
import glob
import os
import pandas as pd
import errno
import time
import pickle

def coordenadas_en_vista_de_original(M_1,x_11,y_11):
    coordenadas_imagen_vista_original=np.float64([(M_1[0,0]*x_11+M_1[0,1]*y_11+M_1[0,2])/(M_1[2,0]*x_11+M_1[2,1]*y_11+M_1[2,2]),(M_1[1,0]*x_11+M_1[1,1]*y_11+M_1[1,2])/(M_1[2,0]*x_11+M_1[2,1]*y_11+M_1[2,2])])
    return coordenadas_imagen_vista_original


def coordenadas_en_vista_original_total(Mr,M,y_r,x_r,p_x,p_y):
    puntos_aux=coordenadas_en_vista_de_original(Mr,p_x+x_r,p_y+y_r)
    coord_en_img_orig=coordenadas_en_vista_de_original(M,puntos_aux[0],puntos_aux[1])
    return coord_en_img_orig

def corrige_cordenadas_que_no_existen(tam_imagen,coordenada_calculada):
    alto=tam_imagen[0]
    ancho=tam_imagen[1]
    
    if coordenada_calculada[0]>ancho:
        coordenada_calculada[0]=ancho
    if coordenada_calculada[0]<0:
        coordenada_calculada[0]=0
        
    if coordenada_calculada[1]>alto:
        coordenada_calculada[1]=alto
    if coordenada_calculada[1]<0:
        coordenada_calculada[1]=0
    
    return coordenada_calculada

def VERIFICA_ETIQUETADO(VoTT_csv,path_resultado_de_verifica,Mr,M,y_r,x_r,path_img_orig,nombre_de_la_imagen_transf):
    multi_df = pd.read_csv(VoTT_csv)
    #COLOR PARA CLASE 0
    color_0 = (255,0,0)
    #COLOR PARA CLASE 1
    color_1 = (0,255,0)
    #COLOR PARA CLASE 2
    color_2 = (0,0,255)
    nombre_de_la_imagen_anterior=''
    
    
    nom_imagen=[]
    clase_lista=[]
    x_min=[]
    y_min=[]
    x_max=[]
    y_max=[]
    
    for index, row in multi_df.iterrows():
        nombre_de_la_imagen=(row[["image"]].tolist())
        info=(row[["xmin", "ymin", "xmax", "ymax"]].tolist())
        nom_imagen.append(nombre_de_la_imagen[0])
        indice=nombre_de_la_imagen_transf.index(nombre_de_la_imagen[0])
        # print(indice)
        clase=(row[["label"]].tolist())
        clase_lista.append(clase[0])
        if nombre_de_la_imagen != nombre_de_la_imagen_anterior:
            img = cv2.imread(path_img_orig[indice])
            tam_imagen=img.shape
        
        
        info_xymin_transformado=coordenadas_en_vista_original_total(Mr[indice],M,y_r[indice],x_r[indice],info[0],info[1])
        info_xymin_transformado=corrige_cordenadas_que_no_existen(tam_imagen,info_xymin_transformado)
        x_min.append(info_xymin_transformado[0])
        y_min.append(info_xymin_transformado[1])
        
        info_xymax_transformado=coordenadas_en_vista_original_total(Mr[indice],M,y_r[indice],x_r[indice],info[2],info[3])
        info_xymax_transformado=corrige_cordenadas_que_no_existen(tam_imagen,info_xymax_transformado)
        x_max.append(info_xymax_transformado[0])
        y_max.append(info_xymax_transformado[1])
        
        if clase[0]=='CLASE_1':
            #AZUL
            color=color_0
        if clase[0]=='CLASE_2':
            #VERDE
            color=color_1
        if clase[0]=='CLASE_3':
            #ROJO
            color=color_2                           
        cv2.rectangle(img, (int(info_xymin_transformado[0]), int(info_xymin_transformado[1])),(int(info_xymax_transformado[0]), int(info_xymax_transformado[1])), color, 8)
        cv2.putText(img, clase[0], (int(info_xymin_transformado[0]), int(info_xymin_transformado[1])+70), cv2.FONT_HERSHEY_SIMPLEX, 3, color, 4)
        nombre_de_la_imagen_anterior=nombre_de_la_imagen
        
        img_g=cv2.resize(img,(1000,700))
        cv2.imwrite(os.path.join(path_resultado_de_verifica,nombre_de_la_imagen[0]),img_g)
    
        diccionario_para_nuevos_recuadros={'image':nom_imagen,
                                            'xmin': x_min,
                                            'ymin': y_min,
                                            'xmax': x_max,
                                            'ymax': y_max,
                                            'label': clase_lista}
        
        
        df = pd.DataFrame(diccionario_para_nuevos_recuadros, columns = ['image', 'xmin', 'ymin','xmax', 'ymax','label'])
        df.to_csv('recuadros_para_imagenes_originales.csv',index=False)
        
def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)
       
data_matrices_de_transfo=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/factores_de_conversion/info_de_matrices_de_homeografia.pkl') 









VoTT_csv='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/IMAGENES_ETIQUETADAS/vott-csv-export/test_con_json-export.csv'
path_resultado_de_verifica='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/verifica_etiquetado'
try:
    os.mkdir(path_resultado_de_verifica) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
        
        
Mr=data_matrices_de_transfo['Mat_compensa']
M=data_matrices_de_transfo['Mat_bir_eye']
y_r=data_matrices_de_transfo['yr']
x_r=data_matrices_de_transfo['xr']
path_img_orig=data_matrices_de_transfo['nombre_img_orig']
nombre_de_la_imagen_transf=data_matrices_de_transfo['numero_img_transf']


tmstmp1 = time.time()
VERIFICA_ETIQUETADO(VoTT_csv,path_resultado_de_verifica,Mr,M,y_r,x_r,path_img_orig,nombre_de_la_imagen_transf)   
tmstmp2 = time.time()
print('Total time elapsed = ', tmstmp2 - tmstmp1)


