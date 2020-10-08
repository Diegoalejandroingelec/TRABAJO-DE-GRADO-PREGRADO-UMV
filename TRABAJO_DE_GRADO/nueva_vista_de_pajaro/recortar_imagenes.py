import cv2
import glob
import os
import errno

def crea_carpeta(path_carpeta):
    try:
        os.mkdir(path_carpeta)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
def recorte_imagenes(path_imagenes,path_carpeta_img_crop,rec_sup=0):
    imagenes_de_prueba=glob.glob(path_imagenes+'/*.JPG')
    rec_sup=700
    for finames in imagenes_de_prueba:
        img=cv2.imread(finames)
        img=img[rec_sup:img.shape[0],:]
        
        filename=finames.split("/")[len(finames.split("/"))-1]
        cv2.imwrite(os.path.join(path_carpeta_img_crop,filename),img)
        
imagenes_a_x_grados=66
path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/'+str(imagenes_a_x_grados)+'_grados'
path_carpeta_img_crop='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/nueva_vista_de_pajaro/'+str(imagenes_a_x_grados)+'_grados'+'/imagenes_recortadas'
crea_carpeta(path_carpeta_img_crop)

recorte_imagenes(path_imagenes,path_carpeta_img_crop,rec_sup=700)