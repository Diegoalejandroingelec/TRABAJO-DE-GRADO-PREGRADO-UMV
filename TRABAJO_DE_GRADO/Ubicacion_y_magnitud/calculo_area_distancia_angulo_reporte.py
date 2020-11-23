import numpy as np
import cv2
import pandas as pd
import math
import pickle
import gmplot
import geomag
from funciones_posicion import move_position

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
#####################################################################
####
####
####      CÁLCULO DEL AREA SUPERFICIAL (CM2) Y UBICACIÓN 
####  ESPACIAL CON DISTANCIA(CM) Y ÁNGULO EN COORDENADAS DEL MUNDO
####             USANDO LOS FACTORES DE CONVERSIÓN 
####
#####################################################################       

def crea_reporte(path_reporte,factor_de_conv_lineal_Vertical,factor_de_conv_lineal_Horizontal,factor_de_conv_area,relacion_nombre_o_con_nombre_transformado,detection_images):
    name_image_List=[]
    label=[]
    area_estimada=[]
    Distancia_estimada=[]
    angulo=[]
    for n_imagen_detectada in range(len(detection_images)):
        if not not detection_images[n_imagen_detectada]['detections']:
            name_image=detection_images[n_imagen_detectada]['image_name']
            img=cv2.imread(name_image,1)
            punto_central=PUNTO_CENTRAL_INI_CAMPO_VISUAL(img)
            for detections_in_one_image in range(len(detection_images[n_imagen_detectada]['detections'])):
                nombre_orig_img=relacion_nombre_o_con_nombre_transformado['nombre_img_orig'][relacion_nombre_o_con_nombre_transformado['numero_img_transf'].index(name_image.split('/')[-1])].split('/')[-1]
                name_image_List.append(nombre_orig_img)
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
    
    
    data = {'IMAGEN':name_image_List,
            'CLASE': label,
            'AREA ESTIMADA': area_estimada,
            'DISTANCIA ESTIMADA': Distancia_estimada,
            'ANGULO ESTIMADO':angulo }
    df = pd.DataFrame(data, columns = ['IMAGEN', 'CLASE', 'AREA ESTIMADA','DISTANCIA ESTIMADA', 'ANGULO ESTIMADO'])
    df.to_csv(path_reporte,index=False)




def obtener_posicion_original(dato):
    contador = 0
    n = ''
    lat1 = ''
    lon1 = ''
    lat2 = ''
    lon2 = ''
    lat3 = ''
    lon3 = ''
    x = ''
    y = ''
    z = ''
    norte = ''
    l = ''
    for d in dato:
        if d == ',':
            contador+=1
        
        else:
            
            if contador == 0:
                n = n + d
                
            if contador == 1:
                lat1 = lat1 + d
                
            if contador == 2:
                lon1 = lon1 + d
            
            if contador == 3:
                lat2 = lat2 + d
                
            if contador == 4:
                lon2 = lon2 + d
                
            if contador == 5:
                lat3 = lat3 + d
                
            if contador == 6:
                lon3 = lon3 + d
        
            if contador == 7:
                x = x + d
                
            if contador == 8:
                y = y + d
                
            if contador == 9:
                z = z + d
                
            if contador == 10:
                norte = norte + d
                
            if contador == 11:
                l = l + d
    
    latitud = 0
    longitud = 0
    
    if n == '1':
        if not (lat1 == ' ') and not (lon1 == ' '):
            latitud = float(lat1)
            longitud = float(lon1)
            
        if not (lat2 == ' ') and not (lon2 == ' '):
            latitud = float(lat2)
            longitud = float(lon2)
            
        if not (lat3 == ' ') and not (lon3 == ' '):
            latitud = float(lat3)
            longitud = float(lon3)
        
    if n == '2':
        if not (lat1 == ' ') and not (lon1 == ' ') and not (lat2 == ' ') and not (lon2 == ' '):
            latitud = (float(lat1) + float(lat2))/2
            longitud = (float(lon1) + float(lon2))/2
            
        if not (lat1 == ' ') and not (lon1 == ' ') and not (lat3 == ' ') and not (lon3 == ' '):
            latitud = (float(lat1) + float(lat3))/2
            longitud = (float(lon1) + float(lon3))/2
            
        if not (lat2 == ' ') and not (lon2 == ' ') and not (lat3 == ' ') and not (lon3 == ' '):
            latitud = (float(lat2) + float(lat3))/2
            longitud = (float(lon2) + float(lon3))/2
            
    if n == '3':
        latitud = (float(lat1)+float(lat2)+float(lat3))/3
        longitud = (float(lon1)+float(lon2)+float(lon3))/3

    return latitud,longitud,float(norte)


def Georeferenciacion(archivo_fallas,path_datos,path_reporte,path_mapa_fallas,relacion_nombre_o_con_nombre_transformado):
    fallas = pd.read_csv(archivo_fallas, sep=',', index_col=0)
    datos_fallas = []
    
    latitud_grieta = []
    longitud_grieta = []
    latitud_hueco = []
    longitud_hueco = []
    latitud_parche = []
    longitud_parche = []
    latitud_piel_c = []
    longitud_piel_c = []
    latitud_original = []
    longitud_original = []
    
    datos_fallas = {
        "NOMBRE":[] ,
        "CLASE":[],
        "AREA":[],
        "LATITUD":[],
        "LONGITUD":[]
        }
    
    for i in range(len(fallas)):
        
        
        nombre_archivo = path_datos + fallas.index[i][0:(len(fallas.index[i])-4)] + '.txt'
        try:
            file = open(nombre_archivo,'r')
            datos = file.read()
            file.close
        except:
            latitud_carro=0
            longitud_carro=0
        
        latitud_carro,longitud_carro,angulo_n = obtener_posicion_original(datos)
        
        if not(latitud_carro == 0 and longitud_carro == 0 ):
            
            if not(latitud_carro in latitud_original) and not(longitud_carro in longitud_original):
                latitud_original.append(latitud_carro)
                longitud_original.append(longitud_carro)
            declinacion_m = geomag.declination(latitud_carro,longitud_carro)
            latitud_falla,longitud_falla = move_position(latitud_carro,longitud_carro,angulo_n+declinacion_m,fallas['DISTANCIA ESTIMADA'][i]/100,fallas['ANGULO ESTIMADO'][i])
        
            if fallas['CLASE'][i] == 'grieta':
                latitud_grieta.append(latitud_falla)
                longitud_grieta.append(longitud_falla)
            elif fallas['CLASE'][i] == 'hueco':
                latitud_hueco.append(latitud_falla)
                longitud_hueco.append(longitud_falla)
            elif fallas['CLASE'][i] == 'parche':
                latitud_parche.append(latitud_falla)
                longitud_parche.append(longitud_falla)
            else:
                latitud_piel_c.append(latitud_falla)
                longitud_piel_c.append(longitud_falla)
            
            
            
            path_aux=relacion_nombre_o_con_nombre_transformado['nombre_img_orig'][0].strip(relacion_nombre_o_con_nombre_transformado['nombre_img_orig'][0].split("/")[-1])
            indice_j=relacion_nombre_o_con_nombre_transformado['nombre_img_orig'].index(path_aux+fallas.index[i])
            
            datos_fallas["NOMBRE"].append(relacion_nombre_o_con_nombre_transformado['numero_img_transf'][indice_j])  
            datos_fallas["CLASE"].append(fallas['CLASE'][i])
            datos_fallas["AREA"].append(fallas['AREA ESTIMADA'][i])
            datos_fallas["LATITUD"].append(latitud_falla)
            datos_fallas["LONGITUD"].append(longitud_falla)
            
            
    df = pd.DataFrame(datos_fallas,columns=['NOMBRE','CLASE','AREA','LATITUD','LONGITUD'])
    df.to_csv(path_reporte,index=False)
    
    gmap1 = gmplot.GoogleMapPlotter(4.634058, -74.068737, 16 ) 
    #gmap1.scatter( latitud_original, longitud_original, '#06F5F9',size = 2, marker = False )
    gmap1.scatter( latitud_grieta, longitud_grieta, '#F2F906',size = 1, marker = False )
    gmap1.scatter( latitud_hueco, longitud_hueco, '#F90A06',size = 1, marker = False )
    gmap1.scatter( latitud_parche, longitud_parche, '#06F5F9',size = 1, marker = False )
    gmap1.scatter( latitud_piel_c, longitud_piel_c, '#58FA82',size = 1, marker = False )
    
    gmap1.draw(path_mapa_fallas)








factor_de_conv_lineal_Vertical=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/img_dia2/factores_de_conversion/factor_conv_lineal_vertical.pkl')
factor_de_conv_lineal_Horizontal=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/img_dia2/factores_de_conversion/factor_conv_lineal_horizontal.pkl')
factor_de_conv_area= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/img_dia2/factores_de_conversion/factor_conv_area.pkl')      
relacion_nombre_o_con_nombre_transformado=load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/img_dia2/factores_de_conversion/info_de_matrices_de_homeografia.pkl')
detection_images= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Recuadros_contenedores/info_deteccion_img_grande/informacion_imagenes_grandes_dia_2.pkl')

path_reporte='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ubicacion_y_magnitud/Reporte_detecciones_dia2.csv'
path_mapa_fallas="/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Ubicacion_y_magnitud/mapa_fallas_Dia_2.html"


archivo_fallas = path_reporte
path_datos ="/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/img_dia2/"

crea_reporte(path_reporte,factor_de_conv_lineal_Vertical,factor_de_conv_lineal_Horizontal,factor_de_conv_area,relacion_nombre_o_con_nombre_transformado,detection_images)

Georeferenciacion(archivo_fallas,path_datos,path_reporte,path_mapa_fallas,relacion_nombre_o_con_nombre_transformado)




def busca(name):
    nombre='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/66_grados/'
    i=relacion_nombre_o_con_nombre_transformado['nombre_img_orig'].index(nombre+name)
    a=relacion_nombre_o_con_nombre_transformado['numero_img_transf'][i]
    print(a)

















