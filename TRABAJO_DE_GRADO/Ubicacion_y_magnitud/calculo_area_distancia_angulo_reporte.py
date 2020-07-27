import numpy as np
import cv2
import pandas as pd
import math
import pickle
#################################################################
####
####
####                 FUNCIÓN PARA EL CÁLCULO DE DISTANCIA ENTRE 
####                   DOS PUNTOS EN COORDENADAS CARTESIANAS
####
#################################################################
def distancia(coord1,coord2):
    dist=round(np.sqrt((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2))
    return int(dist)
###############################################################
####
####
####         FUNCIÓN PARA EL CÁLCULO DEL ÁNGULO CON RESPECTO
####         A LA HORIZONTAL, EN SENTIDO HORARIO Y TENIENDO
####         LOS DOS CATETOS QUE SE FORMAN
####
###############################################################
def obtener_angulo(cateto_opuesto,cateto_adyasente):
    if cateto_adyasente==0 and cateto_opuesto<0:
        angulo=90
    if cateto_adyasente==0 and cateto_opuesto==0:
        angulo=0
    if cateto_adyasente==0 and cateto_opuesto>0:
        angulo=270
    if cateto_adyasente!=0 and cateto_opuesto==0:
        angulo=0
    if cateto_adyasente!=0 and cateto_opuesto>0:
        angulo=360-math.degrees(math.atan(cateto_opuesto/cateto_adyasente))
    if cateto_adyasente!=0 and cateto_opuesto<0:
        angulo=math.degrees(math.atan(-cateto_opuesto/cateto_adyasente))
    return(angulo)
###############################################################
####
####
####  PROCEDIMIENTO PARA CALCULAR EL PUNTO CENTRAL DEL INICIO
####              DEL CAMPO VISUAL DE LA CÁMARA
####
###############################################################

def PUNTO_CENTRAL_INI_CAMPO_VISUAL(img):    
    #BÚSQUEDA DE LAS COORDENADAS DEL PUNTO CENTRAL DEL INICIO DEL CAMPO VISUAL DE LA CÁMARA
    fila=img.shape[:2][0]
    columnas=img.shape[:2][1]
    flag=0
    flag_1=0
    for i in range(columnas):         
        d_i=img[(fila-1):,i,1]
        i_d=img[(fila-1):,(columnas-1)-i,1]
        if d_i!=0 and flag==0:
            coordenada_in=i
            flag=1
        if i_d!=0 and flag_1==0:
            coordenada_fin=(columnas-1)-i
            flag_1=1
    punto_central=(int(coordenada_fin-(coordenada_fin-coordenada_in)/2),(fila-1))
    return(punto_central)


def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)
       
factor_de_conv_lineal_Vertical=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/factores_de_conversion/factor_conv_lineal_vertical.pkl')
factor_de_conv_lineal_Horizontal=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/factores_de_conversion/factor_conv_lineal_horizontal.pkl')
factor_de_conv_area= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/factores_de_conversion/factor_conv_area.pkl')      
detection_images= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/darknet/detect_images_info/informacion_imagenes.pkl')
#####################################################################
####
####
####      CÁLCULO DEL AREA SUPERFICIAL (CM2) Y UBICACIÓN 
####  ESPACIAL CON DISTANCIA(CM) Y ÁNGULO EN COORDENADAS DEL MUNDO
####             USANDO LOS FACTORES DE CONVERSIÓN 
####
#####################################################################
Folder_reporte='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ubicacion y magnitud'

name_image_List=[]
label=[]
area_estimada=[]
Distancia_estimada=[]
angulo=[]

for n_imagen_detectada in range(len(detection_images)):
    name_image=detection_images[n_imagen_detectada]['image_name']
    img=cv2.imread(name_image,1)
    punto_central=PUNTO_CENTRAL_INI_CAMPO_VISUAL(img)
    for detections_in_one_image in range(len(detection_images[n_imagen_detectada]['detections'])):
        name_image_List.append(name_image)
        label.append(detection_images[n_imagen_detectada]['detections'][detections_in_one_image][0])
        confidence=detection_images[n_imagen_detectada]['detections'][detections_in_one_image][1]
        datos_del_recuadro=detection_images[n_imagen_detectada]['detections'][detections_in_one_image][2]
        area_pixeles=datos_del_recuadro[2]*datos_del_recuadro[3]
        cateto_opuesto=punto_central[0]-int(datos_del_recuadro[0])
        cateto_adyasente=punto_central[1]-int(datos_del_recuadro[1])
        
        angulo.append(obtener_angulo(cateto_opuesto,cateto_adyasente))
        
        area_estimada.append(area_pixeles*factor_de_conv_area)
        
        cateto_adyasente_unidades_del_mundo=factor_de_conv_lineal_Vertical*cateto_adyasente
        cateto_opuesto_unidades_del_mundo=factor_de_conv_lineal_Horizontal*cateto_opuesto
        
        Distancia_estimada.append(math.sqrt(cateto_opuesto_unidades_del_mundo**2+cateto_adyasente_unidades_del_mundo**2))


data = {'PATH IMAGEN':name_image_List,
        'CLASE': label,
        'AREA ESTIMADA': area_estimada,
        'DISTANCIA ESTIMADA': Distancia_estimada,
        'ANGULO ESTIMADO':angulo }
df = pd.DataFrame(data, columns = ['PATH IMAGEN', 'CLASE', 'AREA ESTIMADA','DISTANCIA ESTIMADA', 'ANGULO ESTIMADO'])
df.to_csv('Reporte_detecciones.csv')
        
































