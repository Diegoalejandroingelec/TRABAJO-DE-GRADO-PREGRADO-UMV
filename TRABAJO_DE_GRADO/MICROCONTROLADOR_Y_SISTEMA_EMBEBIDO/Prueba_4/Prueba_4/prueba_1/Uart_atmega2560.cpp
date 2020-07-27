/* Ruler 1         2         3         4         5         6         7        */
/******************************************************************************/
/*                                                                            */
/* 		                   Uart_atmega2560.C                                  */
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

/****************************  Uart_atmega2560.h  *****************************/
/*                                                                            */
/*   Proposito: Manejo del puerto uart                                        */
/*                                                                            */
/*   -----------------------------------------------------------------------  */
/*    Junio 1/20               Implementación inicial                         */
/*                                                                            */

/********************************** Headers ***********************************/

/* ------------------------ Inclusión de Std Headers ------------------------ */
#include <math.h>

/* ----------------------- Inclusión de otros  Headers ----------------------- */

#include "Uart_atmega2560.h"

/*****************************  Funciones  **************************************/

/*FN****************************************************************************
*
*	void UART_Begin(SERIAL_T *serial-> Variable que maneja el buffer de recepción
*                   char *buffer_rx-> buffer de recepción
*                   void (*fun_prt)(unsigned int)-> apuntador a la función de 
*					configuración de un puerto serial 
*                   unsigned int ubrr-> tasa de transmisión
*                  )
*
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Incializa los contadores del buffer y hace llamado a la
*					función que configura el puerto serial
*
*   -----------------------------------------------------------------------
*   Jun 1/20               Implementación inicial
*
*******************************************************************************/

void UART_Begin(SERIAL_T *serial, char *buffer_rx,void (*fun_prt)(unsigned int),unsigned int ubrr){
	serial->count = 0;
	serial->count_input = 0;
	serial->count_output = 0;
	serial->input = buffer_rx;
	serial->output = buffer_rx;
	fun_prt(ubrr);
}

/*FN****************************************************************************
*
*	void UART_Store(SERIAL_T *serial-> Variable que maneja el buffer de recepción
*	                char data -> Dato a almacenar
*                  )
*
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Si la cantidad de datos almacenados no es mayor al tamaño
*					del buffer se almacena el dato y aumenta la cantidad de 
*                   datos guardados y el contador de entrada
*                
*   -----------------------------------------------------------------------
*   Jun 1/20               Implementación inicial
*
*******************************************************************************/

void UART_Store(SERIAL_T *serial,char data){
	if(serial->count<MAX_BUFFER){
		*(serial->input) = data;
		serial->count++;
		if(++(serial->count_input) < MAX_BUFFER){
			serial->input++;
			}else{
			serial->input = serial->input - (MAX_BUFFER - 1);
			serial->count_input = 0;
		}
	}
}

/*FN****************************************************************************
*
*	int UART_available(SERIAL_T *serial->Variable que maneja el buffer de recepción
*                     )
*
*   Retorna: Retorna la cantidad de datos en el buffer
*
*
*   -----------------------------------------------------------------------
*   Jun 1/20               Implementación inicial
*
*******************************************************************************/

int UART_available(SERIAL_T *serial){
	return serial->count;
}

/*FN****************************************************************************
*
*	char UART_Read(SERIAL_T *serial->Variable que maneja el buffer de recepción
*                  )
*
*   Retorna: Retorna un valor del buffer de recepción
*
*   Funcionamiento: Si hay algun dato en buffer lo retorna y decrementa el 
*					numero de datos almacenados e incrementa el contador de 
*					salida.
*
*   -----------------------------------------------------------------------
*   Jun 1/20               Implementación inicial
*
*******************************************************************************/

char UART_Read(SERIAL_T *serial){
	char data = 0;
	if(serial->count != 0){
		data = *(serial->output);
		serial->count--;
		if(++(serial->count_output) < MAX_BUFFER){
			serial->output++;
			}else{
			serial->output = serial->output - (MAX_BUFFER - 1);
			serial->count_output = 0;
		}
	}
	return data;
}

/*FN****************************************************************************
*
*	void Num_to_str(float num-> Numero a descomponer en sus digitos 
*                   char *str-> Apuntador a arreglo que almacenara los digitos
*                   int *digits-> Cantidad de digitos almacenados
*                   int n -> Numero de decimales
*                  )
*
*   Retorna: No retorna nada, el arreglo que almacena los digitos pasa por 
*			 referencia 
*
*   Funcionamiento: Recibe una variable de tipo float para descomperla en digitos
*					para se almacenados en un arreglo de tipo char
*
*					- Parte 1: determinar si el numero es negativo
*					- Parte 2: descomponer y almacenar los digitos de la parte
*					entera del numero de entrada
*					- Parte 3: descomponer y almacenar los digitos de la parte
*					decimal del numero de entrada
*   -----------------------------------------------------------------------
*   Jun 1/20               Implementación inicial
*
*******************************************************************************/

void Num_to_str(float num, char *str,int *digits,int n){
	
	int count = 1;
	unsigned int int_part;
	float float_part;
	int i = 0;
	int number = 0;
	
/* ------------------------------- Parte 1 -----------------------------------*/	
	
	if(num<0){
		*(str++) = '-';
		(*digits)++;
		num = -1*num;
	}

/* ------------------------------- Parte 2 -----------------------------------*/

	int_part = num;
	float_part = num-int_part;
	while(int_part>pow(10,count)){
		count++;
	}

	for(i = count;i > 0;i--){
		number = (unsigned int)(int_part/pow(10,i-1))%10;
		*(str++) = number + 48;
		(*digits)++;
	}

/* ------------------------------- Parte 3 -----------------------------------*/

	if(n>0){
		*(str++) = '.';
		(*digits)++;
		i = 1;
		while(n>=i){
			number = (unsigned int)(float_part*pow(10,i))%10;
			*(str++) = number + 48;
			(*digits)++;
			i++;
		}
	}
}

/*FN****************************************************************************
*
*	void UART_Write(float num -> Numero a transmitir 
*                   int n -> cantidad de decimales 
*                   void (*fun_prt)(unsigned char) -> Apuntador a la función 
*					para transmitir por el puerto uart 
*                  )
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Recibe una variable de tipo float la decompone de sus
*					digitos y los envia por separado a traves de un puerto 
*                   uart
*
*   -----------------------------------------------------------------------
*   Jun 1/20               Implementación inicial
*
*******************************************************************************/

void UART_Write(float num,int n,void (*fun_prt)(unsigned char)){
	char str[MAX_BUFFER_TX];
	int digits = 0;
	
	Num_to_str(num,&str[0],&digits,n);
	char *ptr;

	for(ptr = str;ptr<str + digits;){
		fun_prt(*(ptr++));
	}

}

/*FN****************************************************************************
*
*	void UART_Write_array(unsigned char *array->apuntador al arreglo a transmitir
*                         int size_array->tamaño del arreglo
*                         void (*fun_prt)(unsigned char)->Apuntador a la función
*					      para transmitir por el puerto uart
*                        )
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Transmite cada una de las posiciones de un arreglo de tipo
*				    char.
*
*   -----------------------------------------------------------------------
*   Jun 1/20               Implementación inicial
*
*******************************************************************************/

void UART_Write_array(unsigned char *array, int size_array,void (*fun_prt)(unsigned char)){
	
	unsigned char *ptr;
	for(ptr = array;ptr<array + size_array;){
		fun_prt(*(ptr++));
	}
}