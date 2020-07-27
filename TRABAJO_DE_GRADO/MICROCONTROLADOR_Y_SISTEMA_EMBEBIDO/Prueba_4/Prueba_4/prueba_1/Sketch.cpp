/* Ruler 1         2         3         4         5         6         7        */
/******************************************************************************/
/*                                                                            */
/* 				SISTEMA PARA ACELERACIÓN DE DETECCIÓN DE FALLAS               */
/*					SOBRE EL PAVIMENTO EN LA CIUDAD DE BOGOTÁ                 */
/*   ┌────┐ ┌────┐                     		                                  */
/*   └┐  ┌┘ └┐╔══╧═╗                                                          */
/*    │  │   │╚╗  ╔╝      DEVELOPED BY: Javier Enrique Huerfano Diaz          */
/*    │  │   │ ║  ║                     Diego Alejandro Ramirez Vargas        */
/*    │  │   │ ║  ║                                                           */
/*    │╔═╧══╗│ ║  ║       Bogota, D.C., June 3th, 2020.                       */
/*    │╚╗  ╔╝┘ ║  ║                                                           */
/*    └┐║  ╚╗ ╔╝  ║       Copyright (C) Electronics Engineering Program       */
/*     └╚╗  ╚═╝  ╔╝                     School of Engineering                 */
/*      └╚╗     ╔╝                      Pontificia Universidad Javeriana      */
/*        ╚═════╝                       Bogota - Colombia - South America     */
/*                                                                            */
/******************************************************************************/

/********************************** Headers ***********************************/

/*------------------------------ headers standard ----------------------------*/

#include <util/delay.h>
#include <avr/interrupt.h>

/*------------------------------ headers arduino -----------------------------*/

#include <Wire.h>
#include <Adafruit_Sensor.h>
#include <Adafruit_BNO055.h>
#include <utility/imumaths.h>

/*------------------------------ otros headers   -----------------------------*/

#include "Uart_atmega2560.h"
#include "AP3216.h"
#include "GPS.h"
#include "Timeout.h"

/*-------------------------------- constantes   -----------------------------*/

#define  MAGNETIC_DECLINATION 7.23

/*********************** Prototipos de funciones ***************************/

void setup(void );
void loop(void );

/*************************** Variables Globales ******************************/

/*------------------------- Variables puertos UART---------------------------*/

SERIAL_T serial_0; 
SERIAL_T serial_1;
SERIAL_T serial_2;
SERIAL_T serial_3;

char RX_0;
char RX_1;
char RX_2;
char RX_3;

char buffer_rx0[MAX_BUFFER];
char buffer_rx1[MAX_BUFFER];
char buffer_rx2[MAX_BUFFER];
char buffer_rx3[MAX_BUFFER];


/*----------------------------- Variables GPS -------------------------------*/

DATA_GPS_T data_gps1;
DATA_GPS_T data_gps2;
DATA_GPS_T data_gps3;

unsigned char c1;
int finish1 = 0;
float longitude1;
float latitude1;
int count_t1;
unsigned char time_gps_1[10];

unsigned char c2;
int finish2 = 0;
float longitude2;
float latitude2;
int count_t2;
unsigned char time_gps_2[10];


unsigned char c3;
int finish3 = 0;
float longitude3;
float latitude3;
int count_t3;
unsigned char time_gps_3[10];

int flag_gps1;
int flag_gps2;
int flag_gps3;
int count_gps;

/*----------------------------- Variables IMU -------------------------------*/

Adafruit_BNO055 bno = Adafruit_BNO055(55);
sensors_event_t event;
imu::Vector<3> magnetic;
float north_angle;

/*--------------------------- Variables Sensor de luz -----------------------*/

LUX_RANGE_T luxRange;
float als;

/*--------------------------- Otras variables -------------------------------*/

TIMEOUT_T tm_out;


/*FN****************************************************************************
*
*	void USART0_Init( unsigned int ubrr -> Parametro para definir la tasa de
*					  de transmisión.
*					)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Configura la tasa de transmisión, y longitud de datos en 8
*					bits, 1 bit de parada y sin pariedad para el puerto UART 0
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/

void USART0_Init( unsigned int ubrr){
	UCSR0B &= 0x00;
	UCSR0C &= 0x00;
	/* definir la tasa de transmisión */
	UBRR0H = (unsigned char)(ubrr>>8);
	UBRR0L = (unsigned char)ubrr;
	/* habilitar la recepción,transmisión e interrupciones de recepción*/
	UCSR0B |= (1<<RXEN0)|(1<<TXEN0)|(1<<RXCIE0);
	/* definir el formato en 8 bits de datos,1 bit de parada y sin paridad*/
	UCSR0C |= (1<<UCSZ01)|(1<<UCSZ00);
	/* habilita el modo double speed */
	UCSR0A |= (1<<U2X0);
}

/*FN****************************************************************************
*
*	void USART0_Transmit( unsigned char data -> byte a transmitir
*						)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Envia un byte por el puerto UART 0
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/

void USART0_Transmit( unsigned char data ){
	/* espera que el buffer este vacio */
	while ( !( UCSR0A & (1<<UDRE0)) );
	/* coloca el dato en el buffer */
	UDR0 = data;
}

/*FN****************************************************************************
*
*	void USART1_Init( unsigned int ubrr -> Parametro para definir la tasa de
*					  de transmisión.
*					)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Configura la tasa de transmisión, y longitud de datos en 8
*					bits, 1 bit de parada y sin pariedad para el puerto UART 1
*   -----------------------------------------------------------------------
*   Mar 23/20                Implementación inicial
*
*******************************************************************************/

void USART1_Init( unsigned int ubrr){
	UCSR1B &= 0x00;
	UCSR1C &= 0x00;
	UBRR1H = (unsigned char)(ubrr>>8);
	UBRR1L = (unsigned char)ubrr;
	UCSR1B |= (1<<RXEN1)|(1<<TXEN1)|(1<<RXCIE1);
	UCSR1C |= (1<<UCSZ11)|(1<<UCSZ10);
	UCSR1A |= (1<<U2X1);

}

/*FN****************************************************************************
*
*	void USART1_Transmit( unsigned char data -> byte a transmitir
*						)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Envia un byte por el puerto UART 1
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/

void USART1_Transmit( unsigned char data ){
	while ( !( UCSR1A & (1<<UDRE1)) );
	UDR1 = data;
}

/*FN****************************************************************************
*
*	void USART2_Init( unsigned int ubrr -> Parametro para definir la tasa de
*					  de transmisión.
*					)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Configura la tasa de transmisión, y longitud de datos en 8
*					bits, 1 bit de parada y sin pariedad para el puerto UART 2
*   -----------------------------------------------------------------------
*   Mar 23/20                Implementación inicial
*
*******************************************************************************/

void USART2_Init( unsigned int ubrr){
	UCSR2B &= 0x00;
	UCSR2C &= 0x00;
	UBRR2H = (unsigned char)(ubrr>>8);
	UBRR2L = (unsigned char)ubrr;
	UCSR2B |= (1<<RXEN2)|(1<<TXEN2)|(1<<RXCIE2);
	UCSR2C |= (1<<UCSZ21)|(1<<UCSZ20);
	UCSR2A |= (1<<U2X2);
}

/*FN****************************************************************************
*
*	void USART2_Transmit( unsigned char data -> byte a transmitir
*						)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Envia un byte por el puerto UART 2
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/

void USART2_Transmit( unsigned char data ){
	while ( !( UCSR2A & (1<<UDRE2)) );
	UDR2 = data;
}

/*FN****************************************************************************
*
*	void USART3_Init( unsigned int ubrr -> Parametro para definir la tasa de
*					  de transmisión.
*					)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Configura la tasa de transmisión, y longitud de datos en 8
*					bits, 1 bit de parada y sin pariedad para el puerto UART 3
*   -----------------------------------------------------------------------
*   Mar 23/20                Implementación inicial
*
*******************************************************************************/

void USART3_Init( unsigned int ubrr){
	UCSR3B &= 0x00;
	UCSR3C &= 0x00;
	UBRR3H = (unsigned char)(ubrr>>8);
	UBRR3L = (unsigned char)ubrr;
	UCSR3B |= (1<<RXEN3)|(1<<TXEN3)|(1<<RXCIE3);
	UCSR3C |= (1<<UCSZ31)|(1<<UCSZ30);
	UCSR3A |= (1<<U2X3);
}

/*FN****************************************************************************
*
*	void USART3_Transmit( unsigned char data -> byte a transmitir
*						)
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Envia un byte por el puerto UART 3
*   -----------------------------------------------------------------------
*   Mar 23/20               Implementación inicial
*
*******************************************************************************/

void USART3_Transmit( unsigned char data ){
	while ( !( UCSR3A & (1<<UDRE3)) );
	UDR3 = data;
}

/*FN****************************************************************************
*
*	void setupTimer1(int count -> Numero de pulsos a contar
*					 int prescaler -> Prescaler a configurar
*					)
*
*   Retorna: no retorna nada
*
*   Funcionamiento: Se configura el timer 1 de 16 bits de microprocesador en modo
*			       	CTC con el precalerm y valor a contar deseados ademas de
*					habilitar las interrupciones
*
*   -----------------------------------------------------------------------
*   Mayo 4/20               Implementación inicial
*
*******************************************************************************/

void setupTimer1(int count, int prescaler) {
	// reset registros
	TCCR1A = 0;
	TCCR1B = 0;
	TCNT1 = 0;

	OCR1A = count;
	// CTC
	TCCR1B |= (1 << WGM12);

	switch(prescaler){
		
		case 1:
		// Prescaler 1
		TCCR1B |= (1 << CS10);
		break;
		case 8:
		// Prescaler 8
		TCCR1B |= (1 << CS11);
		break;
		case 64:
		// Prescaler 64
		TCCR1B |= (1 << CS11) | (1 << CS10);
		break;
		case 256:
		// Prescaler 64
		TCCR1B |= (1 << CS12);
		break;
		case 1024:
		// Prescaler 1024
		TCCR1B |= (1 << CS12) | (1 << CS10);
		break;
	}
	
	// Habilitar interrupciones
	TIMSK1 |= (1 << OCIE1A);
}

	
/*FN****************************  setup function  ******************************
*
*	Propósito: Configurar cada los sensores de GPS, IMU y de luz ambiente ademas
*			   de los cuatro puertos UART e I2C 
*
*	Funcionamiento :
*					 Parte 1: Configuración de los 4 puertos UART y el puerto
*							  I2C
*					 Parte 2: Configurar el rango del sensor de luz ambiente
*					 Parte 3: Inicializar la unidad de medición inercial 
*					 Parte 4: Configurar los modulos GPS
*				     Parte 5: Configurar el timer 1 del microcontrolador y 
*					 el timeout 
*
*   -----------------------------------------------------------------------
*   Junio 1/20               Implementación inicial 
*
*******************************************************************************/

void setup(void)
{

/*------------------------------- Parte 1 -----------------------------------*/

	/* Tasa de tranmisión 115200 baudios en el puerto 0 mientras que en los 
	puertos 1,2,3 la tasa de transmisión se ajusta en 9600 baudios */ 
	
	UART_Begin(&serial_0,&buffer_rx0[0],&USART0_Init,16);
	UART_Begin(&serial_1,&buffer_rx1[0],&USART1_Init,207);
	UART_Begin(&serial_2,&buffer_rx2[0],&USART2_Init,207);
	UART_Begin(&serial_3,&buffer_rx3[0],&USART3_Init,207);
	Wire.begin();
	
/*------------------------------ Parte 2 -------------------------------------*/

	/* Rango de luz ambiente 20661 lux */
		
	luxRange = RANGE_20661;
	AP3216_init(luxRange,ALS);

/*------------------------------ Parte 3 -------------------------------------*/
	
	if(!bno.begin())
	{
		while(1);
	}
	_delay_ms(1000);
	bno.setExtCrystalUse(true);

/*------------------------------ Parte 4 -------------------------------------*/	
	
	/* Se configuran los modulos GSP a una tasa de transmisión de 115200 baudios
	de igual manera se cambia a esa tasa los puertos uart 1,2 y 3, ademas se 
	cambia la frecuencia de transmisión a 10Hz y desactiva de los formatos 
	VTG, GLL, GGA, GSA, GSV */
	
	GPS_Set_Up(&USART1_Transmit,&USART1_Init);
	GPS_Set_Up(&USART2_Transmit,&USART2_Init);
	GPS_Set_Up(&USART3_Transmit,&USART3_Init);
	
/*------------------------------- Parte 5 -----------------------------------*/	
	
	setupTimer1(1249,64);
	Start_Timeout(&tm_out,15);	
	data_gps1.state_machine = 0;
	data_gps2.state_machine = 0;
	data_gps3.state_machine = 0;
	
}

/*FN****************************  loop function  ******************************
*
*	Propósito: Hacer la lectura de cada uno de los sensores y transmitirlos 
*			   por medio del puerto uart 0
*
*	Funcionamiento : Parte 1: Si hay datos de alguno de los buffers de recepción 
*					 serial se lee y almacenan los datos de interes una vez es
*					 recibida un trama completa valida se procesa y obtiene
*                    la latitud, longitud y hora actual.
*	
*					 Parte 2: Una vez la bandera que indica que hay timeout esta 
*				     en 1 se leen los datos del sensor de orientación y del sensor
*					 de luz para posteriormente enviar los datos leidos por el
*                    puerto UART 0 junto con la información de los GPS			        
*
*   -----------------------------------------------------------------------
*   Junio 1/20               Initial implementation
*
*******************************************************************************/

void loop(void)
{
/*------------------------------- Parte 1 -----------------------------------*/	

/*-------------------------------- GPS 1 ------------------------------------*/

	
	if(UART_available(&serial_1)){
		c1 = UART_Read(&serial_1);
		finish1 = GPS_Store(&data_gps1,c1);
		if(finish1){
			latitude1 = GPS_Get_Latitude(data_gps1.latitude_str,data_gps1.count_lat,data_gps1.orientation[0]);
			longitude1 = GPS_Get_Longitude(data_gps1.longitude_str,data_gps1.count_lon,data_gps1.orientation[1]);
			GPS_Copy_time(data_gps1.time,time_gps_1,data_gps1.count_time);
			count_t1 = data_gps1.count_time;
			flag_gps1 = 1;
		}
	}
	
/*-------------------------------- GPS 2 ------------------------------------*/
	
	if(UART_available(&serial_2)){
		c2 = UART_Read(&serial_2);
		finish2 = GPS_Store(&data_gps2,c2);
		if(finish2){
			latitude2 = GPS_Get_Latitude(data_gps2.latitude_str,data_gps2.count_lat,data_gps2.orientation[0]);
			longitude2 = GPS_Get_Longitude(data_gps2.longitude_str,data_gps2.count_lon,data_gps2.orientation[1]);
			GPS_Copy_time(data_gps2.time,time_gps_2,data_gps2.count_time);
			count_t2 = data_gps2.count_time;
			flag_gps2 = 1;
		}
	}	

/*-------------------------------- GPS 3 ------------------------------------*/
		
	if(UART_available(&serial_3)){
		c3 = UART_Read(&serial_3);
		finish3 = GPS_Store(&data_gps3,c3);
		if(finish3){
			latitude3 = GPS_Get_Latitude(data_gps3.latitude_str,data_gps3.count_lat,data_gps3.orientation[0]);
			longitude3 = GPS_Get_Longitude(data_gps3.longitude_str,data_gps3.count_lon,data_gps3.orientation[1]);
			GPS_Copy_time(data_gps3.time,time_gps_3,data_gps3.count_time);
			count_t3 = data_gps3.count_time;
			flag_gps3 = 1;
		}
	}

/*-------------------------------- Parte 2 ---------------------------------*/
	if(finish_timeout(&tm_out) || (flag_gps1&&flag_gps2&&flag_gps3)){
		if(flag_gps1)
			count_gps++;
		if(flag_gps2)
			count_gps++;
		if(flag_gps3)
			count_gps++;
			
		bno.getEvent(&event); 
		als = AP3216_getAmbientLight(luxRange);
		magnetic = bno.getVector(Adafruit_BNO055::VECTOR_MAGNETOMETER);
		north_angle = atan2(magnetic.y(),magnetic.x());
		north_angle = north_angle*(180/PI);
		north_angle = north_angle - MAGNETIC_DECLINATION;
		
		if (north_angle < 0)
			north_angle = north_angle + 360;
		
		
		UART_Write(count_gps,0,&USART0_Transmit);
		USART0_Transmit(44);
		
		if(flag_gps1){
			UART_Write_array(time_gps_1,count_t1,&USART0_Transmit);
			USART0_Transmit(44);
			UART_Write(latitude1,6,&USART0_Transmit);
			USART0_Transmit(44);
			UART_Write(longitude1,6,&USART0_Transmit);
			USART0_Transmit(44);
			
		}
		
		if(flag_gps2){
			if(!flag_gps1){
				UART_Write_array(time_gps_2,count_t2,&USART0_Transmit);
				USART0_Transmit(44);
			}
			UART_Write(latitude2,6,&USART0_Transmit);
			USART0_Transmit(44);
			UART_Write(longitude2,6,&USART0_Transmit);
			USART0_Transmit(44);
			
		}
		
		if(flag_gps3){
			if(!flag_gps1 && !flag_gps2){
				UART_Write_array(time_gps_3,count_t3,&USART0_Transmit);
				USART0_Transmit(44);
			}
			UART_Write(latitude3,6,&USART0_Transmit);
			USART0_Transmit(44);
			UART_Write(longitude3,6,&USART0_Transmit);
			USART0_Transmit(44);
			
		}
		
		UART_Write(event.orientation.x,2,&USART0_Transmit);
		USART0_Transmit(44);
		UART_Write(event.orientation.y,2,&USART0_Transmit);
		USART0_Transmit(44);
		UART_Write(event.orientation.z,2,&USART0_Transmit);
		USART0_Transmit(44);
		UART_Write(north_angle,0,&USART0_Transmit);
		USART0_Transmit(44);
		UART_Write(als,2,&USART0_Transmit);
		USART0_Transmit('\n');
		USART0_Transmit('\r');

		Restart_Timeout(&tm_out);
		count_gps = 0;
		flag_gps1 = 0;
		flag_gps2 = 0;
		flag_gps3 = 0;
	}
	
}


/*FN****  Función de atención a la interrupcion  del puerto uart 0 ************/

ISR(USART0_RX_vect){
	RX_0 = UDR0;
	UART_Store(&serial_0,RX_0); /* almacena el dato recibido */
}

/*FN****  Función de atención a la interrupcion  del puerto uart 1 ************/

ISR(USART1_RX_vect){
	RX_1 = UDR1;
	UART_Store(&serial_1,RX_1); /* almacena el dato recibido */
}

/*FN****  Función de atención a la interrupcion  del puerto uart 2 ************/

ISR(USART2_RX_vect){
	RX_2 = UDR2;
	UART_Store(&serial_2,RX_2); /* almacena el dato recibido */
}

/*FN****  Función de atención a la interrupcion  del puerto uart 3 ************/

ISR(USART3_RX_vect){
	RX_3 = UDR3;
	UART_Store(&serial_3,RX_3); /* almacena el dato recibido */
}

/*FN********  Función de atención a la interrupcion  del timer 1 **************/

ISR(TIMER1_COMPA_vect) {
	Update_timeout(&tm_out); /* actualiza el conteo del timeout */	
}