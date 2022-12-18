#ifndef __PID_H__
#define __PID_H__

#include <stdbool.h>
#include <stdint.h>

typedef struct {
    uint8_t PID_T;  ///< temperature setpoint
    uint8_t PID_P;  ///< proportional part
    uint8_t PID_I;  ///< integral part
    uint8_t PID_D;  ///< differential part
} PID_config_t;

typedef struct {
    bool active;
    PID_config_t* PIDcfg;
    float* input;
    float* setpoint;
} PID;

extern PID pid0;
extern PID pid1;

#endif //__PID_H__
