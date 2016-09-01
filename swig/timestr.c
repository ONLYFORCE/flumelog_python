#include<time.h>
#include <stdarg.h>  
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

char t_data_time_buffer[64];
 char * GetDateTime( )
{
#ifdef  WIN32

	SYSTEMTIME sysTime;
	GetLocalTime(&sysTime);
	snprintf(t_data_time_buffer, 63,
		"%04d-%02d-%02d %02d:%02d:%02d",
		sysTime.wYear, sysTime.wMonth, sysTime.wDay, sysTime.wHour, sysTime.wMinute, sysTime.wSecond);

#else

	time_t tTime;
	struct tm stTime;

	tTime = time(NULL);
	localtime_r(&tTime, &stTime);

	int32_t iYear = stTime.tm_year + 1900;
	int32_t iMonth = stTime.tm_mon + 1;
	int32_t iDay = stTime.tm_mday;
	int32_t iHour = stTime.tm_hour;
	int32_t iMinute = stTime.tm_min;
	int32_t iSecond = stTime.tm_sec;

	snprintf(t_data_time_buffer, 63,
		"%04d-%02d-%02d %02d:%02d:%02d", iYear, iMonth, iDay, iHour, iMinute, iSecond);

#endif

	return t_data_time_buffer;




}