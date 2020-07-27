from comunicacion_arduino import Obtener_datos
import serial

ser = serial.Serial("COM4",115200,timeout= 1)

ser.flush()
j = 0

f = open("datos.txt","w")
linea = 'Hora,Latitud,Longitud,Angulo X,Angulo Y,Angulo Z,Norte,Intencidad luz \n \r'
f.write(linea)
f.close()


while j < 1000:
    
    if ser.in_waiting > 0:
        datos = ser.readline().decode('utf-8').rstrip()
        linea,v = Obtener_datos(datos)
        
        if v == 1:
            f = open("datos.txt","a")
            f.write(linea)
            j = j + 1
            f.close()
            print(linea)
        
    
ser.close()