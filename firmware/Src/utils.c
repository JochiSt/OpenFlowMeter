
#include "utils.h"

uint8_t upper(uint16_t val){
	return (val >> 8) & 0xFF;
};
uint8_t lower(uint16_t val){
	return (val & 0xFF);
};


