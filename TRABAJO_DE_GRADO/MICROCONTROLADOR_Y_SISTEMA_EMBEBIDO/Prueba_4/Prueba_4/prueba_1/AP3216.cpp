/* Ruler 1         2         3         4         5         6         7        */
/******************************************************************************/
/*                                                                            */
/* 							   AP3216.C                                       */
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

/********************************  Ap3216.c   *********************************/
/*                                                                            */
/*   Proposito: Obtener la magnitud en Lux de la luz ambiente                 */
/*                                                                            */
/*                                                                            */
/*   -----------------------------------------------------------------------  */
/*   Mayo 4/20               Implementación Inicial                           */
/*                                                                            */

/********************************** Headers ***********************************/

/*------------------------------ headers standard ----------------------------*/

#include <inttypes.h>

/*------------------------------ headers arduino -----------------------------*/
#include <Wire.h>

/*------------------------------ otros headers   -----------------------------*/

#include "AP3216.h"

/*FN****************************************************************************
*
*	uint8_t AP3216_Read(uint8_t Address -> dirección del dispositivo 
*                       uint8_t Register -> Registro a leer
*                      )
*
*   Retorna: Retorna el valor almacenado en un registro del sensor AP3216
*
*   Funcionamiento: Lee por I2C el valor almacenado en un determinado registro 
*					del sensor AP3216
*
*   -----------------------------------------------------------------------
*   Mayo 4/20               Initial implementation
*
*******************************************************************************/

uint8_t AP3216_Read(uint8_t Address, uint8_t Register)
{
	uint8_t Data = 0;
	Wire.beginTransmission(Address);
	Wire.write(Register);
	Wire.endTransmission();
	Wire.requestFrom(Address, 1);
	Data = Wire.read();
	return Data;
}

/*FN****************************************************************************
*
*	void AP3216_Write(uint8_t Address -> dirección del dispositivo 
*                     uint8_t Register -> Registro a escribir 
*                     uint8_t Data -> Byte a escribir 
*                    )
*
*   Retorna: No retorna nada
*
*   Funcionamiento: Escribe por I2C un byte en un registro del sensor de luz
*
*   -----------------------------------------------------------------------
*   Mayo 4/20               Initial implementation
*
*******************************************************************************/

void AP3216_Write(uint8_t Address, uint8_t Register, uint8_t Data)
{
	Wire.beginTransmission(Address);
	Wire.write(Register);
	Wire.write(Data);
	Wire.endTransmission();
}

/*FN****************************************************************************
*
*	void AP3216_setLuxRange(LUX_RANGE_T luxRange -> Rango seleccionado
*		            )
*
*   Retorna: no retorna nada
*
*   Funcionamiento: Configura el rango de lux seleccionado
*
*   -----------------------------------------------------------------------
*   Mayo 4/20               Initial implementation
*
*******************************************************************************/

void AP3216_setLuxRange(LUX_RANGE_T luxRange){
	uint8_t alsConfigReg;
	alsConfigReg = AP3216_Read(AP3216_ADDR, ALS_DATA_LOW_REG);
	alsConfigReg &= 0b11001111;
	alsConfigReg |= luxRange;
	AP3216_Write(AP3216_ADDR,ALS_CONFIG_REG, alsConfigReg);
}

/*FN****************************************************************************
*
*	void AP3216_setMode(MODE_T deviceMode -> Modo de operación
*		               )
*
*   Retorna: no retorna nada
*
*   Funcionamiento: Configura el modo de operación seleccionado
*
*   -----------------------------------------------------------------------
*   Mayo 4/20               Initial implementation
*
*******************************************************************************/

void AP3216_setMode(MODE_T deviceMode){
	AP3216_Write(AP3216_ADDR,SYSTEM_CONFIGURATION_REG, deviceMode);
}


/*FN****************************************************************************
*
*	void AP3216_init(LUX_RANGE_T luxRange -> Rango seleccionado
*					 MODE_T mode -> Modo de operación seleccionado
*		            )
*
*   Retorna: no retorna nada
*
*   Funcionamiento: Configura el rango de lux y modo de operación seleccionado
*
*   -----------------------------------------------------------------------
*   Mayo 4/20               Initial implementation
*
*******************************************************************************/

void AP3216_init(LUX_RANGE_T luxRange,MODE_T mode){
	AP3216_setMode(RESET);
	AP3216_setMode(mode);
	AP3216_setLuxRange(luxRange);
}

/*FN****************************************************************************
*
*	uint16_t AP3216_getALSData()
*
*   Retorna: Retorna el valor de la luz ambiente cuantizado a 16bits
*
*   Funcionamiento: Recibe dos bytes correspondiente a la medida y retorna un
*					entero sin signo de 16 bits
*
*   -----------------------------------------------------------------------
*   Mayo 4/20               Initial implementation
*
*******************************************************************************/

uint16_t AP3216_getALSData(){
	uint8_t low_als, high_als;
	uint16_t als = 0x0000;
	low_als = AP3216_Read(AP3216_ADDR, ALS_DATA_LOW_REG);
	high_als = AP3216_Read(AP3216_ADDR, ALS_DATA_HIGH_REG);
	als = (high_als<<8) + low_als;
	return als;
}

/*FN****************************************************************************
*
*	float AP3216_getAmbientLight(LUX_RANGE_T luxRange -> Rango de lux seleccionado
*								)
*
*   Retorna: Retorna el valor de la luz ambiente en lux
*
*   Funcionamiento: multiplica la medida por el factor de escala de acuerdo al
*					rango seleccionado.
*
*   -----------------------------------------------------------------------
*   Mayo 4/20               Initial implementation
*
*******************************************************************************/

float AP3216_getAmbientLight(LUX_RANGE_T luxRange){
	uint16_t rawALS = 0;
	rawALS = AP3216_getALSData();
	float als=0;
	
	switch(luxRange){
		case RANGE_20661:
		als = 0.35 * rawALS;
		break;
		case RANGE_5162:
		als = 0.0788 * rawALS;
		break;
		case RANGE_1291:
		als = 0.0197 * rawALS;
		break;
		case RANGE_323:
		als = 0.0049 * rawALS;
		break;
		default:
		als = 0.35 * rawALS;
		break;
	}
	return als;
}