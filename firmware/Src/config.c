
#include "config.h"

const uint8_t SMOO = 15;      // averaging factor
                              // gives the number of old samples
                              // SMOO_MAX - SMOO is number of new samples
                              // VAL = (val * (SMOO_MAX - SMOO) + Previous_value * SMOO) / SMOO_MAX
const uint8_t SMOO_MAX = 16;  // Maximal value of SMOO


