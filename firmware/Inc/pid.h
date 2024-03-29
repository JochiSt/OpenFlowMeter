#ifndef __PID_H__
#define __PID_H__

#include <stdbool.h>
#include <stdint.h>

typedef struct {
    float PID_T;  ///< temperature setpoint
    float PID_P;  ///< proportional part
    float PID_I;  ///< integral part
    float PID_D;  ///< differential part
} PID_config_t;

typedef struct {
    bool active;

    PID_config_t* PIDcfg;

    float* input;
    uint16_t* output;

    float errorInt;
    float lastError;
} PID;

extern PID pid[2];

void runPID(PID* pid);

#endif //__PID_H__
