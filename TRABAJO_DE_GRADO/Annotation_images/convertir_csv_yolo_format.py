import cv2
import os
import pandas as pd
import glob
import errno
def funcion1(vott_df,labeldict):
    # Encode labels according to labeldict if code's don't exist
    if not "code" in vott_df.columns:
        vott_df["code"] = vott_df["label"].apply(lambda x: labeldict[x])
    # Round float to ints
    for col in vott_df[["xmin", "ymin", "xmax", "ymax"]]:
        vott_df[col] = (vott_df[col]).apply(lambda x: round(x))
        
def csv_to_yolo_format(VoTT_csv,image_path,Folder_labels,path_clases_file,Folder_para_direccion_de_imagenes_train,Folder_para_direccion_de_imagenes_test):
    multi_df = pd.read_csv(VoTT_csv)
    labels = multi_df["label"].unique()
    labeldict = dict(zip(labels, range(len(labels))))
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
        file = open(Folder_labels+'/'+str(nombre_de_la_imagen[0].strip('.jpg'))+'.txt', "a")
        file.write(texto)
        file.close()
        nombre_de_la_imagen_anterior=nombre_de_la_imagen
    for clases in labels:
        file = open(path_clases_file+'/clases.names','a')
        file.write(clases+os.linesep )
        file.close()
        
        
        
    clase_0=0
    clase_1=0
    clase_2=0
    for index, row in multi_df.iterrows():
        codigo_clase=(row[["code"]].tolist())
        if codigo_clase[0]==0:
            clase_0=clase_0+1
        if codigo_clase[0]==1:
            clase_1=clase_1+1
        if codigo_clase[0]==2:
            clase_2=clase_2+1
            
            
    porcentaje_clase_0=0.9
    porcentaje_clase_1=0.85
    porcentaje_clase_2=0.85
    num_train_clase_0=int(clase_0*porcentaje_clase_0)
    num_train_clase_1=int(clase_1*porcentaje_clase_1)
    num_train_clase_2=int(clase_2*porcentaje_clase_2)
    nombre_de_la_imagen_anterior=''
    clase_0_for_train=0
    clase_1_for_train=0
    clase_2_for_train=0
    
    prohibido_clase_0=False
    prohibido_clase_1=False
    prohibido_clase_2=False
    no_guardar=False
    imagenes_to_train=[]
    
    for index, row in multi_df.iterrows():  
        codigo_clase=(row[["code"]].tolist())
        nombre_de_la_imagen=(row[["image"]].tolist())
        
        if nombre_de_la_imagen != nombre_de_la_imagen_anterior:
            if no_guardar==False and nombre_de_la_imagen_anterior!='':
                imagenes_to_train.append(multi_df['image'][index-1])
            nombre_de_la_imagen_anterior=nombre_de_la_imagen
            no_guardar=False
            
        if no_guardar==False: 
            if codigo_clase[0]==0 and clase_0_for_train<num_train_clase_0:
                clase_0_for_train=clase_0_for_train+1
                #print(nombre_de_la_imagen[0])
            if codigo_clase[0]==1 and clase_1_for_train<num_train_clase_1:  
                clase_1_for_train=clase_1_for_train+1
                #print(nombre_de_la_imagen[0])
            if codigo_clase[0]==2 and clase_2_for_train<num_train_clase_2:
                clase_2_for_train=clase_2_for_train+1
                #print(nombre_de_la_imagen[0])
        
        
        
        if clase_0_for_train>=num_train_clase_0:
            prohibido_clase_0=True
        if clase_1_for_train>=num_train_clase_1:
            prohibido_clase_1=True
        if clase_2_for_train>=num_train_clase_2:
            prohibido_clase_2=True
             
        if prohibido_clase_0 and codigo_clase[0]==0:
            no_guardar=True
            #print('SE ACTIVÓ UN NO GUARGAR CON LA IMAGEN', nombre_de_la_imagen[0],'CON CLASE 0 PROHIBIDA')
        if prohibido_clase_1 and codigo_clase[0]==1:
            no_guardar=True
            #print('SE ACTIVÓ UN NO GUARGAR CON LA IMAGEN', nombre_de_la_imagen[0],'CON CLASE 1 PROHIBIDA')
        if prohibido_clase_2 and codigo_clase[0]==2:
            no_guardar=True
            #print('SE ACTIVÓ UN NO GUARGAR CON LA IMAGEN', nombre_de_la_imagen[0],'CON CLASE 2 PROHIBIDA')
    
    images_text=[]
    for n in imagenes_to_train:
        images_text.append(image_path+n)
        
    for fnames in images_text:
        file = open(Folder_para_direccion_de_imagenes_train,'a')
        file.write(fnames+os.linesep )
        file.close()
        
    imagenes_to_test=[]
    for x in range(len(multi_df['image'])):
        imagenes_to_test_disponible=True
        for n in imagenes_to_train:
            if multi_df['image'][x]==n:
                imagenes_to_test_disponible=False        
        if imagenes_to_test_disponible:
            imagenes_to_test.append(multi_df['image'][x])
            
    imagenes_to_test=list(set(imagenes_to_test))
    
    images_text_1=[]
    for n in imagenes_to_test:
        images_text_1.append(image_path+n)
        
    for fnames in images_text_1:
        file = open(Folder_para_direccion_de_imagenes_test,'a')
        file.write(fnames+os.linesep )
        file.close()
    
    codigos_train=[]
    codigos_test=[]
    for index, row in multi_df.iterrows():  
        codigo_clase=(row[["code"]].tolist())
        nombre_de_la_imagen=(row[["image"]].tolist())
        
        for n in imagenes_to_test:
            if nombre_de_la_imagen[0]==n:
                codigos_test.append(codigo_clase[0])
        
        for n in imagenes_to_train:
            if nombre_de_la_imagen[0]==n:
                codigos_train.append(codigo_clase[0])
                

    c_0=0
    c_1=0
    c_2=0
    for n in codigos_test:
        if n==0:
            c_0+=1
        if n==1:
            c_1+=1
        if n==2:
            c_2+=1
    
    
    imagenes_con_clases_de_interes=imagenes_to_train+imagenes_to_test
    todas_las_images_en_la_carpeta = glob.glob(image_path+'*.jpg')
    aux=[]
    for fnames in todas_las_images_en_la_carpeta:
        aux.append(fnames.lstrip(image_path))
        
    todas_las_images_en_la_carpeta=aux
    
    imagenes_sin_clases_de_interes=[]
    for n in todas_las_images_en_la_carpeta:
        si_esta_la_imagen=False
        no_toma_la_imagen=False
        for k in imagenes_con_clases_de_interes:
            if n==k:
                si_esta_la_imagen=True
            if n!=k and si_esta_la_imagen==False:
                aux1=n
            if si_esta_la_imagen==True:
                no_toma_la_imagen=True
                    
        if no_toma_la_imagen==False:
            imagenes_sin_clases_de_interes.append(aux1)
            
    for n in imagenes_sin_clases_de_interes:
        file = open(Folder_labels+'/'+n.strip('.jpg')+'.txt','a')
        file.close()
    porcentaje_de_imagenes_sin_clases_de_interes_para_train=0.8
    num_clases_de_interes_para_train=int(porcentaje_de_imagenes_sin_clases_de_interes_para_train*len(imagenes_sin_clases_de_interes))
    
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
    print('El total de patrones de la clase '+labels[0]+' es: '+ str(clase_0))
    print('El total de patrones de la clase '+labels[1]+' es: '+ str(clase_1))
    print('El total de patrones de la clase '+labels[2]+' es: '+ str(clase_2))
    print('El total de imagenes sin clases de interes (sin label) es: '+ str(len(imagenes_sin_clases_de_interes)))
    print('')
    print('')
    print('Hay '+str(c_0)+' patrones en la clase '+labels[0]+' para test es decir un '+str("{:.2f}".format((c_0*100)/clase_0))+'%')
    print('Hay '+str(c_1)+' patrones en la clase '+labels[1]+' para test es decir un '+str("{:.2f}".format((c_1*100)/clase_1))+'%')
    print('Hay '+str(c_2)+' patrones en la clase '+labels[2]+' para test es decir un '+str("{:.2f}".format((c_2*100)/clase_2))+'%')
    print('Hay '+str(con_test)+' imagenes sin label para test es decir un '+str("{:.2f}".format((con_test*100)/len(imagenes_sin_clases_de_interes)))+'%') 
    c_00=0
    c_11=0
    c_22=0
    for n in codigos_train:
        if n==0:
            c_00+=1
        if n==1:
            c_11+=1
        if n==2:
            c_22+=1
    print('')
    print('')
    print('Hay '+str(c_00)+' patrones en la clase '+labels[0]+' para train es decir un '+str("{:.2f}".format((c_00*100)/clase_0))+'%')
    print('Hay '+str(c_11)+' patrones en la clase '+labels[1]+' para train es decir un '+str("{:.2f}".format((c_11*100)/clase_1))+'%')
    print('Hay '+str(c_22)+' patrones en la clase '+labels[2]+' para train es decir un '+str("{:.2f}".format((c_22*100)/clase_2))+'%')
    print('Hay '+str(con_train)+' imagenes sin label para train es decir un '+str("{:.2f}".format((con_train*100)/len(imagenes_sin_clases_de_interes)))+'%') 

            
            
       
Folder_labels='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/Info_dataset/labels'
VoTT_csv = '/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/Info_dataset/JPEGImages/libros_2-export.csv'
image_path='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/Info_dataset/JPEGImages/'
path_clases_file='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/clases'
Folder_para_direccion_de_imagenes_train='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/train.txt'
Folder_para_direccion_de_imagenes_test='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/test.txt'

try:
    os.mkdir(path_clases_file) 
    os.mkdir(Folder_labels) 
except OSError as e:
    if e.errno != errno.EEXIST:
        raise
csv_to_yolo_format(VoTT_csv,image_path,Folder_labels,path_clases_file,Folder_para_direccion_de_imagenes_train,Folder_para_direccion_de_imagenes_test) 

    
