def Obtener_datos(datos):
    info = ''
    tem = ''
    contador = 0
    primero = 1
    valido = 0

    if len(datos) > 1 and datos[1] == '0':
        datos = datos[3:len(datos)]
        for i in range(len(datos)):
            if datos[i] == ',':
                contador = contador + 1
                primero = 1
            else:
                if contador == 0:
                    if primero == 1:
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 1:
                    if primero == 1:
                        x = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                
                if contador == 2:
                    if primero == 1:
                        y = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 3:
                    if primero == 1:
                        z = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 4:
                    if primero == 1:
                        norte = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                    
        if contador == 3:
            luz = tem
            info = ' '+ ',' + x + ',' + y + ',' + z + ',' + norte + ',' + luz + '\n'             
            valido = 1

    if len(datos) > 1 and datos[1] == '1':
        
        datos = datos[3:len(datos)]
        for i in range(len(datos)):
            if datos[i] == ',':
                contador = contador + 1
                primero = 1
            else:
                if contador == 0:
                    if primero == 1:
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 1:
                    if primero == 1:
                        tiempo = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 2:
                    if primero == 1:
                        latitud = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]                
                        
                if contador == 3:
                    if primero == 1:
                        longitud = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]                
                        
                if contador == 4:
                    if primero == 1:
                        x = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                
                if contador == 5:
                    if primero == 1:
                        y = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 6:
                    if primero == 1:
                        z = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 7:
                    if primero == 1:
                        norte = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                
        if contador == 7 and len(tiempo) > 2:
            luz = tem
            hora = int(tiempo[0]+tiempo[1])
            if hora < 5:
                hora = (hora + 24)- 5
                hora = str(hora)
                
            else:
                hora  = hora - 5
                hora = str(hora)
            
            tiempo = tiempo[2:len(tiempo)]
            info = hora + tiempo + ',' + str(latitud) + ',' + str(longitud) + ',' + x + ',' + y + ',' + z + ',' + norte + ',' +  luz + '\n'             
            valido = 1

    if len(datos) > 1 and datos[1] == '2':
    
        datos = datos[3:len(datos)]
        for i in range(len(datos)):
            if datos[i] == ',':
                contador = contador + 1
                primero = 1
            else:
                if contador == 0:
                    if primero == 1:
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 1:
                    if primero == 1:
                        tiempo = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 2:
                    if primero == 1:
                        latitud1 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]                
                        
                if contador == 3:
                    if primero == 1:
                        longitud1 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]                
                        
                if contador == 4:
                    if primero == 1:
                        latitud2 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 5:
                    if primero == 1:
                        longitud2 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                                                
                if contador == 6:
                    if primero == 1:
                        x = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                
                if contador == 7:
                    if primero == 1:
                        y = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 8:
                    if primero == 1:
                        z = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 9:
                    if primero == 1:
                        norte = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i] 
                
        if contador == 9 and len(tiempo) > 2:
            luz = tem
            latitud = round((float(latitud1) + float(latitud2))/2,6)
            longitud = round((float(longitud1) +float(longitud2))/2,6)
            hora = int(tiempo[0]+tiempo[1])
            if hora < 5:
                hora = (hora + 24)- 5
                hora = str(hora)
                
            else:
                hora  = hora - 5
                hora = str(hora)
            
            tiempo = tiempo[2:len(tiempo)]
            info = hora + tiempo + ',' + str(latitud) + ',' + str(longitud) + ',' + x + ',' + y + ',' + z + ',' + norte + ','  + luz + '\n'             
            valido = 1

    if len(datos) > 1 and datos[1] == '3':
        datos = datos[3:len(datos)]
        for i in range(len(datos)):
            if datos[i] == ',':
                contador = contador + 1
                primero = 1
            else:
                if contador == 0:
                    if primero == 1:
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 1:
                    if primero == 1:
                        tiempo = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 2:
                    if primero == 1:
                        latitud1 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]                
                        
                if contador == 3:
                    if primero == 1:
                        longitud1 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]                
                        
                if contador == 4:
                    if primero == 1:
                        latitud2 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 5:
                    if primero == 1:
                        longitud2 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                                                
                if contador == 6:
                    if primero == 1:
                        latitud3 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                
                if contador == 7:
                    if primero == 1:
                        longitud3 = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 8:
                    if primero == 1:
                        x = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                
                if contador == 9:
                    if primero == 1:
                        y = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                        
                if contador == 10:
                    if primero == 1:
                        z = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                
                if contador == 11:
                    if primero == 1:
                        norte = tem 
                        tem = datos[i]
                        primero = 0
                    else:
                        tem = tem + datos[i]
                
                
        if contador == 11 and len(tiempo) > 2:
            luz = tem
            latitud = round((float(latitud1) + float(latitud2) + float(latitud3))/3,6)
            longitud = round((float(longitud1) +float(longitud2) +float(longitud3))/3,6)
            hora = int(tiempo[0]+tiempo[1])
            if hora < 5:
                hora = (hora + 24)- 5
                hora = str(hora)
                
            else:
                hora  = hora - 5
                hora = str(hora)
            
            tiempo = tiempo[2:len(tiempo)]
            info = hora + tiempo + ',' + str(latitud) + ',' + str(longitud) + ',' + x + ',' + y + ',' + z + ',' +  norte + ',' +luz + '\n'             
            valido = 1

    return info,valido
