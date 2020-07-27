/* Ruler 1         2         3         4         5         6         7        */
/******************************************************************************/
/*                                                                            */
/* 							   Timeout.c                                      */
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

/********************************  Timeout.c  *********************************/
/*                                                                            */
/*   Proposito: Generar un timeout para evitar quedarse en un estado de forma */
/*   infinita cuando se pierde la conexión con algun modulo GPS               */
/*                                                                            */
/*                                                                            */
/*   -----------------------------------------------------------------------  */
/*    Junio 1/20               Implementación inicial                         */
/*                                                                            */

/********************************** Headers ***********************************/

#include "Timeout.h"

/*****************************  Funciones  **************************************/

/*FN****************************************************************************
*
*	void Start_Timeout(TIMEOUT_T *timeout -> Apuntador a la variable que almacena 
*                      los parametros del timeout
*                      int time -> Numero de pulsos a contar 
*					   )
*
*   Retorna: No retorna nada la variable que guarda los parametros del timeut 
*			 pasa por referencia.
*
*   Funcionamiento: Se define la cantidad de pulsos que se quieren contar 
*					y se reinicia el contador 
*
*   -----------------------------------------------------------------------
*   Junio 1/20               Implementación inicial
*
*******************************************************************************/

void Start_Timeout(TIMEOUT_T *timeout, int time){
	timeout->flagStart = 1;
	timeout->flagTimeout = 0;
	timeout->timeout = time;
	timeout->count = 0;
}



/*FN****************************************************************************
*
*	void Restart_Timeout(TIMEOUT_T *timeout -> Apuntador a la variable que almacena
*                      los parametros del timeout
*					   )
*
*   Retorna: No retorna nada la variable que guarda los parametros del timeut
*			 pasa por referencia.
*
*   Funcionamiento: Reinicia el timeout
*
*   -----------------------------------------------------------------------
*   Junio 1/20               Implementación inicial
*
*******************************************************************************/

void Restart_Timeout(TIMEOUT_T *timeout){
	timeout->flagStart = 1;
	timeout->flagTimeout = 0;
	timeout->count = 0;
}


/*FN****************************************************************************
*
*	void Update_timeout(TIMEOUT_T *timeout -> Apuntador a la variable que almacena
*                      los parametros del timeout
*					   )
*
*   Retorna: No retorna nada la variable que guarda los parametros del timeut
*			 pasa por referencia.
*
*   Funcionamiento: Cuando se llama esta función si el contador es menor al
*                   timeout aumenta el contador si no la bandera de que 
*                   indica cuando se ha terminado un conteo es activada
*
*
*   -----------------------------------------------------------------------
*   Junio 1/20               Implementación inicial
*
*******************************************************************************/

void Update_timeout(TIMEOUT_T *timeout){
	if(timeout->flagStart){
		if( timeout->count < timeout->timeout){
			timeout->count++;
		}else{
			timeout->flagTimeout = 1;
			timeout->flagStart = 0;
		}
	}
}

/*FN****************************************************************************
*
*	char finish_timeout(TIMEOUT_T *timeout -> Apuntador a la variable que almacena
*                      los parametros del timeout
*					   )
*
*   Retorna: Retorna el estado de la bandera que indica si hubo o no timeout
*
*
*   -----------------------------------------------------------------------
*   Junio 1/20               Implementación inicial
*
*******************************************************************************/

char finish_timeout(TIMEOUT_T *timeout){
	return timeout->flagTimeout;
}