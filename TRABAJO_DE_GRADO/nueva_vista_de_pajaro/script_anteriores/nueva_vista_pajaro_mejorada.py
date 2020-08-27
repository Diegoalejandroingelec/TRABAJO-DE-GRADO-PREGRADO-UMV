import numpy as np
import cv2
import glob
import os
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


   
imagenes_a_x_grados=40
path_imagenes='C:/Users/diego/Desktop/todas las carpetas del escritorio/DIEGO ALEJANDRO/NOVENO SEMESTRE/Procesamiento_de_imagenes/Proyecto/nueva_vista_de_pajaro/'+str(imagenes_a_x_grados)+'_grados'
path='resultados_'+str(imagenes_a_x_grados)
###############################################################
####
####
####                 CALIBRACIÓN DE LA CÁMARA
####
####
###############################################################
# criterio de terminación
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 41, 0.001)
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
    cv2.imshow('img',img)
    cv2.waitKey(50)
    filename='tablero_de_calibracion_esquinas'+str(i)+'.png'
    cv2.imwrite(os.path.join(path,filename),img)
    i=i+1
  else:
      print('NO es buena la imagen'+ fname)
cv2.destroyAllWindows()

#PARAMETROS INTRÍNSECOS Y EXTRÍNSECOS DE LA CÁMARA
ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1],None,None)

i=0
for fname in images:
    img = cv2.imread(fname)
    dst = undistorted_images(img,mtx,dist)
    
    cv2.imshow("undistorted", dst),cv2.waitKey(50)
    filename='tablero_de_calib_sin_distorsion_por_camara'+str(i)+'.png'
    cv2.imwrite(os.path.join(path,filename),dst)
    i=i+1
cv2.destroyAllWindows() 

#CÁLCULO DEL ERROR DE REPROYECCIÓN
tot_error = 0 
for i in range(len(objpoints)): 
  imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist) 
  error = cv2.norm(imgpoints[i],imgpoints2, cv2.NORM_L2)/len(imgpoints2) 
  tot_error += error 
print( "Error de reproyección total: ", tot_error, 'píxeles') 

###############################################################
####
####
####                 DETECCIÓN DE ESQUINAS
####
####
###############################################################
img_patron = cv2.imread(path_imagenes+'/tablero_esquinas.JPG')
cv2.imshow('IMAGEN ORIGINAL',img_patron)
cv2.waitKey(0)
img_patron=undistorted_images(img_patron,mtx,dist)
cv2.imshow('IMAGEN ORIGINAL SIN DISTORSION POR CAMARA',img_patron)
cv2.waitKey(0)

gray_image = cv2.cvtColor(img_patron,cv2.COLOR_BGR2GRAY)
if imagenes_a_x_grados==40:
    bilateral_F = cv2.bilateralFilter(gray_image, 9, 70, 70)
else:
    bilateral_F = cv2.bilateralFilter(gray_image, 9, 100, 100)
    
        
cv2.imshow('IMAGEN EN ESCALA DE GRISES',gray_image)
cv2.imshow('IMAGEN FILTRADA (BILATERAL FILTER)',bilateral_F)
cv2.waitKey(0)

if imagenes_a_x_grados==40:
    esquinas = cv2.cornerHarris(bilateral_F, 4, 1, 0.23)
else:
    esquinas = cv2.cornerHarris(bilateral_F, 4, 1, 0.233)

ret, esquinas = cv2.threshold(esquinas,0.09*esquinas.max(),255,0)
esquinas = np.uint8(esquinas)

cv2.imshow('Esquinas Segmentadas', esquinas)
cv2.waitKey(0)
ret, labels, stats, centroides = cv2.connectedComponentsWithStats(esquinas)
criterio_n = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 2, 0.1)
esquinas_1 = cv2.cornerSubPix(bilateral_F,np.float32(centroides),(5,5),(-1,-1),criterio_n)
esquinas_1=esquinas_1[1:len(esquinas_1),:]

if imagenes_a_x_grados==40:
    coord_sup_izquierda=esquinas_1[0].astype(int)
    coord_sup_derecha=esquinas_1[1].astype(int)
    coord_inf_derecha=esquinas_1[3].astype(int)
    coord_inf_izquierda=esquinas_1[2].astype(int)
else:
    coord_sup_izquierda=esquinas_1[0].astype(int)
    coord_sup_derecha=esquinas_1[1].astype(int)
    coord_inf_derecha=esquinas_1[2].astype(int)
    coord_inf_izquierda=esquinas_1[3].astype(int)
###############################################################
####
####
####           OBTENCIÓN DE LA MATRIZ DE HOMEOGRAFÍA
####
####
###############################################################
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
cv2.imshow('BIRD EYE TRANSFORM_1',transf_bird_eye)
cv2.waitKey(0)
###############################################################
####
####
####                 OBTENCIÓN DE FACTORES DE CONVERCIÓN 
####
####51X27
###############################################################

vertical_d=distancia([bias_X,bias_Y],[bias_X,rows+bias_Y])
horizontal_d=distancia([bias_X,bias_Y],[cols+bias_X,bias_Y])

factor_de_conv_lineal_0=51/vertical_d
factor_de_conv_lineal_1=27/horizontal_d

factor_de_conv_lineal=(factor_de_conv_lineal_0+factor_de_conv_lineal_1)/2

area_en_pixeles=vertical_d*horizontal_d
factor_de_conv=1377/area_en_pixeles
###############################################################
####
####
####  TRANSFORMACIÓN DE PERSPECTIVA DE LAS IMÁGENES DE PRUEBA 
####
####
###############################################################
imagenes_de_prueba=glob.glob(path_imagenes+'/*.JPG')
i=0
for finame in imagenes_de_prueba:
    img_prueba = cv2.imread(finame)
    img_prueba=undistorted_images(img_prueba,mtx,dist)
    transf_bird_eye_2 = cv2.warpPerspective(img_prueba,M,(ancho_IMG,altura_IMG),flags=cv2.INTER_LINEAR+ cv2.WARP_INVERSE_MAP +cv2.WARP_FILL_OUTLIERS, borderMode=cv2.BORDER_CONSTANT, borderValue = [0, 0, 0])
    filename='imagen_'+str(i)+'.png'
    cv2.imwrite(os.path.join(path,filename),transf_bird_eye_2)
    i=i+1
