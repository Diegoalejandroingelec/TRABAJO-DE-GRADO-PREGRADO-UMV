import numpy as np
import cv2
import pickle
import os
import errno

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

def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)
    
def save_obj(obj, name ):
    with open('info_deteccion_img_grande/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def crear_carpeta(path):
    try:
        os.mkdir(path) 
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise 
            
def coordenadas_e_info_bounding_box(imagen_info,detection_number):
    yExtent=int(imagen_info['detections'][detection_number][2][3])
    xEntent=int(imagen_info['detections'][detection_number][2][2])
    xCoord=int(imagen_info['detections'][detection_number][2][0]-imagen_info['detections'][detection_number][2][2]/2)
    yCoord=int(imagen_info['detections'][detection_number][2][1]-imagen_info['detections'][detection_number][2][3]/2)
    sup_izq=(xCoord, yCoord)
    inf_der=(xCoord + xEntent, yCoord + yExtent)
    clase=imagen_info['detections'][detection_number][0]
    conf_val=imagen_info['detections'][detection_number][1]
    return sup_izq,inf_der,clase,conf_val

def limpia_recuadros_parecidos_y_anidados(detection_big_images):
    for imagen_info in detection_big_images:
        if imagen_info['detections']:
            lista_de_indices_para_eliminar=[]
            for detection_number in range(len(imagen_info['detections'])):
                
                sup_izq,inf_der,clase,conf_val=coordenadas_e_info_bounding_box(imagen_info,detection_number)
                for det_n in range(len(imagen_info['detections'])-detection_number-1):
                    sup_izq1,inf_der1,clase1,conf_val=coordenadas_e_info_bounding_box(imagen_info,det_n+detection_number+1)
                    infor=[sup_izq[0],sup_izq[1],inf_der[0],inf_der[1]]
                    esta_en_ventana,flag_muy_similares,flag_IoU_alto=calcula_interseccion_entre_cuadrados(infor,sup_izq1[0],sup_izq1[1],inf_der1[0],inf_der1[1])
                    
                    if flag_muy_similares and clase==clase1:
                        bb1=(inf_der[0]-sup_izq[0])*(inf_der[1]-sup_izq[1])
                        bb2=(inf_der1[0]-sup_izq1[0])*(inf_der1[1]-sup_izq1[1])
                        if bb1>bb2:
                            lista_de_indices_para_eliminar.append(det_n+detection_number+1) 
                        if bb2>bb1:
                            lista_de_indices_para_eliminar.append(detection_number)
                        if bb2==bb1:
                            lista_de_indices_para_eliminar.append(detection_number)
                        
            for borra in lista_de_indices_para_eliminar:
                imagen_info['detections'][borra]='borrar'
            while('borrar' in imagen_info['detections']):
                imagen_info['detections'].remove('borrar')
    return detection_big_images            
          
def sup_inf_to_centro_hw(x_min_merg,y_min_merg,x_max_merg,y_max_merg):
    X=(x_max_merg-x_min_merg)/2+x_min_merg
    Y=(y_max_merg-y_min_merg)/2+y_min_merg
    H=(y_max_merg-y_min_merg)
    W=(x_max_merg-x_min_merg)
    return X,Y,W,H

def Merge_bounding_box(IoU_to_merge,detection_big_images):
    detection_big_images_and_merged=[]
    for imagen_info in detection_big_images:
        det_aux=[]
        if imagen_info['detections']:
            # if (imagen_info['image_name']).split('/')[-1]=='1114.jpg':
            #     print('ohoh')
            save_rec_merged=[False]*len(imagen_info['detections'])
            for detection_number in range(len(imagen_info['detections'])):
               
                sup_izq,inf_der,clase,conf_val=coordenadas_e_info_bounding_box(imagen_info,detection_number)
                lista_de_recuadros_para_juntar=[]
                lista_de_recuadros_para_juntar.append((sup_izq[0],sup_izq[1],inf_der[0],inf_der[1],clase,conf_val))
                for det_n in range(len(imagen_info['detections'])-detection_number-1):
                    sup_izq1,inf_der1,clase1,conf_val1=coordenadas_e_info_bounding_box(imagen_info,det_n+detection_number+1)
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

def Make_draw_bounding_box(detection_big_images_and_merged):    
    color_0 = (0,0,255)
    color_1 = (255,0,0)
    color_2 = (0,255,0)
    color_3 = (255,0,255)    
    for imagen_info in detection_big_images_and_merged:
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
                clase=imagen_info['detections'][detection_number][0]
                if clase=='hueco':
                    color=color_0
                if clase == 'piel_de_cocodrilo':
                    color=color_1
                if clase=='parche':
                    color=color_2
                if clase == 'grieta':
                    color=color_3
                    
                cv2.rectangle(img,sup_izq,inf_der, color, 2)
                proba=imagen_info['detections'][detection_number][1]
                #cv2.putText(img,clase+' '+str("{:.2f}".format(proba*100))+'%', sup_izq_titulo, cv2.FONT_HERSHEY_SIMPLEX, 2, color_0, 3)
                #cv2.putText(img,clase[0], sup_izq_titulo, cv2.FONT_HERSHEY_SIMPLEX, 2, color, 3)
            
            
    #        img_g=cv2.resize(img,(2500,1500))
            cv2.imwrite(os.path.join(path_imagenes_boundingbox,imagen_info['image_name'].split("/")[-1]),img)
            
        if not imagen_info['detections']:    
            img=cv2.imread(imagen_info['image_name'])
      #       img_g=cv2.resize(img,(2500,1500))
            cv2.imwrite(os.path.join(path_imagenes_boundingbox,imagen_info['image_name'].split("/")[-1]),img)

def usa_detec_de_img_peque_para_hacer_detec_de_img_grandes(detection_images,dicci_ventaneado,path_imagenes_grandes):
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
    return detection_big_images    
           
            
path_resultado_de_deteccion_img_big='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Recuadros_contenedores/info_deteccion_img_grande'

dicci_ventaneado=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ventanear_imagenes/datos_del_ventaneado/datos_ventaneado_dia1.pkl')    
detection_images= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/darknet/detect_images_info/informacion_imagenes_dia1_multi_clase.pkl')
path_imagenes_boundingbox='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Recuadros_contenedores/resultados_dia1_multiclase_and_merged_111'

path_imagenes_grandes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/66_grados/imagenes_recortadas/img_etiquetadas/vott-csv-export/'

crear_carpeta(path_imagenes_boundingbox)
crear_carpeta(path_resultado_de_deteccion_img_big)


#detection_big_images=usa_detec_de_img_peque_para_hacer_detec_de_img_grandes(detection_images,dicci_ventaneado,path_imagenes_grandes)
detection_big_images=detection_images

detection_big_images=limpia_recuadros_parecidos_y_anidados(detection_big_images)                
IoU_to_merge=0.20
detection_big_images_and_merged=Merge_bounding_box(IoU_to_merge,detection_big_images)            
#save_obj(detection_big_images_and_merged, 'informacion_imagenes_grandes_dia_1' )           
Make_draw_bounding_box(detection_big_images_and_merged)    




