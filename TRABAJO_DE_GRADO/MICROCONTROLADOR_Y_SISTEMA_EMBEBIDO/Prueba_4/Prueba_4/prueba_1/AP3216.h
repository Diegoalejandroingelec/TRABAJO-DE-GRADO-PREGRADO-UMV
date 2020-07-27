#ifndef AP3216_H_
#define AP3216_H_

/********************************** Headers ***********************************/

/*------------------------------ headers standard ----------------------------*/

#include <inttypes.h>

/**************************** Constantes simbólicas  **************************/

#define AP3216_ADDR                   0x1E
#define ALS_CONFIG_REG                0x10
#define ALS_DATA_LOW_REG              0x0C
#define ALS_DATA_HIGH_REG             0x0D
#define SYSTEM_CONFIGURATION_REG      0x00

/************************** Definción de tipos *******************************/

typedef enum {
	POWER_DOWN,   
	ALS,
	PS,
	ALS_PS,
	RESET,
	ALS_ONCE,
	PS_ONCE,
	ALS_PS_ONCE
} MODE_T;

typedef enum {
	RANGE_20661 = 0b00000000,
	RANGE_5162  = 0b00010000,
	RANGE_1291  = 0b00100000,
	RANGE_323 = 0b00110000
}LUX_RANGE_T;

/* ---------------------------- Funciones  ------------------------------- */

uint8_t AP3216_Read(uint8_t Address, uint8_t Register);
void AP3216_Write(uint8_t Address, uint8_t Register, uint8_t Data);
void AP3216_setLuxRange(LUX_RANGE_T luxRange);
void AP3216_setMode(MODE_T deviceMode);
void AP3216_init(LUX_RANGE_T luxRange,MODE_T mode);
uint16_t AP3216_getALSData();
float AP3216_getAmbientLight(LUX_RANGE_T luxRange);

#endif /* AP3216_H_ */