%module timestr
%{
#define SWIG_FILE_WITH_INIT
#include<time.h>
#include <stdarg.h>  
#include <sys/time.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
extern char t_data_time_buffer[64];
extern char * GetDateTimeStr();
%}
char t_data_time_buffer[64];
char * GetDateTimeStr();