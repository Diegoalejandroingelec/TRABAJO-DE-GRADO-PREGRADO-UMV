import numpy as np
import os
import pickle
import time
import errno
import pandas as pd
import shutil
import matplotlib.pyplot as plt


def calcula_IoU(info,x_min,y_min,x_max,y_max):
    tipo=[]
    flag_muy_similares=False
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
    
    num_de_pix_intersection=(info_aux[2]-info_aux[0])*(info_aux[3]-info_aux[1])
    
    num_de_pix_recuadro_1=(info[2]-info[0])*(info[3]-info[1])
    num_de_pix_recuadro_2=(x_max-x_min)*(y_max-y_min)
    
    IoU=num_de_pix_intersection/((num_de_pix_recuadro_1+num_de_pix_recuadro_2)-num_de_pix_intersection)
      
    return IoU

def calcula_interseccion_entre_cuadrados(info,x_min,y_min,x_max,y_max,IoU_to_merge=1):
    tipo=[]
    flag_muy_similares=False
    esta_en_ventana=False
    flag_IoU_alto=False
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
    
    num_de_pix_intersection=(info_aux[2]-info_aux[0])*(info_aux[3]-info_aux[1])
    
    num_de_pix_recuadro_1=(info[2]-info[0])*(info[3]-info[1])
    num_de_pix_recuadro_2=(x_max-x_min)*(y_max-y_min)
    
    IoU=num_de_pix_intersection/((num_de_pix_recuadro_1+num_de_pix_recuadro_2)-num_de_pix_intersection)
    if (IoU > 0.7) or ('c15'in tipo )or ('c4' in tipo):
       flag_muy_similares=True 
    if (num_de_pix_intersection*100)/num_de_pix_recuadro_1>80:
        flag_muy_similares=True
    if (num_de_pix_intersection*100)/num_de_pix_recuadro_2>80:
        flag_muy_similares=True
    if (IoU >=IoU_to_merge):
        flag_IoU_alto=True
    return esta_en_ventana,flag_muy_similares,flag_IoU_alto

def sup_inf_to_centro_hw(x_min_merg,y_min_merg,x_max_merg,y_max_merg):
    X=(x_max_merg-x_min_merg)/2+x_min_merg
    Y=(y_max_merg-y_min_merg)/2+y_min_merg
    H=(y_max_merg-y_min_merg)
    W=(x_max_merg-x_min_merg)
    return X,Y,W,H

def coordenadas_e_info_bounding_box_2(imagen_info,detection_number):
    yExtent=int(imagen_info['detections'][detection_number][2][3])
    xEntent=int(imagen_info['detections'][detection_number][2][2])
    xCoord=int(imagen_info['detections'][detection_number][2][0]-imagen_info['detections'][detection_number][2][2]/2)
    yCoord=int(imagen_info['detections'][detection_number][2][1]-imagen_info['detections'][detection_number][2][3]/2)
    sup_izq=(xCoord, yCoord)
    inf_der=(xCoord + xEntent, yCoord + yExtent)
    clase=imagen_info['detections'][detection_number][0]
    conf_val=imagen_info['detections'][detection_number][1]
    return sup_izq,inf_der,clase,conf_val

def Merge_bounding_box(IoU_to_merge,detection_big_images):
    detection_big_images_and_merged=[]
    for imagen_info in detection_big_images:
        det_aux=[]
        if imagen_info['detections']:
            # if (imagen_info['image_name']).split('/')[-1]=='1114.jpg':
            #     print('ohoh')
            save_rec_merged=[False]*len(imagen_info['detections'])
            for detection_number in range(len(imagen_info['detections'])):
               
                sup_izq,inf_der,clase,conf_val=coordenadas_e_info_bounding_box_2(imagen_info,detection_number)
                lista_de_recuadros_para_juntar=[]
                lista_de_recuadros_para_juntar.append((sup_izq[0],sup_izq[1],inf_der[0],inf_der[1],clase,conf_val))
                for det_n in range(len(imagen_info['detections'])-detection_number-1):
                    sup_izq1,inf_der1,clase1,conf_val1=coordenadas_e_info_bounding_box_2(imagen_info,det_n+detection_number+1)
                    infor=[sup_izq[0],sup_izq[1],inf_der[0],inf_der[1]]
                    esta_en_ventana,flag_muy_similares,flag_IoU_alto=calcula_interseccion_entre_cuadrados(infor,sup_izq1[0],sup_izq1[1],inf_der1[0],inf_der1[1],IoU_to_merge)
                    
                    if flag_IoU_alto and clase==clase1:
                        lista_de_recuadros_para_juntar.append((sup_izq1[0],sup_izq1[1],inf_der1[0],inf_der1[1],clase1,conf_val1))
                        save_rec_merged[detection_number]=True
                        save_rec_merged[det_n+detection_number+1]=True
                        
                if len(lista_de_recuadros_para_juntar)>1:
                    # print((imagen_info['image_name']).split('/')[-1])
                    save_me=lista_de_recuadros_para_juntar
                    save_me=np.array(save_me)
                    lista_con_los_x=[int(xx) for xx in list(save_me[:,0])+list(save_me[:,2])]
                    lista_con_los_y=[int(yy) for yy in list(save_me[:,1])+list(save_me[:,3])]
                    x_max_merg=int(max(lista_con_los_x))
                    x_min_merg=int(min(lista_con_los_x))
                    y_max_merg=int(max(lista_con_los_y))
                    y_min_merg=int(min(lista_con_los_y))
                    conf_list_float=[float(confi) for confi in list(save_me[:,5])]                   
                    conf_val_merg=max(conf_list_float)
                    clase_merg=save_me[0,4]
                    X,Y,W,H=sup_inf_to_centro_hw(x_min_merg,y_min_merg,x_max_merg,y_max_merg)
                    det_aux.append((clase_merg,conf_val_merg,(X,Y,W,H)))
                if len(lista_de_recuadros_para_juntar)==1:
                    save_me=lista_de_recuadros_para_juntar
                    save_me=np.array(save_me)
                    lista_con_los_x=[int(xx) for xx in list(save_me[:,0])+list(save_me[:,2])]
                    lista_con_los_y=[int(yy) for yy in list(save_me[:,1])+list(save_me[:,3])]
                    x_max_merg=int(max(lista_con_los_x))
                    x_min_merg=int(min(lista_con_los_x))
                    y_max_merg=int(max(lista_con_los_y))
                    y_min_merg=int(min(lista_con_los_y)) 
                    conf_list_float=[float(confi) for confi in list(save_me[:,5])]                   
                    conf_val_merg=max(conf_list_float)
                    clase_merg=save_me[0,4]
                    X,Y,W,H=sup_inf_to_centro_hw(x_min_merg,y_min_merg,x_max_merg,y_max_merg)
                    if save_rec_merged[detection_number]==False:
                        det_aux.append((clase_merg,conf_val_merg,(X,Y,W,H)))
                    
        
        
        detection_big_im_merg={'detections':det_aux,
                          'image_name':imagen_info['image_name']}
        detection_big_images_and_merged.append(detection_big_im_merg)
    return detection_big_images_and_merged

def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)
    
def get_txt_info(txt_path):
    lis_lin=[]
    f = open(txt_path, "r")
    while(True):
        linea = f.readline()
        lis_lin.append(linea)
        if not linea:
            break
    f.close()
    lis_lin.pop()
    aux=[]
    for i in lis_lin:
        aux.append(i.split("/")[-1][:len(i.split("/")[-1])-1])
    lis_lin=aux
    return lis_lin

def crea_carpeta_con_img_de_test(path_imagenes,path_destino,lis_lin):
    try:
        os.mkdir(path_destino) 
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
    
    
    aux_2=[]
    for i in lis_lin:
        aux_2.append(path_imagenes+i)
        
    lis_lin=aux_2
    
    for imagen in lis_lin:
        imagen_copia = path_destino + imagen.split('/')[-1]
        shutil.copy(imagen,imagen_copia)

def coordenadas_e_info_bounding_box(imagen_info):
    yExtent=int(imagen_info[2][3])
    xEntent=int(imagen_info[2][2])
    xCoord=int(imagen_info[2][0]-imagen_info[2][2]/2)
    yCoord=int(imagen_info[2][1]-imagen_info[2][3]/2)
    sup_izq=(xCoord, yCoord)
    inf_der=(xCoord + xEntent, yCoord + yExtent)
    clase=imagen_info[0]
    conf_val=imagen_info[1]
    return sup_izq,inf_der,clase,conf_val

def elimina_recuadros_superpuestos(detection_images):
    cont=0
    cont2=0
    for imagen_info in detection_images:
        if imagen_info['detections']:
            lista_de_indices_para_eliminar=[]
            for detection_number in range(len(imagen_info['detections'])):
                cont2+=1
                sup_izq,inf_der,clase,conf_vla=coordenadas_e_info_bounding_box_2(imagen_info,detection_number)
                for det_n in range(len(imagen_info['detections'])-detection_number-1):
                    sup_izq1,inf_der1,clase1,conf_vla1=coordenadas_e_info_bounding_box_2(imagen_info,det_n+detection_number+1)
                    infor=[sup_izq[0],sup_izq[1],inf_der[0],inf_der[1]]
                    esta_en_ventana,flag_muy_similares,f=calcula_interseccion_entre_cuadrados(infor,sup_izq1[0],sup_izq1[1],inf_der1[0],inf_der1[1])
                    
                    if flag_muy_similares and clase==clase1:
                        bb1=(inf_der[0]-sup_izq[0])*(inf_der[1]-sup_izq[1])
                        bb2=(inf_der1[0]-sup_izq1[0])*(inf_der1[1]-sup_izq1[1])
                        if bb1>bb2:
                            lista_de_indices_para_eliminar.append(det_n+detection_number+1) 
                        if bb2>bb1:
                            lista_de_indices_para_eliminar.append(detection_number)
                        if bb2==bb1:
                            lista_de_indices_para_eliminar.append(detection_number)
                        cont+=1
            for borra in lista_de_indices_para_eliminar:
                imagen_info['detections'][borra]='borrar'
            while('borrar' in imagen_info['detections']):
                imagen_info['detections'].remove('borrar')
    return detection_images
                
def calculate_perform_parameters(detection_images,path_CSV,txt_path,IoU_limit):
    info_txt=get_txt_info(txt_path)
    multi_df = pd.read_csv(path_CSV)
    las_clases=list(multi_df['label'].unique())
    FN_count=0
    TP_count=0
    FP_count=0
    las_clases_para_retornar=[]
    GT_etiquetas=0
    Num_predicciones=0
    GT_etiquetas_c=np.zeros(len(las_clases))
    avg_IoU=[]
    clases_TP=[]
    clases_FP=[]
    aux_clases_FP=[]
    aux_clases_FP_conf=[]
    confidence_value=[]
    for nn in detection_images:
        Num_predicciones+=len(nn['detections'])
        #print(nn['image_name'].split('/')[-1],len(nn['detections'])) 
        
    lista_De_TP=[]    
    for imagen_name in info_txt:
        recuadros_en_la_imagen = multi_df[multi_df['image'] == imagen_name]
        
        
        inicializa_TP=True
        
        
        if recuadros_en_la_imagen.empty:
            for detecciones in range(len(detection_images)):
                if imagen_name==detection_images[detecciones]['image_name'].split('/')[-1]:
                    indice=detecciones
            for det1 in range(len(detection_images[indice]['detections'])):
                 sup_izq_p,inf_der_p,clase_pred,conf_val=coordenadas_e_info_bounding_box(detection_images[indice]['detections'][det1])
                 clases_FP.append(clase_pred) 
                 confidence_value.append((conf_val,clases_FP[-1],'FP'))
            FP_count+=len(detection_images[indice]['detections'])
            
        if not recuadros_en_la_imagen.empty:    
            for index, row in recuadros_en_la_imagen.iterrows():
                flag_TP=False
                info=(row[["xmin", "ymin", "xmax", "ymax"]].tolist())
                clase=(row[["label"]].tolist())[0]
                for ff in range(len(las_clases)):
                    if clase==las_clases[ff]:
                        GT_etiquetas_c[ff]+=1
                        
                GT_etiquetas+=1
                
                for detecciones in range(len(detection_images)):
                    if imagen_name==detection_images[detecciones]['image_name'].split('/')[-1]:
                        indice=detecciones
                if inicializa_TP:        
                    TP_list=np.zeros(len(detection_images[indice]['detections']))
                    inicializa_TP=False
                IoU_list=[]
                det_list=[]
                clase_p_lista=[]
                clase_p_FP=[]
                clase_p_FP_conf=[]
                clase_p_lista_conf=[]
                #Compara etiqueta con todos los recuadros predichos 
                for det in range(len(detection_images[indice]['detections'])):
                    
                    sup_izq_p,inf_der_p,clase_pred,conf_val=coordenadas_e_info_bounding_box(detection_images[indice]['detections'][det])
                    
                    IoU=calcula_IoU(info,sup_izq_p[0],sup_izq_p[1],inf_der_p[0],inf_der_p[1])
                    
                    clase_p_FP.append(clase_pred)
                    clase_p_FP_conf.append(conf_val)
                    if IoU>IoU_limit and clase==clase_pred:
                        IoU_list.append(IoU)
                        det_list.append(det)
                        clase_p_lista.append(clase_pred)
                        clase_p_lista_conf.append(conf_val)
                        #if TP_list[det]==0:
                        #TP_list[det]=1
                        #flag_TP=True
    
                if IoU_list:
                    if TP_list[det_list[IoU_list.index(max(IoU_list))]]!=1:
                        flag_TP=True
                        TP_list[det_list[IoU_list.index(max(IoU_list))]]=1
                        avg_IoU.append(max(IoU_list))
                        clases_TP.append(clase_p_lista[IoU_list.index(max(IoU_list))])
                        confidence_value.append((clase_p_lista_conf[IoU_list.index(max(IoU_list))],clases_TP[-1],'TP'))
                        
                
    
                        
                    
                    
                if not flag_TP:
                    FN_count+=1
                    
                    
            aux_clases_FP.append(clase_p_FP) 
            aux_clases_FP_conf.append(clase_p_FP_conf)
            lista_De_TP.append((TP_list,imagen_name)) 
    
    
    
    for uu in range(len(lista_De_TP)):
        for l_D_TP in range(len(lista_De_TP[uu][0])):
            if lista_De_TP[uu][0][l_D_TP]==0:
                clases_FP.append(aux_clases_FP[uu][l_D_TP])
                confidence_value.append((aux_clases_FP_conf[uu][l_D_TP],clases_FP[-1],'FP'))
                
                
        
    
    
   
    dicci_REC_PRE={'conf':np.array(np.array(confidence_value)[:,0],np.float64),
                    'clase':np.array(confidence_value)[:,1],
                    'TP_FP':np.array(confidence_value)[:,2]}    
    df = pd.DataFrame(dicci_REC_PRE, columns = ['conf', 'clase', 'TP_FP'])
    
    for listas_de_info in lista_De_TP:
        TP_count+=list(listas_de_info[0]).count(1)
        FP_count+=list(listas_de_info[0]).count(0)
        
    clases_num=las_clases
    array_cont_clases_TP=np.zeros(len(clases_num))
    array_cont_clases_FP=np.zeros(len(clases_num))
    u=0
    for para_c_cla in clases_num:
        
        for cla in clases_TP:
            if cla==para_c_cla:
                array_cont_clases_TP[u]+=1
        u+=1
    
    k=0
    for para_c_cla1 in clases_num:
        for cla1 in clases_FP:
            if cla1==para_c_cla1:
                array_cont_clases_FP[k]+=1
        k+=1
    
        
    for c in range(len(clases_num)):
        las_clases_para_retornar.append((GT_etiquetas_c[c],clases_num[c]))
        print('')
        print('Para la clase '+clases_num[c]+ ' se tiene '+ 'TP: '+str(int(array_cont_clases_TP[c]))+' FP: '+str(int(array_cont_clases_FP[c]))+ ' FN: '+str(int(GT_etiquetas_c[c]-array_cont_clases_TP[c])))
        print('Para la clase '+clases_num[c]+ ' Recall: '+str(array_cont_clases_TP[c]/(array_cont_clases_TP[c]+(GT_etiquetas_c[c]-array_cont_clases_TP[c]))))
        print('Para la clase '+clases_num[c]+ ' Presicion: '+str(array_cont_clases_TP[c]/(array_cont_clases_TP[c]+array_cont_clases_FP[c])))
        Pre=array_cont_clases_TP[c]/(array_cont_clases_TP[c]+array_cont_clases_FP[c])
        Rec=array_cont_clases_TP[c]/(array_cont_clases_TP[c]+(GT_etiquetas_c[c]-array_cont_clases_TP[c]))
        print('Para la clase '+clases_num[c]+ ' F1-score: '+str(2*(Pre*Rec)/(Pre+Rec)))
        print('')
        
    print('LOS PARAMETROS TOTALES SON:')
    print('TP: '+str(TP_count))
    print('FP: '+str(FP_count))
    print('FN: '+str(FN_count))
    
    
    print('Presicion '+str(TP_count/(TP_count+FP_count)))
    print('Recall '+str(TP_count/(TP_count+FN_count)))
    def promediarLista(lista):
        suma=0.0
        for i in range(0,len(lista)):
            suma=suma+lista[i]
     
        return suma/len(lista)
    
    print('Avg_IoU',promediarLista(avg_IoU))
    
    if (TP_count+FN_count-(GT_etiquetas))!=0 or (Num_predicciones-(TP_count+FP_count))!=0: 
        print('ERROR!!!!')
    return df,las_clases_para_retornar
             
def interp_prec(recall,precision,clase_name):
    list_for_graphic_R=[]
    list_for_graphic_P=[]
    precision2=precision.copy()
    i=len(recall)-2
    
    # interpolation...
    while i>=0:
        if precision[i+1]>precision[i]:
            precision[i]=precision[i+1]
        i=i-1
    
    # plotting...
    fig, ax = plt.subplots()
    for i in range(len(recall)-1):
        list_for_graphic_R.append(recall[i])
        list_for_graphic_P.append(precision[i])
        list_for_graphic_R.append(recall[i])
        list_for_graphic_P.append(precision[i+1])
        
        list_for_graphic_R.append(recall[i])
        list_for_graphic_P.append(precision[i+1])
        list_for_graphic_R.append(recall[i+1])
        list_for_graphic_P.append(precision[i+1])
    ax.plot(list_for_graphic_R,list_for_graphic_P,'-',label='Interpolado',color='red')
    #ax.legend('Interpolado')
    ax.plot(recall,precision2,'k--',label='No interpolado',color='green')
    ax.legend()
    plt.title('Recall vs Precision'+' clase '+ clase_name)
    ax.set_xlabel("Recall")
    ax.set_ylabel("Precision")
    ax.grid(True)
    plt.savefig('Recall_Precision_'+clase_name+'.eps')
    plt.show()
    return precision

def Compute_map(data_frame,ground_truth):
    clases_en_df=list(data_frame['clase'].unique())
    df_por_clases=[None]*len(clases_en_df)
    
    for n in range(len(clases_en_df)):
        df_por_clases[n]=data_frame[data_frame['clase'] ==clases_en_df[n]]
        
    for n in range(len(clases_en_df)):
        df_por_clases[n]=df_por_clases[n].sort_values('conf',ascending=False)
        
    acum_AP=0   
    for data_frame_n in df_por_clases:
        K=data_frame_n['TP_FP'].value_counts()
        for gth in ground_truth:
            if list(data_frame_n['clase'].unique())[0]==gth[1]:
                K_recall=gth[0]
                
        #print(K_recall,list(data_frame_n['clase'].unique())[0])        
        rec_g=[]
        pre_g=[]
        cont=0
        cont_true_p=0
        for i in list(data_frame_n['TP_FP']):
            cont+=1
            if i=='TP':
                cont_true_p+=1
                
            rec_g.append(cont_true_p/K_recall)
            pre_g.append(cont_true_p/cont)
        
        rec_ant=''
        premax=[]
        pre_interp=[]
        f_t=True   
        for r,p in zip(rec_g,pre_g):  
            premax.append(p)
            if rec_ant!=r and f_t==False:
                aux=premax.pop()
                max_prec=max(premax)
                for n in range(len(premax)):
                    pre_interp.append(max_prec)
                
                premax=[]    
                premax.append(aux)
            f_t=False
            rec_ant=r
        max_prec=max(premax)
        for n in range(len(premax)):
            pre_interp.append(max_prec)  
            
        clase_name=list(data_frame_n['clase'].unique())[0]    
        pre_interp=interp_prec(rec_g,pre_interp,clase_name)    
        
    
        print('')
        print('para la clase '+clase_name+' el AP es '+str(sum(pre_interp)/K_recall))
        print('')
        
        
        
        acum_AP+=sum(pre_interp)/K_recall
    
    mAP=acum_AP/len(df_por_clases)
    
    print('El mAP@'+str(IoU_limit)+' es de '+str(mAP))
    
    
    tmstmp2 = time.time()
    print('TIEMPO CONSUMIDO EN EL COMPUTO ES DE: ', tmstmp2 - tmstmp1)              



detection_images= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/darknet/detect_images_info/informacion_imagenes_test_UMV.pkl')
txt_path="/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Performance_parameters/UMV_data/test.txt"


path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/UMV/JPEGImages/'

path_destino='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Performance_parameters/imagenes_test_UMV/'

path_CSV='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Performance_parameters/UMV_data/etiquetas_umv_ventaneadas.csv'




#crea_carpeta_con_img_de_test(path_imagenes,path_destino,get_txt_info(txt_path))


tmstmp1 = time.time()
detection_images=elimina_recuadros_superpuestos(detection_images)

IoU_to_merge=0.2
detection_images=Merge_bounding_box(IoU_to_merge,detection_images)

IoU_limit=0.2   
data_frame,ground_truth=calculate_perform_parameters(detection_images,path_CSV,txt_path,IoU_limit)
Compute_map(data_frame,ground_truth)





















