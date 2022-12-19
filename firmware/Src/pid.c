#include "pid.h"

PID pid0;
PID pid1;

const uint16_t MAX_PID_OUTPUT = 1023;
const uint16_t MIN_PID_OUTPUT = 0;

void runPID(PID* pid){
  if(pid->active){
    float error = pid->PIDcfg->PID_T - *pid->input;
    pid->errorInt += error;

    // do the PID calculations
    float output = 0;
    output += pid->PIDcfg->PID_P * error;
    output += pid->PIDcfg->PID_I * pid->errorInt;
    output += pid->PIDcfg->PID_D * (error - pid->lastError);

    output += (float)*pid->output;

    pid->lastError = error;

    if( output > MAX_PID_OUTPUT){
      output = MAX_PID_OUTPUT;
    }
    if( output < MIN_PID_OUTPUT){
      output = MIN_PID_OUTPUT;
    }

    *pid->output = (uint16_t) output;
  }else{
    // TODO implement some default output, which is used, when the PIC is not
    // operating
  }
}
