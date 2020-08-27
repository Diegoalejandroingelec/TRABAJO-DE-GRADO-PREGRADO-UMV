import numpy as np
import cv2
import pandas as pd
import time
import pickle
import json


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


def encontrar_clave_para_cada_imagen(path_proyecto_vott):   
    with open(path_proyecto_vott,'r') as miarchivo:
        datos=miarchivo.read()
    
    objeto=json.loads(datos)
    dicci_assets=objeto['assets']
    
    lista_clave=[]
    lista_imagen=[]
    nombre_imagen_original=[]
    for clave, valor in dicci_assets.items(): 
        lista_clave.append(clave)
        lista_imagen.append(valor['path'])
        nombre_imagen_original.append(valor['name'])
        # print(clave)
        # print(valor['path']+'\n')
        
    return lista_clave,lista_imagen,nombre_imagen_original


def rellenar_informacion_asset(ancho,alto,Id_asset,nombre_imagen,path_imagen):
    dicci_size={"width":ancho,
            "height":alto}
    
    dicci_asset={"format": "jpg",
                   "id":Id_asset,
                   "name": nombre_imagen,
                   "path":"file:"+path_imagen,
                   "size":dicci_size,
                   "state":2,
                   "type":1}
    return dicci_asset
def rellenar_informacion_region(sup_iz,sup_de,inf_de,inf_iz,clase,id_region):
    dicci_sup_iz={"x":sup_iz[0],
                  "y":sup_iz[1]}
    
    dicci_sup_de={"x":sup_de[0],
                  "y":sup_de[1]}
    
    dicci_inf_de={"x":inf_de[0],
                  "y":inf_de[1]}
    
    dicci_inf_iz={"x":inf_iz[0],
                  "y":inf_iz[1]}
    
    
    dicci_bounding_box={"height":dicci_inf_iz['y']-dicci_sup_iz['y'],
                        "left":dicci_sup_iz['x'],
                        "top":dicci_sup_iz['y'],
                        "width":dicci_sup_de['x']-dicci_sup_iz['x']}
    
    list_points=[dicci_sup_iz,dicci_sup_de,dicci_inf_de,dicci_inf_iz]
    
    dicci_region={"boundingBox":dicci_bounding_box,
                  "id":"xyzlo"+str(id_region),
                  "points":list_points,
                  "tags":[clase],
                  "type":"RECTANGLE"}  
    return dicci_region
    


def hacer_archivo_json(dicci_asset,lista_dicci_region):
    dicci_total={'asset':dicci_asset,
                 'regions':lista_dicci_region,
                 'version':'2.2.0'}
    with open(dicci_asset['id']+'-asset.json','w') as f:
        json.dump(dicci_total,f)

def ordena_esquinas_del_recuadro(xy_max,xy_min):
    
    if(xy_max[0]>xy_min[0]):
        x_max=xy_max[0]
        x_min=xy_min[0]
    else:
        x_max=xy_min[0]
        x_min=xy_max[0]
        
        
    if(xy_max[1]>xy_min[1]):
        y_max=xy_max[1]
        y_min=xy_min[1]
    else:
        y_max=xy_min[1]
        y_min=xy_max[1]
        
    x_y_max=[x_max,y_max]
    x_y_min=[x_min,y_min]
    
    return x_y_max,x_y_min

def VERIFICA_ETIQUETADO(VoTT_csv,Mr,M,y_r,x_r,path_img_orig,nombre_de_la_imagen_transf,path_proyecto_vott):
    
    lista_clave,lista_imagen,nombre_imagen_original=encontrar_clave_para_cada_imagen(path_proyecto_vott)
    
    multi_df = pd.read_csv(VoTT_csv)
    nombre_de_la_imagen_anterior=''
    
    
    i=0
    lista_dicci_region=[]
    for index, row in multi_df.iterrows():
        nombre_de_la_imagen=(row[["image"]].tolist())
        info=(row[["xmin", "ymin", "xmax", "ymax"]].tolist())
        
        indice=nombre_de_la_imagen_transf.index(nombre_de_la_imagen[0])
        
        
        
        
        # print(indice)
        clase=(row[["label"]].tolist())
      
        if nombre_de_la_imagen != nombre_de_la_imagen_anterior:
            if i!=0:
               hacer_archivo_json(dicci_asset,lista_dicci_region) 
            lista_dicci_region=[]               
            img = cv2.imread(path_img_orig[indice])
            tam_imagen=img.shape
            indice_clave=lista_imagen.index('file:'+path_img_orig[indice])
            clave_img=lista_clave[indice_clave]
            nom_img=nombre_imagen_original[indice_clave]
            dicci_asset=rellenar_informacion_asset(tam_imagen[1],tam_imagen[0],clave_img,nom_img,path_img_orig[indice])

        
        
        
        info_xymin_transformado=coordenadas_en_vista_original_total(Mr[indice],M,y_r[indice],x_r[indice],info[0],info[1])
        info_xymin_transformado=corrige_cordenadas_que_no_existen(tam_imagen,info_xymin_transformado)
        
        
        info_xymax_transformado=coordenadas_en_vista_original_total(Mr[indice],M,y_r[indice],x_r[indice],info[2],info[3])
        info_xymax_transformado=corrige_cordenadas_que_no_existen(tam_imagen,info_xymax_transformado)
        
        info_xymax_transformado,info_xymin_transformado =ordena_esquinas_del_recuadro(info_xymax_transformado,info_xymin_transformado)
        
        dicci_region=rellenar_informacion_region(info_xymin_transformado, [info_xymax_transformado[0],info_xymin_transformado[1]],info_xymax_transformado, [info_xymin_transformado[0],info_xymax_transformado[1]], clase[0], i)
        lista_dicci_region.append(dicci_region)
                      
        nombre_de_la_imagen_anterior=nombre_de_la_imagen
        i=i+1 
     
    hacer_archivo_json(dicci_asset,lista_dicci_region)  
     
    
    
        
        
      
        
def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)
       
data_matrices_de_transfo=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/factores_de_conversion/info_de_matrices_de_homeografia.pkl') 









VoTT_csv='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/IMAGENES_ETIQUETADAS/vott-csv-export/test_con_json-export.csv'
path_proyecto_vott='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/IMAGENES_ORIGINALES_ETIQUETADAS/IMAGENES_ORIGINALES.vott'

        
Mr=data_matrices_de_transfo['Mat_compensa']
M=data_matrices_de_transfo['Mat_bir_eye']
y_r=data_matrices_de_transfo['yr']
x_r=data_matrices_de_transfo['xr']
path_img_orig=data_matrices_de_transfo['nombre_img_orig']
nombre_de_la_imagen_transf=data_matrices_de_transfo['numero_img_transf']


tmstmp1 = time.time()
VERIFICA_ETIQUETADO(VoTT_csv,Mr,M,y_r,x_r,path_img_orig,nombre_de_la_imagen_transf,path_proyecto_vott)   
tmstmp2 = time.time()
print('Total time elapsed = ', tmstmp2 - tmstmp1)



