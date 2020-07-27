#ifndef GPS_H_
#define GPS_H_

/**************************** Definción de tipos ******************************/

typedef struct DATA_GPS_T DATA_GPS_T;
struct DATA_GPS_T{
	unsigned char longitude_str[15];
	unsigned char latitude_str[15];
	unsigned char time[15];
	unsigned char orientation[2];
	int count_lon;
	int count_lat;
	int count_time;
	int state_machine;
};

/* ---------------------------- Funciones  ------------------------------- */

int GPS_Store(DATA_GPS_T *gps, unsigned char c);
float GPS_Get_Longitude(unsigned char *longitude_str,int count_lon, unsigned char orientation );
float GPS_Get_Latitude( unsigned  char *latitude_str,int count_lat, unsigned char orientation );
void GPS_Copy_time(unsigned char *time_str,unsigned char *time_cpy,int size_cpy);
void GPS_Set_Up(void (*fun_prt_transmit)(unsigned char),void (*fun_prt_init)(unsigned int));

#endif /* GPS_H_ */