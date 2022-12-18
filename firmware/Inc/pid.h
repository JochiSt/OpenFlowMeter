#ifndef __PID_H__
#define __PID_H__

#include <stdbool.h>
#include <stdint.h>

typedef struct {
    bool active;
    PID_config_t* PIDcfg;
    float* input;
    float* setpoint;
} PID;

extern PID pid0;
extern PID pid1;

#endif //__PID_H__
