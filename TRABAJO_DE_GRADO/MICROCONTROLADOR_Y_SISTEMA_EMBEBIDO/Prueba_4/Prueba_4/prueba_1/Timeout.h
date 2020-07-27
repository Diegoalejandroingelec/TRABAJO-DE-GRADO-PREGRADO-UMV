#ifndef TIMEOUT_H_
#define TIMEOUT_H_

/**************************** Definción de tipos ******************************/

typedef struct TIMEOUT_T TIMEOUT_T;
struct TIMEOUT_T{
	char flagTimeout;
	char flagStart;
	int count;
	int timeout;
};

/* ---------------------------- Funciones  ------------------------------- */

void Start_Timeout(TIMEOUT_T *timeout, int time);
void Restart_Timeout(TIMEOUT_T *timeout);
void Update_timeout(TIMEOUT_T *timeout);
char finish_timeout(TIMEOUT_T *timeout);



#endif /* TIMEOUT_H_ */