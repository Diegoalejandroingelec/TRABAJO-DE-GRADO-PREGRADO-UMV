#ifndef UART_ATMEGA2560
#define UART_ATMEGA2560

/**************************** Constantes simbólicas  **************************/

#define MAX_BUFFER 1000
#define MAX_BUFFER_TX 10

/************************** Definción de tipos *******************************/

typedef struct SERIAL_T SERIAL_T;
struct SERIAL_T {
	int count;
	int count_input;
	int count_output;
	char *output;
	char *input;
};

/* ---------------------------- Functions  ------------------------------- */

void UART_Begin(SERIAL_T *serial, char *buffer_rx,void (*fun_prt)(unsigned int),unsigned int ubrr);
void UART_Store(SERIAL_T *serial,char data);
int  UART_available(SERIAL_T *serial);
char UART_Read(SERIAL_T *serial);
void Num_to_str(float num, char *str,int *digits,int n);
void UART_Write(float num,int n,void (*fun_prt)(unsigned char));
void UART_Write_array(unsigned char *array, int size_array,void (*fun_prt)(unsigned char));

#endif