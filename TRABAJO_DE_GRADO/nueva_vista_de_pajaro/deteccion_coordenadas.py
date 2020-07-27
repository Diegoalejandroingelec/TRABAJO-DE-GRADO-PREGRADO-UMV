import numpy as np
import cv2
###############################################################
####
####
####                 DETECCIÓN DE ESQUINAS
####
####
###############################################################
BAN=False
def pnt1 (event,x,y,flags,param):
    global refpnt
    global BAN
    if BAN==False:
        BAN=True
        refpnt=[]
    if event == cv2.EVENT_FLAG_LBUTTON:
        refpnt.append([x,y])
        print('x= '+str(x)+ ', y= '+ str(y))

def deteccion_esquinas(path_imagenes,scale_percent=38):
    refpnt=[]
    img_patron = cv2.imread(path_imagenes)
    #cv2.imshow('IMAGEN ORIGINAL',img_patron)
    #cv2.waitKey(0)
    width_original=img_patron.shape[1]
    height_original=img_patron.shape[0]
    print(height_original,width_original)
    img_patron.shape[0]
    width = int(img_patron.shape[1] * scale_percent / 100)
    height = int(img_patron.shape[0] * scale_percent / 100)
    dim = (width, height)
    print(dim)
    #cv2.imshow('IMAGEN ORIGINAL SIN DISTORSION POR CAMARA',img_patron)
    #cv2.waitKey(0)
    
    
    esquinas_1234=cv2.resize(img_patron  , dim)
    cv2.namedWindow('Esquinas Segmentadas')
    cv2.setMouseCallback('Esquinas Segmentadas', pnt1)
    cv2.imshow('Esquinas Segmentadas', esquinas_1234)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    coord_sup_izquierda=np.array([int(refpnt[0][0]*(width_original/width)),int(refpnt[0][1]*(height_original/height))])
    coord_sup_derecha=np.array([int(refpnt[1][0]*(width_original/width)),int(refpnt[1][1]*(height_original/height))])
    coord_inf_izquierda=np.array([int(refpnt[2][0]*(width_original/width)),int(refpnt[2][1]*(height_original/height))])
    coord_inf_derecha=np.array([int(refpnt[3][0]*(width_original/width)),int(refpnt[3][1]*(height_original/height))])
    
    # coord_sup_izquierda=np.array([int(refpnt[0][0]),int(refpnt[0][1])])
    # coord_sup_derecha=np.array([int(refpnt[1][0]),int(refpnt[1][1])])
    # coord_inf_izquierda=np.array([int(refpnt[2][0]),int(refpnt[2][1])])
    # coord_inf_derecha=np.array([int(refpnt[3][0]),int(refpnt[3][1])])
    return coord_sup_izquierda,coord_sup_derecha,coord_inf_derecha,coord_inf_izquierda,img_patron,dim

scale_percent=30
path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/RESULTADOS_1234/0.jpg'
coord_sup_izquierda,coord_sup_derecha,coord_inf_derecha,coord_inf_izquierda,img_patron,dim_resize=deteccion_esquinas(path_imagenes,scale_percent)
scale_percent=30
path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/RESULTADOS_1234/66666.jpg'
coord_sup_izquierda1,coord_sup_derecha1,coord_inf_derecha1,coord_inf_izquierda1,img_patron1,dim_resize1=deteccion_esquinas(path_imagenes,scale_percent)
