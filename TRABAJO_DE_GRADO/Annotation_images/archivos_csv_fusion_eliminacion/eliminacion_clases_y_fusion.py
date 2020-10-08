import pandas as pd
import glob

def elimina_clases(path_archivo_inp,path_archivo_out,clase_para_eliminar):
    archivo_original=pd.read_csv(path_archivo_inp)

    image=[]
    xmin=[]
    ymin=[]
    xmax=[]
    ymax=[]
    label=[]
    for indice, row in archivo_original.iterrows():
        if row[["label"]].tolist()!=[clase_para_eliminar]:
            image.append(row[["image"]].tolist()[0])
            xmin.append(row[["xmin"]].tolist()[0])    
            ymin.append(row[["ymin"]].tolist()[0]) 
            xmax.append(row[["xmax"]].tolist()[0]) 
            ymax.append(row[["ymax"]].tolist()[0])
            label.append(row[["label"]].tolist()[0]) 
    
    data = {'image':image,
        'xmin':xmin ,
        'ymin':ymin ,
        'xmax':xmax ,
        'ymax':ymax,
        'label':label}
    df = pd.DataFrame(data, columns = ['image', 'xmin', 'ymin','xmax', 'ymax','label'])
    df.to_csv(path_archivo_out,index=False)

def fusionar_archivos_csv(path_de_archivos_a_fusionar,path_de_archivo_fusionado):
    all_data = pd.DataFrame() 
    dfs = []
    flag_de_header=True
    for f in glob.glob(path_de_archivos_a_fusionar+"*.csv"): 
        if flag_de_header:
            df = pd.read_csv(f,header=None)
            flag_de_header=False
        else:
            df = pd.read_csv(f,header=None,skiprows = 1) 
            
        dfs.append(df) 
           
    all_data = pd.concat(dfs, ignore_index=True)
    all_data.to_csv(path_de_archivo_fusionado, index=None,header=None)



path_archivo_inp='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/Info_dataset/JPEGImages/libros_2-export.csv'
path_archivo_out='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/archivos_csv_fusion_eliminacion/base_datos_con_clase_eliminada.csv'

path_de_archivos_a_fusionar='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/archivos_csv_fusion_eliminacion/archivos_a_fusionar/'
path_de_archivo_fusionado='/home/diego/TRABAJO-DE-GRADO-PREGRADO-UMV/TRABAJO_DE_GRADO/Annotation_images/archivos_csv_fusion_eliminacion/archivo_fusionado.csv'


clase_para_eliminar='LIBRO'


fusionar_archivos_csv(path_de_archivos_a_fusionar,path_de_archivo_fusionado)

#elimina_clases(path_archivo_inp,path_archivo_out,clase_para_eliminar)

    
    

