#include "pid.h"
#include <stdio.h>

PID pid0;
PID pid1;

const uint16_t MAX_PID_OUTPUT = (512<<2);  //TODO just for debugging purpose can be
                                      // increased to fullscale
const uint16_t MIN_PID_OUTPUT = (0x0A<<2); // a minimal current is needed to measure
                                      // the resistance.

//#define PID_DEBUG_PRINTF

void runPID(PID* pid){
  if(pid->active){
    float error = pid->PIDcfg->PID_T - *pid->input;
    //pid->errorInt = pint->errorInt * 0.9 + 0.1 * error;
    pid->errorInt += error;

    // do the PID calculations
    float output = 0;
    float P_term = pid->PIDcfg->PID_P * error;
    float I_term = pid->PIDcfg->PID_I * pid->errorInt;
    float D_term = pid->PIDcfg->PID_D * (error - pid->lastError);

    output += P_term;
    output += I_term;
    output += D_term;
    output += (float)*pid->output;

#ifdef PID_DEBUG_PRINTF
    printf("PID error  %f\r\n", error);
    printf("   in %f", *pid->input);
    printf("    P %f - I %f - D %f\r\n", P_term, I_term, D_term);
    printf("PID sum    %f\r\n", output);
#endif

    pid->lastError = error;

    if( output > MAX_PID_OUTPUT){
      output = MAX_PID_OUTPUT;
    }
    if( output < MIN_PID_OUTPUT){
      output = MIN_PID_OUTPUT;
    }

#ifdef PID_DEBUG_PRINTF
    printf("PID output %f\r\n", output);
#endif

    *pid->output = (uint16_t) output;
  }else{
    // TODO implement some default output, which is used, when the PID is not
    // operating
    *pid->output = MIN_PID_OUTPUT;
  }
}
