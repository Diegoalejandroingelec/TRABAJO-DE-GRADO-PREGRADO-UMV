
import cv2
import pickle
import os
import errno

def load_obj(name ):
    with open( name, 'rb') as f:
        return pickle.load(f)
detection_images= load_obj('/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/darknet/detect_images_info/informacion_imagenes.pkl')
path_imagenes_boundingbox='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Recuadros_contenedores/resultados_con_recuadros'
path_imagenes='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/IMAGENES_ETIQUETADAS/vott-csv-export/'
try:
    os.mkdir(path_imagenes_boundingbox) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
color_0 = (255,0,0)
for imagen_info in detection_images:
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
            cv2.rectangle(img,sup_izq,inf_der, color_0, 3)
            clase=imagen_info['detections'][detection_number][0]
            proba=imagen_info['detections'][detection_number][1]
            cv2.putText(img,clase+' '+str("{:.2f}".format(proba*100))+'%', sup_izq_titulo, cv2.FONT_HERSHEY_SIMPLEX, 1, color_0, 2)
        
        img_g=cv2.resize(img,(1000,700))
        cv2.imwrite(os.path.join(path_imagenes_boundingbox,imagen_info['image_name'].split("/")[-1]),img_g)
        
    if not imagen_info['detections']:    
        img=cv2.imread(imagen_info['image_name'])
        img_g=cv2.resize(img,(1000,700))
        cv2.imwrite(os.path.join(path_imagenes_boundingbox,imagen_info['image_name'].split("/")[-1]),img_g)
        
