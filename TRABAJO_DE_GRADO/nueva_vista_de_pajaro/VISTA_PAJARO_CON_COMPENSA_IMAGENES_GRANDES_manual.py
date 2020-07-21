import numpy as np
import cv2
import glob
import os
import math
import pickle
import time
import errno
###############################################################
####
####
####                 FUNCIÓN PARA EL CÁLCULO DE DISTANCIA ENTRE 
####                   DOS PUNTOS EN COORDENADAS CARTESIANAS
####
###############################################################
def distancia(coord1,coord2):
    dist=round(np.sqrt((coord1[0]-coord2[0])**2+(coord1[1]-coord2[1])**2))
    return int(dist)
###############################################################
####
####
####                 FUNCIÓN PARA ELIMINAR DISTORSIÓN RADIAL 
####                      Y TANGENCIAL DE LA CÁMARA
####
###############################################################
def undistorted_images(imagen,mtx,dist):
    h,  w = imagen.shape[:2]
    newcameramtx, roi=cv2.getOptimalNewCameraMatrix(mtx,dist,(w,h),1,(w,h))
    # undistort
    dst = cv2.undistort(imagen, mtx, dist, None, newcameramtx)
    #crop the image
    x,y,w,h = roi
    dst = dst[y:y+h, x:x+w]
    return dst

###############################################################
####
####
####                 FUNCIÓN PARA CALCULAR LAS COORDENADAS 
####                 EN LA IMÁGEN CON VISTA DE PÁJARO TENIENDO 
####                 LAS COORDENADAS DE LA IMÁGEN ORIGINAL Y 
####                 LA MATRIZ DE HOMEOGRAFÍA M
####
###############################################################
def coordenadas_en_vista_de_pajaro(M,x_1,y_1):
    coordenadas_imagen_vista_pajaro=np.int32([((M[1,1]*M[2,2]-M[1,2]*M[2,1])*x_1-(M[0,1]*M[2,2]-M[0,2]*M[2,1])*y_1+(M[0,1]*M[1,2]-M[0,2]*M[1,1]))/((M[1,0]*M[2,1]-M[1,1]*M[2,0])*x_1-(M[0,0]*M[2,1]-M[0,1]*M[2,0])*y_1+(M[0,0]*M[1,1]-M[0,1]*M[1,0])),      -((M[1,0]*M[2,2]-M[1,2]*M[2,0])*x_1-(M[0,0]*M[2,2]-M[0,2]*M[2,0])*y_1+(M[0,0]*M[1,2]-M[0,2]*M[1,0]))/((M[1,0]*M[2,1]-M[1,1]*M[2,0])*x_1-(M[0,0]*M[2,1]-M[0,1]*M[2,0])*y_1+(M[0,0]*M[1,1]-M[0,1]*M[1,0]))])
    return coordenadas_imagen_vista_pajaro



###############################################################
####
####
####                 FUNCIÓN PARA CALCULAR
####                  LA MATRIZ DE HOMEOGRAFIA
####
###############################################################





def matriz_de_homeografia(coord_sup_izquierda,coord_sup_derecha,coord_inf_izquierda,coord_inf_derecha,img_patron,path_resultados,num_res,dim_resize):
    img_patron=cv2.resize(img_patron, dim_resize)
    #print(img_patron.shape)
    cols=distancia(coord_sup_izquierda,coord_sup_derecha)
    rows=distancia(coord_inf_izquierda,coord_sup_izquierda)
    #VALORES INICIALES DEL MAPEO EN UNA IMAGEN MUY GRANDE PARA SER ESCALADA POSTERIORMENTE
    bias_X=5000
    bias_Y=5000
    altura_IMG=10000
    ancho_IMG=10000
    pts1 = np.float32([coord_sup_izquierda,coord_sup_derecha,coord_inf_izquierda,coord_inf_derecha])
    pts2 = np.float32([[bias_X,bias_Y],[cols+bias_X,bias_Y],[bias_X,rows+bias_Y],[bias_X+cols,bias_Y+rows]])
    M = cv2.getPerspectiveTransform(pts2,pts1)
    transf_bird_eye = cv2.warpPerspective(img_patron,M,(ancho_IMG,altura_IMG),flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP+cv2.WARP_FILL_OUTLIERS, borderMode=cv2.BORDER_CONSTANT, borderValue = [0, 0, 0])
    #print(transf_bird_eye.shape)
    
    #cv2.imshow('BIRD EYE TRANSFORM_1',transf_bird_eye)
    #cv2.waitKey(0)
    #CÁLCULO DE LA UBICACIÓN DE LAS COORDENADAS LÍMITES SUPERIOR IZQUIERDA Y SUPERIOR DERECHA DE LA IMÁGEN ORIGINAL
    #EN LAS COORDENADAS DE LA IMÁGEN CON VISTA DE PÁJARO 
    limites_imagen=[]
    limites_imagen.append(coordenadas_en_vista_de_pajaro(M,0,0))
    limites_imagen.append(coordenadas_en_vista_de_pajaro(M,(img_patron.shape[1]-1),0))
    
    #BIAS EN Y PARA TRASLADAR LA IMAGEN A LA PARTE SUPERIOR  
    if limites_imagen[0][1]>limites_imagen[1][1]:
        bias_Y=bias_Y-limites_imagen[0][1]
    else:
        bias_Y=bias_Y-limites_imagen[1][1]
        
    #NUEVO CÁLCULO DE LA MATRIZ DE HOMEOGRAFÍA    
    pts1 = np.float32([coord_sup_izquierda,coord_sup_derecha,coord_inf_izquierda,coord_inf_derecha])
    pts2 = np.float32([[bias_X,bias_Y],[cols+bias_X,bias_Y],[bias_X,rows+bias_Y],[bias_X+cols,bias_Y+rows]])
    M = cv2.getPerspectiveTransform(pts2,pts1)
    transf_bird_eye = cv2.warpPerspective(img_patron,M,(ancho_IMG,altura_IMG),flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP+cv2.WARP_FILL_OUTLIERS, borderMode=cv2.BORDER_CONSTANT, borderValue = [0, 0, 0])
    
    
    #CÁLCULO DE LA UBICACIÓN DE LAS COORDENADAS LÍMITES INFERIOR IZQUIERDA E INFERIOR DERECHA DE LA IMÁGEN ORIGINAL
    #EN LAS COORDENADAS DE LA IMÁGEN CON VISTA DE PÁJARO 
    limites_imagen.append(coordenadas_en_vista_de_pajaro(M,0,(img_patron.shape[0]-1)))
    limites_imagen.append(coordenadas_en_vista_de_pajaro(M,(img_patron.shape[1]-1),(img_patron.shape[0]-1)))
    # RESVISA DESDE QUE PÍXELES HASTA QUE PIXELES SE ENCUENTRA LA IMÁGEN EN LA PARTE SUPERIOR (FILA 0)
    flag_10=0
    flag_11=0
    for i in range(transf_bird_eye.shape[1]):         
        i_dd=transf_bird_eye[0,i,1]
        d_ii=transf_bird_eye[0,(transf_bird_eye.shape[1]-1)-i,1]
        if i_dd!=0 and flag_10==0:
            coordenada_ini=i
            flag_10=1
        if d_ii!=0 and flag_11==0:
            coordenada_finn=(transf_bird_eye.shape[1]-1)-i
            flag_11=1
    
    #CÁCULO DEL BIAS EN X PARA TRASLADAR LA IMÁGEN HACIA LA IZQUIERDA 
    bias_X=bias_X-coordenada_ini
    #CÁLCULO DEL ANCHO TOTAL DE LA IMÁGEN
    ancho_IMG=coordenada_finn-coordenada_ini
    #CÁLCULO DEL ALTO TOTAL DE LA IMÁGEN
    if limites_imagen[2][1]<limites_imagen[3][1]:
        altura_IMG=limites_imagen[2][1]
    else:
        altura_IMG=limites_imagen[3][1]
    
    #NUEVO CÁLCULO DE LA MATRIZ DE HOMEOGRAFÍA DEFINITIVA
    pts1 = np.float32([coord_sup_izquierda,coord_sup_derecha,coord_inf_izquierda,coord_inf_derecha])
    pts2 = np.float32([[bias_X,bias_Y],[cols+bias_X,bias_Y],[bias_X,rows+bias_Y],[bias_X+cols,bias_Y+rows]])
    M = cv2.getPerspectiveTransform(pts2,pts1)
    transf_bird_eye = cv2.warpPerspective(img_patron,M,(ancho_IMG,altura_IMG),flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP+cv2.WARP_FILL_OUTLIERS, borderMode=cv2.BORDER_CONSTANT, borderValue = [0, 0, 0])
    #cv2.imshow('BIRD EYE TRANSFORM CON COMPENSACION',transf_bird_eye)
    #cv2.waitKey(0)
    
    filename=str(num_res)+'.jpg'
    cv2.imwrite(os.path.join(path_resultados,filename),transf_bird_eye)
    
    mostrarrrr=cv2.resize(transf_bird_eye  ,dim_resize)
    cv2.imshow('IMAGEN ORIGINAL',mostrarrrr)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return cols,rows,bias_X,bias_Y









###############################################################
####
####
####                 FUNCIÓN PARA COMPENSAR CON 
####                   ANGULOS DE PITCH Y ROLL
####
###############################################################


def compensa_por_movimiento(coord_sup_izquierda,coord_sup_derecha,coord_inf_izquierda,coord_inf_derecha,angulo_pitch,angulo_roll,path_imagenes,path_resultados,mtx,dist,num_res,dim_resize):
    img_patron = cv2.imread(path_imagenes)
    # cv2.imshow('IMAGEN ORIGINAL',img_patron)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    img_patron=undistorted_images(img_patron,mtx,dist)
    #cv2.imshow('IMAGEN ORIGINAL SIN DISTORSION POR CAMARA',img_patron)
    #cv2.waitKey(0)
    al,an=img_patron.shape[0],img_patron.shape[1]
    pi=math.pi
    pith=(-angulo_pitch*pi)/180
    roll=(-angulo_roll*pi)/180
    ##X
    Mx=np.array([[1,0,0],[0,math.cos(pith),-math.sin(pith)],[0,math.sin(pith),math.cos(pith)]])
    ##Y
    My=np.array([[math.cos(roll),0,math.sin(roll)],[0,1,0],[-math.sin(roll),0,math.cos(roll)]])
    
    fy,fx= mtx[1][1],mtx[0][0]
    
    
    bias_X=5000
    bias_Y=5000
    Krc=mtx
    Kvc=np.array([[fx,   0.        , bias_X],
           [  0.        , fy, bias_Y],
           [  0.        ,   0.        ,   1.        ]])
    
    Kvc_m1=np.linalg.inv(Kvc)
    M_comp=np.dot(Mx,My)
    
    Mr=np.dot(np.dot(Krc,M_comp),Kvc_m1)
    
    transf_bird_eye = cv2.warpPerspective(img_patron,Mr,(10000,10000),flags=cv2.INTER_LINEAR+cv2.WARP_INVERSE_MAP+cv2.WARP_FILL_OUTLIERS, borderMode=cv2.BORDER_CONSTANT, borderValue = [0, 0, 0])
    #cv2.imshow('BIRD EYE TRANSFORM_1',transf_bird_eye)
    #cv2.waitKey(0)
    
    
    #CÁLCULO DE LA UBICACIÓN DE LAS COORDENADAS LÍMITES SUPERIOR IZQUIERDA Y SUPERIOR DERECHA DE LA IMÁGEN ORIGINAL
    #EN LAS COORDENADAS DE LA IMÁGEN CON VISTA DE PÁJARO 
    limites_imagen=[]
    limites_imagen.append(coordenadas_en_vista_de_pajaro(Mr,0,0))
    limites_imagen.append(coordenadas_en_vista_de_pajaro(Mr,(img_patron.shape[1]-1),0))
    
    #BIAS EN Y PARA TRASLADAR LA IMAGEN A LA PARTE SUPERIOR  
    if limites_imagen[0][1]>limites_imagen[1][1]:
        bias_Y=bias_Y-limites_imagen[0][1]
    else:
        bias_Y=bias_Y-limites_imagen[1][1]
        
    #NUEVO CÁLCULO DE LA MATRIZ DE HOMEOGRAFÍA    
    
    Kvc=np.array([[fx,   0.        , bias_X],
           [  0.        , fy, bias_Y],
           [  0.        ,   0.        ,   1.        ]])
    
    Kvc_m1=np.linalg.inv(Kvc)
    
    Mr=np.dot(np.dot(Krc,M_comp),Kvc_m1)
    
    
    transf_bird_eye = cv2.warpPerspective(img_patron,Mr,(10000,10000),flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP+cv2.WARP_FILL_OUTLIERS, borderMode=cv2.BORDER_CONSTANT, borderValue = [0, 0, 0])
    #CÁLCULO DE LA UBICACIÓN DE LAS COORDENADAS LÍMITES INFERIOR IZQUIERDA E INFERIOR DERECHA DE LA IMÁGEN ORIGINAL
    #EN LAS COORDENADAS DE LA IMÁGEN CON VISTA DE PÁJARO 
    limites_imagen.append(coordenadas_en_vista_de_pajaro(Mr,0,(img_patron.shape[0]-1)))
    limites_imagen.append(coordenadas_en_vista_de_pajaro(Mr,(img_patron.shape[1]-1),(img_patron.shape[0]-1)))
    # RESVISA DESDE QUE PÍXELES HASTA QUE PIXELES SE ENCUENTRA LA IMÁGEN EN LA PARTE SUPERIOR (FILA 0)
    flag_10=0
    flag_11=0
    for i in range(transf_bird_eye.shape[1]):         
        i_dd=transf_bird_eye[0,i,1]
        d_ii=transf_bird_eye[0,(transf_bird_eye.shape[1]-1)-i,1]
        if i_dd!=0 and flag_10==0:
            coordenada_ini=i
            flag_10=1
        if d_ii!=0 and flag_11==0:
            coordenada_finn=(transf_bird_eye.shape[1]-1)-i
            flag_11=1
    
    #CÁCULO DEL BIAS EN X PARA TRASLADAR LA IMÁGEN HACIA LA IZQUIERDA 
    bias_X=bias_X-coordenada_ini
    #CÁLCULO DEL ANCHO TOTAL DE LA IMÁGEN
    ancho_IMG=coordenada_finn-coordenada_ini
    #CÁLCULO DEL ALTO TOTAL DE LA IMÁGEN
    if limites_imagen[2][1]<limites_imagen[3][1]:
        altura_IMG=limites_imagen[2][1]
    else:
        altura_IMG=limites_imagen[3][1]
    
    #NUEVO CÁLCULO DE LA MATRIZ DE HOMEOGRAFÍA DEFINITIVA
    
    
    #NUEVO CÁLCULO DE LA MATRIZ DE HOMEOGRAFÍA    
    
    Kvc=np.array([[fx,   0.        , bias_X],
           [  0.        , fy, bias_Y],
           [  0.        ,   0.        ,   1.  ]])
    
    Kvc_m1=np.linalg.inv(Kvc)
    Mr=np.dot(np.dot(Krc,M_comp),Kvc_m1)
    
    
    transf_bird_eye = cv2.warpPerspective(img_patron,Mr,(ancho_IMG,altura_IMG),flags=cv2.INTER_LINEAR + cv2.WARP_INVERSE_MAP+cv2.WARP_FILL_OUTLIERS, borderMode=cv2.BORDER_CONSTANT, borderValue = [0, 0, 0])
    transf_bird_eye=cv2.resize(transf_bird_eye  , (an , al))
    cols,rows,bias_XX,bias_YY=matriz_de_homeografia(coord_sup_izquierda,coord_sup_derecha,coord_inf_izquierda,coord_inf_derecha,transf_bird_eye,path_resultados,num_res,dim_resize)
    
    
    vertical_d=distancia([bias_XX,bias_YY],[bias_XX,rows+bias_YY])
    horizontal_d=distancia([bias_XX,bias_YY],[cols+bias_XX,bias_YY])
    factor_de_conv_lineal_Vertical=51/vertical_d
    factor_de_conv_lineal_Horizontal=27/horizontal_d
    
    area_en_pixeles=vertical_d*horizontal_d
    factor_de_conv_area=1377/area_en_pixeles
    return factor_de_conv_lineal_Vertical,factor_de_conv_lineal_Horizontal,factor_de_conv_area


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

def deteccion_esquinas(path_imagenes,mtx,dist,scale_percent=38):
    img_patron = cv2.imread(path_imagenes+'/tablero_esquinas.JPG')
    #cv2.imshow('IMAGEN ORIGINAL',img_patron)
    #cv2.waitKey(0)
    img_patron=undistorted_images(img_patron,mtx,dist)
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
    
    # coord_sup_izquierda=np.array([int(refpnt[0][0]*(width_original/width)),int(refpnt[0][1]*(height_original/height))])
    # coord_sup_derecha=np.array([int(refpnt[1][0]*(width_original/width)),int(refpnt[1][1]*(height_original/height))])
    # coord_inf_izquierda=np.array([int(refpnt[2][0]*(width_original/width)),int(refpnt[2][1]*(height_original/height))])
    # coord_inf_derecha=np.array([int(refpnt[3][0]*(width_original/width)),int(refpnt[3][1]*(height_original/height))])
    
    coord_sup_izquierda=np.array([int(refpnt[0][0]),int(refpnt[0][1])])
    coord_sup_derecha=np.array([int(refpnt[1][0]),int(refpnt[1][1])])
    coord_inf_izquierda=np.array([int(refpnt[2][0]),int(refpnt[2][1])])
    coord_inf_derecha=np.array([int(refpnt[3][0]),int(refpnt[3][1])])
    return coord_sup_izquierda,coord_sup_derecha,coord_inf_derecha,coord_inf_izquierda,img_patron,dim

###############################################################
####
####
####                 CALIBRACIÓN DE LA CÁMARA
####
####
###############################################################


def calibra_camara(tam_cuadros,path_imagenes,path):
    # criterio de terminación
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, tam_cuadros, 0.001)
    #Dieferencias en el patron de calibración
    if imagenes_a_x_grados==51:
        puntos_verticales=7
        puntos_horizontales=8
    else:
        puntos_verticales=5
        puntos_horizontales=8
    # preparar puntos de objeto, como (0,0,0,0), (1,0,0,0), (2,0,0,0)...., (6,5,0)
    objp = np.zeros((puntos_horizontales*puntos_verticales,3), np.float32)
    objp[:,:2] = np.mgrid[0:puntos_horizontales,0:puntos_verticales].T.reshape(-1,2)
    # Arrays para almacenar puntos de objeto y puntos de imagen de todas las imágenes.
    objpoints = [] # PUNTOS 3D DEL MUNDO 
    imgpoints = [] # PUNTOS 2D EN EL PLANO DE LA IMAGEN 
    images = glob.glob(path_imagenes+'/calibra/*.JPG')
    i=0
    for fname in images:
      img = cv2.imread(fname)
      gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
      # Encuentra las esquinas del tablero de ajedrez
      ret, corners = cv2.findChessboardCorners(gray, (puntos_horizontales,puntos_verticales),None)
      if ret == True:
        objpoints.append(objp)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        imgpoints.append(corners2)
        # Dibuja y muestra las esquinas
        img = cv2.drawChessboardCorners(img, (puntos_horizontales,puntos_verticales), corners2,ret)
        #cv2.imshow('img',img)
        #cv2.waitKey(50)
        filename='tablero_de_calibracion_esquinas'+str(i)+'.png'
        cv2.imwrite(os.path.join(path,filename),img)
        i=i+1
      else:
          print('NO es buena la imagen'+ fname)
    #cv2.destroyAllWindows()
    
    #PARAMETROS INTRÍNSECOS Y EXTRÍNSECOS DE LA CÁMARA
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)
    
    i=0
    for fname in images:
        img = cv2.imread(fname)
        dst = undistorted_images(img,mtx,dist)
        
        #cv2.imshow("undistorted", dst),cv2.waitKey(50)
        filename='tablero_de_calib_sin_distorsion_por_camara'+str(i)+'.png'
        cv2.imwrite(os.path.join(path,filename),dst)
        i=i+1
    #cv2.destroyAllWindows() 
    
    #CÁLCULO DEL ERROR DE REPROYECCIÓN
    tot_error = 0 
    for i in range(len(objpoints)): 
      imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist) 
      error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2) 
      tot_error += error 
    print( "Error de reproyección total: ", tot_error, 'píxeles') 
    return mtx,dist

def save_obj(obj, name ):
    with open('factores_de_conversion/'+ name + '.pkl', 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)



imagenes_a_x_grados=66
path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/'+str(imagenes_a_x_grados)+'_grados'
path='resultados_'+str(imagenes_a_x_grados)
path_resultados='RESULTADOS_COMPENSADOS_66'

try:
    os.mkdir('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/'+path) 
    os.mkdir('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/'+path_resultados) 
    os.mkdir('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/factores_de_conversion') 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
        
tam_cuadros=17
tmstmp1 = time.time()
mtx,dist=calibra_camara(tam_cuadros,path_imagenes,path)
###############################################################
####
####
####                 DETECCIÓN DE ESQUINAS
####
####
###############################################################
scale_percent=38
coord_sup_izquierda,coord_sup_derecha,coord_inf_derecha,coord_inf_izquierda,img_patron,dim_resize=deteccion_esquinas(path_imagenes,mtx,dist,scale_percent)
###############################################################
####
####
####           OBTENCIÓN DE LA MATRIZ DE HOMEOGRAFÍA
####
####
###############################################################



imagenes_a_x_grados=66
path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/'+str(imagenes_a_x_grados)+'_grados'

#
#
angulo_pitch=0
angulo_roll=0
num_res=1
#
#
#
path_del_tablero='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/66_grados/tablero_esquinas.JPG'
factor_de_conv_lineal_Vertical,factor_de_conv_lineal_Horizontal,factor_de_conv_area=compensa_por_movimiento(coord_sup_izquierda,coord_sup_derecha,coord_inf_izquierda,coord_inf_derecha,angulo_pitch,angulo_roll,path_del_tablero,path_resultados,mtx,dist,66661,dim_resize)


save_obj(factor_de_conv_lineal_Vertical,'factor_conv_lineal_vertical')
save_obj(factor_de_conv_lineal_Horizontal,'factor_conv_lineal_horizontal')
save_obj(factor_de_conv_area,'factor_conv_area')


imagenes_de_prueba=glob.glob(path_imagenes+'/*.JPG')
i=0
for finame in imagenes_de_prueba:   
    compensa_por_movimiento(coord_sup_izquierda,coord_sup_derecha,coord_inf_izquierda,coord_inf_derecha,angulo_pitch,angulo_roll,finame,path_resultados,mtx,dist,i)
    i=i+1


tmstmp2 = time.time()
print('Total time elapsed = ', tmstmp2 - tmstmp1)