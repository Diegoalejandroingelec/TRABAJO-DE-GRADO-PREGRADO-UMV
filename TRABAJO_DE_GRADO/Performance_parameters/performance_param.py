
import numpy as np
import os
import pickle
import time
import errno
import pandas as pd
import shutil

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

def calcula_interseccion_entre_cuadrados(info,x_min,y_min,x_max,y_max):
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
    if (IoU > 0.7) or ('c15'in tipo )or ('c4' in tipo):
       flag_muy_similares=True 
    if (num_de_pix_intersection*100)/num_de_pix_recuadro_1>80:
        flag_muy_similares=True
    if (num_de_pix_intersection*100)/num_de_pix_recuadro_2>80:
        flag_muy_similares=True
    
    return esta_en_ventana,flag_muy_similares

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

def coordenadas_e_info_bounding_box_2(imagen_info,detection_number):
    yExtent=int(imagen_info['detections'][detection_number][2][3])
    xEntent=int(imagen_info['detections'][detection_number][2][2])
    xCoord=int(imagen_info['detections'][detection_number][2][0]-imagen_info['detections'][detection_number][2][2]/2)
    yCoord=int(imagen_info['detections'][detection_number][2][1]-imagen_info['detections'][detection_number][2][3]/2)
    sup_izq=(xCoord, yCoord)
    inf_der=(xCoord + xEntent, yCoord + yExtent)
    clase=imagen_info['detections'][detection_number][0]
    return sup_izq,inf_der,clase

def elimina_recuadros_superpuestos(detection_images):
    cont=0
    cont2=0
    for imagen_info in detection_images:
        if imagen_info['detections']:
            lista_de_indices_para_eliminar=[]
            for detection_number in range(len(imagen_info['detections'])):
                cont2+=1
                sup_izq,inf_der,clase=coordenadas_e_info_bounding_box_2(imagen_info,detection_number)
                for det_n in range(len(imagen_info['detections'])-detection_number-1):
                    sup_izq1,inf_der1,clase1=coordenadas_e_info_bounding_box_2(imagen_info,det_n+detection_number+1)
                    infor=[sup_izq[0],sup_izq[1],inf_der[0],inf_der[1]]
                    esta_en_ventana,flag_muy_similares=calcula_interseccion_entre_cuadrados(infor,sup_izq1[0],sup_izq1[1],inf_der1[0],inf_der1[1])
                    
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
    GT_etiquetas=0
    Num_predicciones=0
    GT_etiquetas_c=np.zeros(len(las_clases))
    avg_IoU=[]
    clases_TP=[]
    clases_FP=[]
    aux_clases_FP=[]
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
                 confidence_value.append(conf_val)
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
                clase_p_lista_conf=[]
                #Compara etiqueta con todos los recuadros predichos 
                for det in range(len(detection_images[indice]['detections'])):
                    
                    sup_izq_p,inf_der_p,clase_pred,conf_val=coordenadas_e_info_bounding_box(detection_images[indice]['detections'][det])
                    
                    IoU=calcula_IoU(info,sup_izq_p[0],sup_izq_p[1],inf_der_p[0],inf_der_p[1])
                    
                    clase_p_FP.append(clase_pred)
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
                        #confidence_value.append()
                        
                
    
                        
                    
                    
                if not flag_TP:
                    FN_count+=1
                    
                    
            aux_clases_FP.append(clase_p_FP)        
            lista_De_TP.append((TP_list,imagen_name)) 
    
    
    
    for uu in range(len(lista_De_TP)):
        for l_D_TP in range(len(lista_De_TP[uu][0])):
            if lista_De_TP[uu][0][l_D_TP]==0:
                clases_FP.append(aux_clases_FP[uu][l_D_TP])
                
                
                
        
    
    
    
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
        
        print('')
        print('Para la clase '+clases_num[c]+ ' se tiene '+ 'TP: '+str(int(array_cont_clases_TP[c]))+' FP: '+str(int(array_cont_clases_FP[c]))+ ' FN: '+str(int(GT_etiquetas_c[c]-array_cont_clases_TP[c])))
        print('Para la clase '+clases_num[c]+ ' Recall: '+str(array_cont_clases_TP[c]/(array_cont_clases_TP[c]+(GT_etiquetas_c[c]-array_cont_clases_TP[c]))))
        print('Para la clase '+clases_num[c]+ ' Presicion: '+str(array_cont_clases_TP[c]/(array_cont_clases_TP[c]+array_cont_clases_FP[c])))
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
             
                
detection_images= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/darknet/detect_images_info/informacion_imagenes_test_multi_clase.pkl')
txt_path="/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Performance_parameters/test.txt"

path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/JPEGImages/'
path_destino='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Performance_parameters/imagenes_test_multi_clase/'

path_CSV='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Performance_parameters/etiquetas_javi_multi_clase.csv'




#crea_carpeta_con_img_de_test(path_imagenes,path_destino,get_txt_info(txt_path))


tmstmp1 = time.time()
detection_images=elimina_recuadros_superpuestos(detection_images)
IoU_limit=0.2   
calculate_perform_parameters(detection_images,path_CSV,txt_path,IoU_limit)
tmstmp2 = time.time()
print('TIEMPO CONSUMIDO EN EL COMPUTO ES DE: ', tmstmp2 - tmstmp1)