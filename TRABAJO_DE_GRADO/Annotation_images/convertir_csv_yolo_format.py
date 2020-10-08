import cv2
import os
import pandas as pd
import glob
import errno
import numpy as np
def funcion1(vott_df,labeldict):
    # Encode labels according to labeldict if code's don't exist
    if not "code" in vott_df.columns:
        vott_df["code"] = vott_df["label"].apply(lambda x: labeldict[x])
    # Round float to ints
    for col in vott_df[["xmin", "ymin", "xmax", "ymax"]]:
        vott_df[col] = (vott_df[col]).apply(lambda x: round(x))
def crea_carpeta(path_carpeta):
    try:
        os.mkdir(path_carpeta)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise
            
def csv_to_yolo_format(VoTT_csv,image_path,Folder_labels,path_clases_file,Folder_para_direccion_de_imagenes_train,Folder_para_direccion_de_imagenes_test,porcentaje_de_cada_clase):
    multi_df = pd.read_csv(VoTT_csv)
    labels = multi_df["label"].unique()
    labeldict = dict(zip(labels, range(len(labels))))
    print('Las clases son: ')
    for clave, valor in labeldict.items():
        print('Clase '+str(valor)+' '+ clave)
    
    funcion1(multi_df, labeldict)
    nombre_de_la_imagen_anterior=''
    for index, row in multi_df.iterrows():
        nombre_de_la_imagen=(row[["image"]].tolist())
        info=(row[["code","xmin", "ymin", "xmax", "ymax"]].tolist())
        X=(info[3]-info[1])/2+info[1]
        Y=(info[4]-info[2])/2+info[2]
        H_im=info[4]-info[2]
        W_im=info[3]-info[1]
        if nombre_de_la_imagen != nombre_de_la_imagen_anterior:
            img = cv2.imread(image_path+nombre_de_la_imagen[0])
            height, width= img.shape[0],img.shape[1]             
        X_relat=X/width
        Y_relat=Y/height
        H_im_relat=H_im/height
        W_im_relat=W_im/width
        texto=str(info[0])+' '+str(X_relat)+' '+str(Y_relat)+' '+str(W_im_relat)+' '+str(H_im_relat)+os.linesep   
        file = open(Folder_labels+'/'+str(nombre_de_la_imagen[0][0:len(nombre_de_la_imagen[0])-4])+'.txt', "a")
        file.write(texto)
        file.close()
        nombre_de_la_imagen_anterior=nombre_de_la_imagen
    for clases in labels:
        file = open(path_clases_file+'/clases.names','a')
        file.write(clases+os.linesep )
        file.close()
        
        
    #CUENTA CUANTOS PATRONES HAY DE CADA CLASE    
    clases_=np.zeros(len(labels))
    for index, row in multi_df.iterrows():
        codigo_clase=(row[["code"]].tolist())
        clases_[codigo_clase[0]]+=1

            
    #ESTABLECE EL PORCENTAJE DE PATRONES PARA TRAIN        
    porcentaje_clase_=porcentaje_de_cada_clase
    num_train_clases_=[]
    for n in range(len(labels)):
        num_train_clases_.append(int(clases_[n]*porcentaje_clase_[n]))
        
    #num_train_clases_=[int(clases_[0]*porcentaje_clase_0),int(clases_[1]*porcentaje_clase_1),int(clases_[2]*porcentaje_clase_2)]

    
    
    #INICIALIZA CONTADORES PARA SABER CUANTOS PATRONES VAN DE CADA CLASE PARA EL SET DE TRAIN
    nombre_de_la_imagen_anterior=''
    clases_for_train=np.zeros(len(labels))
    #INICIALIZA BANDERAS PARA CADA CLASE PARA SABER SI SE DEBEN GUARDAR MAS PATRONES DE DICHA CLASE 
    prohibido_clases_=[False]*len(labels)

    #BANDERA PARA SABER SI GUARDAR O NO 
    no_guardar=False
    #LISTA PARA AGREGAR EL NOMBRE DE LA IMÁGENES DE TRAIN
    imagenes_to_train=[]
    #CICLO PARA DEFINIR QUE IMAGENES VAN AL SET DE TRAIN
    for index, row in multi_df.iterrows():  
        codigo_clase=(row[["code"]].tolist())
        nombre_de_la_imagen=(row[["image"]].tolist())
        
        if nombre_de_la_imagen != nombre_de_la_imagen_anterior:
            if no_guardar==False and nombre_de_la_imagen_anterior!='':
                imagenes_to_train.append(multi_df['image'][index-1])
            nombre_de_la_imagen_anterior=nombre_de_la_imagen
            no_guardar=False
        #SI LA BANDERA DE GUARDADO ESTA EN FALSE AUMNETA EL CONTADOR DE LA CLASE
        #SIEMPRE QUE NO HAYA REVASADO EL NUMERO DEFINIDO DE PATRONES POR CLASE            
        if no_guardar==False:             
            if clases_for_train[codigo_clase[0]]<num_train_clases_[codigo_clase[0]]:
                clases_for_train[codigo_clase[0]]+=1
        
        #SI EL NUMERO DE PATRONES POR CLASE ES MAYOR O IGUAL AL LIMITE DEFINIDO
        #PROHIBE GUARDAR LA CLASE QUE HA REVASADO DICHO LIMITE
        if clases_for_train[codigo_clase[0]]>=num_train_clases_[codigo_clase[0]]:
            prohibido_clases_[codigo_clase[0]]=True
       
        
        
        #SI LA CLASE ESTÁ PROHIBIDA Y LA CLASE DEL RECUADRO COINCIDE CON LA CLASE PROHIBIDA, ACTIVA LA BANDERA
        #QUE EVITA QUE LA IMAGEN SE GUARDE EN LA LISTA DE IMAGENES PARA TRAIN
        if prohibido_clases_[codigo_clase[0]]:
            no_guardar=True
            #print('SE ACTIVÓ UN NO GUARGAR CON LA IMAGEN', nombre_de_la_imagen[0],'CON CLASE 0 PROHIBIDA')
       
    
    
    
    
    #ESCRIBE Y GUARDA UN ARCHIVO DE TEXTO CON TODAS LAS IMAGENES DE TRAIN
    images_text=[]
    for n in imagenes_to_train:
        images_text.append(image_path+n)
        
    for fnames in images_text:
        file = open(Folder_para_direccion_de_imagenes_train,'a')
        file.write(fnames+os.linesep )
        file.close()
    #IDENTIFICA QUE IMAGENES NO ESTAN EN LA LISTA DE TRAIN Y LAS UBICA EN LA LISTA DE TEST    
    imagenes_to_test=[]
    for x in range(len(multi_df['image'])):
        imagenes_to_test_disponible=True
        for n in imagenes_to_train:
            if multi_df['image'][x]==n:
                imagenes_to_test_disponible=False        
        if imagenes_to_test_disponible:
            imagenes_to_test.append(multi_df['image'][x])
    #ELIMINA LAS IMAGENES REPETIDAS DE LA LISTA DE IMAGENES DE TEST        
    imagenes_to_test=list(set(imagenes_to_test))
    #ESCRIBE Y GUARDA UN ARCHIVO DE TEXTO CON TODAS LAS IMAGENES DE TEST
    images_text_1=[]
    for n in imagenes_to_test:
        images_text_1.append(image_path+n)
        
    for fnames in images_text_1:
        file = open(Folder_para_direccion_de_imagenes_test,'a')
        file.write(fnames+os.linesep )
        file.close()
    
    #
    codigos_train=[]
    codigos_test=[]
    for index, row in multi_df.iterrows():  
        codigo_clase=(row[["code"]].tolist())
        nombre_de_la_imagen=(row[["image"]].tolist())
        
        if nombre_de_la_imagen[0] in imagenes_to_test:
            codigos_test.append(codigo_clase[0])
            
        if nombre_de_la_imagen[0] in imagenes_to_train:
            codigos_train.append(codigo_clase[0])   
                
    #CUENTA CUANTOS PATRONES HAY EN CADA CLASE PARA EL DATASET DE TEST
    c_=np.zeros(len(labels))
    for n in codigos_test:
        c_[n]+=1
        
    
    #AGRUPA TODAS LAS IMAGENES CON CLASES DE INTERES EN UNA LISTA
    imagenes_con_clases_de_interes=imagenes_to_train+imagenes_to_test
    #AGRUPA TODAS LAS IMAGENES DE LA CARPETA INDEPENDIENTEMENTE SI 
    #TIENEN CLASES DE INTERES O NO
    todas_las_images_en_la_carpeta = glob.glob(image_path+'*.jpg')
    aux=[]
    for fnames in todas_las_images_en_la_carpeta:
        aux.append(fnames.split('/')[-1])
    #QUITA EL PATH DE LAS IMAGENES Y SOLO DEJA EL NOMBRE    
    todas_las_images_en_la_carpeta=aux
    
    #IDENTIFICA QUE IMAGENES NO TIENEN CLASE DE INTERES
    imagenes_sin_clases_de_interes=[]
    for n in todas_las_images_en_la_carpeta:
       if not(n in imagenes_con_clases_de_interes):
           imagenes_sin_clases_de_interes.append(n)

    #CREA ARCHIVOS DE TEXTO VACIOS PARA CADA IMAGEN SIN CLASE DE INTERES        
    for n in imagenes_sin_clases_de_interes:
        file = open(Folder_labels+'/'+n[0:len(n)-4]+'.txt','a')
        file.close()
        
    #DEFINE EL NUMERO DE IMAGENES SIN CLASES DE INTERES PARA TRAIN   
    porcentaje_de_imagenes_sin_clases_de_interes_para_train=0.8
    num_clases_de_interes_para_train=int(porcentaje_de_imagenes_sin_clases_de_interes_para_train*len(imagenes_sin_clases_de_interes))
    
    #DEFINE EL CONTADOR DE IMAGENES PARA TRAIN Y PARA TEST
    con_train=0
    con_test=0
    imagenes_sin_clases_de_interes_to_train=[]
    imagenes_sin_clases_de_interes_to_test=[]
    for n in imagenes_sin_clases_de_interes:
        if con_train<num_clases_de_interes_para_train:
            imagenes_sin_clases_de_interes_to_train.append(image_path+n)
            con_train+=1
        else:
            imagenes_sin_clases_de_interes_to_test.append(image_path+n)
            con_test+=1 
    
    for n in imagenes_sin_clases_de_interes_to_test:
        file = open(Folder_para_direccion_de_imagenes_test,'a')
        file.write(n+os.linesep )
        file.close()
    for n in imagenes_sin_clases_de_interes_to_train:
        file = open(Folder_para_direccion_de_imagenes_train,'a')
        file.write(n+os.linesep )
        file.close()
        
    print('Hay '+str(len(imagenes_to_train)+con_train)+' imagenes para Train')
    print('Hay '+str(len(imagenes_to_test)+con_test)+' imagenes para Test')
    print('El total de imagenes es '+str(len(imagenes_to_test)+len(imagenes_to_train)+con_test+con_train))
    print('')
    print('')
    for n in range(len(labels)):
        print('El total de patrones de la clase '+labels[n]+' es: '+ str(clases_[n]))
    print('El total de imagenes sin clases de interes (sin label) es: '+ str(len(imagenes_sin_clases_de_interes)))
    print('')
    print('')
    for n in range(len(labels)):
        print('Hay '+str(c_[n])+' patrones en la clase '+labels[n]+' para test es decir un '+str("{:.2f}".format((c_[n]*100)/clases_[n]))+'%')
    if len(imagenes_sin_clases_de_interes) >0:
        print('Hay '+str(con_test)+' imagenes sin label para test es decir un '+str("{:.2f}".format((con_test*100)/len(imagenes_sin_clases_de_interes)))+'%') 
    c_t=np.zeros(len(labels))
    for n in codigos_train:
        c_t[n]+=1
    print('')
    print('')
    for n in range(len(labels)):
        print('Hay '+str(c_t[n])+' patrones en la clase '+labels[n]+' para train es decir un '+str("{:.2f}".format((c_t[n]*100)/clases_[n]))+'%')
    if len(imagenes_sin_clases_de_interes) >0:
        print('Hay '+str(con_train)+' imagenes sin label para train es decir un '+str("{:.2f}".format((con_train*100)/len(imagenes_sin_clases_de_interes)))+'%') 

            
            
#PATH DONDE SE VAN A GUARDAR LOS LABELS Y EL ARCHIVO CON LOS NOMBRES DE LAS CLASES        
Folder_labels='/data/estudiantes/umv/DATOS_PARA_YOLO/info_dataset_2/labels'
path_clases_file='/data/estudiantes/umv/DATOS_PARA_YOLO/clases'

#PATH DONDE SE VAN A GUARDAR ARCHIVOS DE TEXTO CON LOS PATH DE LA IMAGENES PARA TRAIN Y PARA TEST
Folder_para_direccion_de_imagenes_train='/data/estudiantes/umv/DATOS_PARA_YOLO/train.txt'
Folder_para_direccion_de_imagenes_test='/data/estudiantes/umv/DATOS_PARA_YOLO/test.txt'

#PATH DE LA UBICACIÓN DEL ARCHIVO CSV DE LAS ETIQUETAS Y PATH DE LAS IMÁGENES 
VoTT_csv = '/data/estudiantes/umv/DATOS_PARA_YOLO/info_dataset_2/JPEGImages/archivo_fusionado.csv'
image_path='/data/estudiantes/umv/DATOS_PARA_YOLO/info_dataset_2/JPEGImages/'



crea_carpeta(path_clases_file)
crea_carpeta(Folder_labels)

porcentaje_de_cada_clase=[0.80]
csv_to_yolo_format(VoTT_csv,image_path,Folder_labels,path_clases_file,Folder_para_direccion_de_imagenes_train,Folder_para_direccion_de_imagenes_test,porcentaje_de_cada_clase) 

    
