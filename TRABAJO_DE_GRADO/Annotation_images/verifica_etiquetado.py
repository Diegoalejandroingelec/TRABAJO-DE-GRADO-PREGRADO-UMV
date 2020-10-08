import numpy as np
import cv2
import glob
import os
import pandas as pd
import errno
import time
import pickle

def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)
    
# def genera_etiquetas_imagenes_G(csv_de_img_ventaneadas):
#     multi_df = pd.read_csv(csv_de_img_ventaneadas)
#     multi_df=multi_df.sort_values('image')
#     info_list=[]
#     dicci_ventaneado=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/datos_del_ventaneado/datos_ventaneado.pkl')
#     for index, row in multi_df.iterrows():
#         nombre_de_la_imagen=(row[["image"]].tolist())[0]
        
#         info=(row[["image","xmin", "ymin", "xmax", "ymax","label"]].tolist())
        

        
        
        
#         indice=dicci_ventaneado['imagen'].index(nombre_de_la_imagen[0:len(nombre_de_la_imagen)-11]+'.jpg')
#         alto_m=dicci_ventaneado['alto_m'][indice]
#         ancho_m=dicci_ventaneado['ancho_m'][indice]
#         coord_ini=dicci_ventaneado['coo_ini'][indice]

#         if indicador=="_sup_iz":
#             info[0]=nombre_de_la_imagen[0:len(nombre_de_la_imagen)-11]+'.jpg'
#             info_list.append(info)
#         if indicador=="_sup_de":
#             info[0]=nombre_de_la_imagen[0:len(nombre_de_la_imagen)-11]+'.jpg'
#             info[1]=info[1]+ancho_m
#             info[3]=info[3]+ancho_m
#             info_list.append(info)
#         if indicador=="_inf_iz":
#             info[0]=nombre_de_la_imagen[0:len(nombre_de_la_imagen)-11]+'.jpg'
#             info[1]=info[1]+coord_ini
#             info[2]=info[2]+alto_m
#             info[3]=info[3]+coord_ini
#             info[4]=info[4]+alto_m
#             info_list.append(info)
#         if indicador=="_inf_de":
#             info[0]=nombre_de_la_imagen[0:len(nombre_de_la_imagen)-11]+'.jpg'
#             info[1]=info[1]+ancho_m
#             info[2]=info[2]+alto_m
#             info[3]=info[3]+ancho_m
#             info[4]=info[4]+alto_m
#             info_list.append(info)
            
       
#     df = pd.DataFrame(info_list)    
#     df=df.rename(columns={0:"image",1:"xmin",2:"ymin",3:"xmax",4:"ymax",5:"label"})
#     df.to_csv('etiquetas_de_imagenes_grandes_generadas_con_imagenes_pequeñas.csv',index=False)
    
    
    

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
            #print("imagen cargada "+nombre_de_la_imagen[0])
            img = cv2.imread(path_im_prueba+nombre_de_la_imagen[0])
        
        if clase[0]=='falla':
            #AZUL
            color=color_0
        if clase[0]=='libro_cerrado':
            #VERDE
            color=color_1
        if clase[0]=='libro_abierto':
            #ROJO
            color=color_2                           
        cv2.rectangle(img, (int(info[0]), int(info[1])),(int(info[2]), int(info[3])), color, 3)
        #cv2.putText(img, str(row[["num_rec"]].tolist()[0]), (int(info[0]), int(info[1])+30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 1)
        nombre_de_la_imagen_anterior=nombre_de_la_imagen
        
        #img_g=cv2.resize(img,(1000,700))
        img_g=img
        cv2.imwrite(os.path.join(path_resultado_de_verifica,nombre_de_la_imagen[0]),img_g)
    
    
    todas_las_images_en_la_carpeta = glob.glob(path_im_prueba+'*.jpg')
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
            
    print(len(todas_las_images_en_la_carpeta))
    print(len(imagenes_sin_clases_de_interes))
    print(len(imagenes_con_clases_de_interes))
    for n in range(len(imagenes_sin_clases_de_interes)):
#        print(imagenes_sin_clases_de_interes[n])
        img = cv2.imread(path_im_prueba+imagenes_sin_clases_de_interes[n])
       # img_g=cv2.resize(img,(1000,700))
        cv2.imwrite(os.path.join(path_resultado_de_verifica,imagenes_sin_clases_de_interes[n]),img)





path_im_prueba='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/66_grados/imagenes_recortadas/img_etiquetadas/vott-csv-export/'

VoTT_csv='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/66_grados/imagenes_recortadas/img_etiquetadas/vott-csv-export/fallas_dia1-export.csv'
VoTT_csv_de_img_ventaneadas='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/IMAGENES_ETIQUETADAS/vott-csv-export/archivo_fusionado.csv'


path_resultado_de_verifica='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/verifica_etiquetado'


try:
    os.mkdir(path_resultado_de_verifica) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
tmstmp1 = time.time()

#genera_etiquetas_imagenes_G(VoTT_csv_de_img_ventaneadas)
VERIFICA_ETIQUETADO(VoTT_csv,path_resultado_de_verifica,path_im_prueba)   
tmstmp2 = time.time()
print('Total time elapsed = ', tmstmp2 - tmstmp1)


















