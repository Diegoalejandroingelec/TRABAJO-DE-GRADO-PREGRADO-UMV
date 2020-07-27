/* Ruler 1         2         3         4         5         6         7        */
/******************************************************************************/
/*                                                                            */
/* 							   GPS.C                                          */
/*                                                                            */
/*          DEVELOPED BY: Javier Enrique Huerfano Diaz                        */
/*                    Diego Alejandro Ramirez Vargas                          */
/*                                                                            */
/*          Bogota, D.C., June 3th, 2020.                                     */
/*                                                                            */
/*          Copyright (C) Electronics Engineering Program                     */
/*                    School of Engineering                                   */
/*                    Pontificia Universidad Javeriana                        */
/*                    Bogota - Colombia - South America                       */
/*                                                                            */
/******************************************************************************/

/************************************  GPS.c  *********************************/
/*                                                                            */
/*   Proposito: Obtener coordenadas de GPS en latitud y longitud              */
/*                                                                            */
/*                                                                            */
/*                                                                            */
/*   -----------------------------------------------------------------------  */
/*    Junio 1/20               Implementación inicial                         */
/*                                                                            */

/********************************** Headers ***********************************/

/* ------------------------ Inclusión de Std Headers ------------------------ */
#include <math.h>
#include <util/delay.h>

/* ----------------------- Inclusión de otros  Headers ----------------------- */

#include "GPS.h"
#include "Uart_atmega2560.h"

/*****************************  Funciones  **************************************/

/*FN****************************************************************************
*
*   int GPS_Store(DATA_GPS_T *gps -> Apuntador a una variable que almacena los 
*									datos recidos
*                 unsigned char c -> Caracter a almacenar 
*				  )
*
*   Retorna: 1 si se ha terminado de recibir toda la información
*
*   Funcionamiento: Almacena los caracteres recibidos 
*
*		           Estado 0: Cambia de estado una vez es recibido un $ y 
*			       reinicia los contadores.
*	
*				   Estado 1: Cambia de estado una vez recibida una ,
*
*				   Estado 2: Almacena los datos correspondientes a la hora 
*				   cambia de estado una vez recibida una ,
*
*				   Estado 3: Si se recibe una V se regresa al estado 0.
*				   Si es recido un caracter distinto y una , cambia al 
*				   estado 4.
*							
*				   Estado 4: Almacena los datos correspondientes a la latitud
*				   cambia de estado una vez recibida una ,
*
*				   Estado 5: Almacena la orientacion ya sea norte o sur
*				   cambia de estado una vez recibida una ,
* 
*				   Estado 6: Almacena los datos correspondientes a la longitud
*				   cambia de estado una vez recibida una ,
*
*				   Estado 7: Almacena la orientacion ya sea esto u oeste
*				   cambia de estado una vez recibida una ,
* 								 
*   -----------------------------------------------------------------------
*   Junio 1/20               Implementación inicial
*
*******************************************************************************/

int GPS_Store(DATA_GPS_T *gps, unsigned char c){
	int finish = 0;
	
	switch(gps->state_machine){
		case 0:
			if(c == 36){
				gps->count_lat = 0;
				gps->count_lon = 0;
				gps->count_time = 0;
				gps->state_machine = 1;
			}else{
				gps->state_machine = 0;
				finish = 0;
			}
		break;
			
		case 1:
			if(c == 44){
				gps->state_machine = 2;
			}else{
				gps->state_machine = 1;
			}
		break;
			
		case 2:
			if(c == 44){
				gps->state_machine = 3;
			}else{
				gps->time[gps->count_time++] = c;
				gps->state_machine = 2;
			}
		break;
			
		case 3:
			if(c == 44){
				gps->state_machine = 4;
			}else if(c == 65){
				gps->state_machine = 3;
			}else{
				gps->state_machine = 0;
			}
		break;
			
		case 4:
			if(c == 44){
				gps->state_machine = 5;
			}else{
				gps->latitude_str[gps->count_lat++] = c;
				gps->state_machine = 4;
			}
		break;
			
		case 5:
			if(c == 44){
				gps->state_machine = 6;
			}else{
				gps->orientation[0] = c;
				gps->state_machine = 5;
			}
		break;
			
		case 6:
			if(c == 44){
				gps->state_machine = 7;
			}else{
				gps->longitude_str[gps->count_lon++] = c;
				gps->state_machine = 6;
			}
		break;
			
		case 7:
			if(c == 44){
				gps->state_machine = 0;
				finish = 1;
			}else{
				gps->orientation[1] = c;
				gps->state_machine = 7;
			}
		break;
			
/*		case 8:
			if(c == 42){
				finish = 1;
				gps->state_machine = 0;
			}else{
				gps->state_machine = 8;
			}
		break;*/
		
	}
	return finish;
}

/*FN****************************************************************************
*
*	float GPS_Get_Longitude(unsigned char *longitude_str-> Apuntador al arreglo
*                           que almacena la longitud. 
*						    int count_lon-> tamaño del arreglo
*							unsigned char orientation-> orientación este u oeste
*						   )
*
*   Retorna: Retorna la longitud en grados decimales
*
*   Funcionamiento: 
*					parte 1: Separa la medida en grados y minutos
*					parte 2: determina la medida de longitud en grados decimales
*			        parte 3: Si es orientación es oeste el valor de la longitud 
*					debe ser negativo 
*
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/
float GPS_Get_Longitude(unsigned char *longitude_str,int count_lon,unsigned char orientation ){
	
	float longitude;
	float minute;
	int degrees;
	int i = 1;
	
	unsigned char *ptr;
	ptr = longitude_str;

/* ------------------------------- Parte 1 -------------------------------- */
	
	degrees = (*ptr - 48)*100 + (*(ptr+1) - 48)*10 + (*(ptr+2) - 48);
	minute =  (*(ptr+3) - 48)*10 + ((*(ptr+4) - 48));
	
	for(ptr = longitude_str + 6;ptr < longitude_str + count_lon;){
		minute+= (*(ptr++)-48)/pow(10.0,i);
		i++;
	}

/* ------------------------------- Parte 2 -------------------------------- */
	
	longitude = degrees + minute/60.0;
	
/* ------------------------------- Parte 3 -------------------------------- */
	
	if(orientation == 87)
		longitude = -longitude;
	
	return longitude;
}

/*FN****************************************************************************
*
*	float  GPS_Get_Latitude(unsigned char *latitude_str-> Apuntador al arreglo
*                           que almacena la latitud.
*						    int count_lon-> tamaño del arreglo
*							unsigned char orientation-> orientación norte o sur
*						   )
*
*   Retorna: Retorna la latitud en grados decimales
*
*   Funcionamiento:
*					parte 1: Separa la medida en grados y minutos
*					parte 2: determina la medida de latitud en grados decimales
*			        parte 3: Si es orientación es sur el valor de la latitud
*					debe ser negativo
*
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/

float GPS_Get_Latitude(unsigned char *latitude_str,int count_lat,unsigned char orientation ){
	float latitude;
	float minute;
	int degrees;
	int i = 1;
	
	unsigned char *ptr;
	ptr = latitude_str;

/* ------------------------------- Parte 1 -------------------------------- */
	
	degrees = (*ptr - 48)*10 + (*(ptr+1) - 48);
	minute =  (*(ptr+2) - 48)*10 + ((*(ptr+3) - 48));
	
	for(ptr = latitude_str + 5;ptr < latitude_str + count_lat;){
		minute+= (*(ptr++)-48)/pow(10.0,i);
		i++;
	}

/* ------------------------------- Parte 2 -------------------------------- */

	latitude = degrees + minute/60.0;

/* ------------------------------- Parte 3 -------------------------------- */

	if(orientation == 83)
		latitude = -latitude;
	
	return latitude;
}

/*FN****************************************************************************
*
*	void GPS_Set_Up(void (*fun_prt_transmit)(unsigned char) -> Apuntador a la
*					función de transmisión de un puerto serial  
*					void (*fun_prt_init)(unsigned int) -> Apuntador a la
*					función de configuración de un puerto serial 
*					)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Configura la tasa de transmisión, frecuencia de envio de 
*					datos y desactiva algunos formatos
*		
*					parte 1: Cambiar la tasa de transmisión  del modulo GPS
*					a 115200 baudios
*					parte 2: Cambiar la tasa de transmisión  del puerto uart
*					a 115200 baudios
*					parte 3: desactivar los formatos VTG, GLL, GGA, GSA
*                   y GSV.
*
*					parte 4: cambiar la frecuencia de envio de datos a 10Hz
*
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/


void GPS_Set_Up(void (*fun_prt_transmit)(unsigned char),void (*fun_prt_init)(unsigned int)){
	
	/*  Palabras de configuración del modulo gps 7m  */ 
	
	unsigned char VTG_OFF[26] = {181, 98,  6, 1, 8, 0, 240, 5, 0, 0, 0, 0, 0, 1, 5, 71,  181, 98,  6, 1, 2, 0, 240, 5, 254, 22};
	unsigned char GLL_OFF[26] = {181, 98,  6, 1, 8, 0, 240, 1, 0, 0, 0, 0, 0, 1, 1, 43,  181, 98,  6, 1, 2, 0, 240, 1, 250, 18};
	unsigned char GGA_OFF[26] = {181, 98,  6, 1, 8, 0, 240, 0, 0, 0, 0, 0, 0, 1, 0, 36,  181, 98,  6, 1, 2, 0, 240, 0, 249, 17};
	unsigned char GSV_OFF[26] = {181, 98,  6, 1, 8, 0, 240, 3, 0, 0, 0, 0, 0, 1, 3, 57,  181, 98,  6, 1, 2, 0, 240, 3, 252, 20};
	unsigned char GSA_OFF[26] = {181, 98,  6, 1, 8, 0, 240, 2, 0, 0, 0, 0, 0, 1, 2, 50,  181, 98,  6, 1, 2, 0, 240, 2, 251, 19};
	unsigned char BAUD_RATE_115200[61] = {36, 69, 73, 71, 65, 81, 44, 86, 84, 71, 42, 51, 50, 13, 10, 181, 98, 6, 0, 1, 0, 1, 8, 34, 181, 98, 6, 0, 20, 0, 1, 0, 0, 0, 208, 8, 0, 0, 0, 194, 1, 0, 7, 0, 3, 0, 0, 0, 0, 0, 192, 126, 181, 98, 6, 0, 1, 0, 1, 8, 34 };
	unsigned char RATE_10_HZ[22]= {181, 98, 6, 8, 6, 0, 100, 0, 1, 0, 1, 0, 122, 18, 181, 98, 6, 8, 0, 0, 14, 48 };
	
/* ------------------------------- Parte 1 -------------------------------- */

	
	UART_Write_array(BAUD_RATE_115200,61,(*fun_prt_transmit));
	_delay_ms (100);

/* ------------------------------- Parte 2 -------------------------------- */
	
	fun_prt_init(16);
	
/* ------------------------------- Parte 3 -------------------------------- */

	
	UART_Write_array(VTG_OFF,26,(*fun_prt_transmit));
	UART_Write_array(GLL_OFF,26,(*fun_prt_transmit));
	UART_Write_array(GGA_OFF,26,(*fun_prt_transmit));
	UART_Write_array(GSV_OFF,26,(*fun_prt_transmit));
	UART_Write_array(GSA_OFF,26,(*fun_prt_transmit));
	
/* ------------------------------- Parte 4 -------------------------------- */
	
	UART_Write_array(RATE_10_HZ,22,(*fun_prt_transmit));
	
}

/*FN****************************************************************************
*
*	void GPS_Copy_time(unsigned char *time_str->arreglo a copiar 
*					   unsigned char *time_cpy->arreglo donde se guardaran los 
*					   datos de la hora actual 
*                      int size_cpy -> numuro de caracteres a copiar
*                       )
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Copia los caracteres de la hora actual en otro arreglo 
*
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/

void GPS_Copy_time(unsigned char *time_str,unsigned char *time_cpy,int size_cpy){
	unsigned char *source_ptr;
	unsigned char *dest_ptr;
	
	dest_ptr = time_cpy;
	for(source_ptr = time_str;source_ptr< time_str + size_cpy;){
		*(dest_ptr++) = *(source_ptr++);
	}
}
