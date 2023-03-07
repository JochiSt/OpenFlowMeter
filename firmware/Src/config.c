
#include <stdio.h>

#include "eeprom_cfg.h"
#include "config.h"

config_t default_cfg;
config_t cfg;

const float LSB2U = 3.3 / 4096;
const float LSB2I = 3.3 / 4096 * 10e-3;

const float U2I = 10e-3;  // TODO insert right value here

void generateDefaultCFG(config_t *cfg){
  // set the board ID
  cfg->board_ID = 1;

  // set the rates
  cfg->interval_CAN_ADC = (500/125);
  cfg->interval_PRINT_UART = (1000/125);

  cfg->interval_I2C_TMP100 = (2000/125);
  cfg->interval_I2C_BME680 = 255;

  // set the smoothing
  cfg->SMOO = 15;
  cfg->SMOO_MAX = 16;

  // set the PID
  cfg->PID[0].PID_T = 40;
  cfg->PID[0].PID_P = 0;
  cfg->PID[0].PID_I = 0;
  cfg->PID[0].PID_D = 0;

  cfg->PID[1].PID_T = 40;
  cfg->PID[1].PID_P = 0;
  cfg->PID[1].PID_I = 0;
  cfg->PID[1].PID_D = 0;

  cfg->PID_flags.PID0_active = 0;
  cfg->PID_flags.PID1_active = 0;

#if defined(PCB_V2)
  // gain settings from calculations / optimisation
  cfg->GAIN[0].Igain = 1 + 47.0e3 / 5.6e3;
  cfg->GAIN[0].Ugain = 1 + 33.0e3 / 5.6e3;
  cfg->GAIN[0].Ibias = 0.12;
  cfg->GAIN[0].Ubias = 0.01;

  cfg->GAIN[1].Igain = 1 + 47.0e3 / 5.6e3;
  cfg->GAIN[1].Ugain = 1 + 33.0e3 / 5.6e3;
  cfg->GAIN[1].Ibias = 0.12;
  cfg->GAIN[1].Ubias = 0.01;
#endif
#if defined(PCB_V3)
  for(int i=0; i<2; i++){
    cfg->U_R1[i] = 47e3;
    cfg->U_R2[i] = 5.6e3;
    cfg->I_R1[i] = 47e3;
    cfg->I_R2[i] = 5.6e3;
  }
#endif

}

/**
 * print the configuration to UART
 */
void printCfg(config_t *cfg){

  printf("BoardID %d\r\n", cfg->board_ID);

  printf("Intervals:\r\n");
  printf("CANADC   %d\r\n", cfg->interval_CAN_ADC);
  printf("UART     %d\r\n", cfg->interval_PRINT_UART);
  printf("I2C:\r\n");
  printf("  TMP100 %d\r\n",cfg->interval_I2C_TMP100);
  printf("  BME680 %d\r\n",cfg->interval_I2C_BME680);

  printf("\r\n");
  printf("SMOO:    %d\r\n", cfg->SMOO);
  printf("SMOOMAX: %d\r\n", cfg->SMOO_MAX);

#if defined(PCB_V2)
  printf("\r\n");
  printf("Gain:");
  printf("  CH0 I %f U%f\r\n", cfg->GAIN[0].Igain, cfg->GAIN[0].Ugain);
  printf("  CH1 I %f U%f\r\n", cfg->GAIN[1].Igain, cfg->GAIN[1].Ugain);
  printf("Offset:");
  printf("  CH0 I %f U%f\r\n", cfg->GAIN[0].Ibias, cfg->GAIN[0].Ubias);
  printf("  CH1 I %f U%f\r\n", cfg->GAIN[1].Ibias, cfg->GAIN[1].Ubias);
#endif
#if defined(PCB_V3)
  printf("\r\n");
  printf("Resistors:\r\n");
  for(int i=0; i<2; i++){
    printf("  U R1 %f R2 %f\r\n", cfg->U_R1[i], cfg->U_R2[i]);
    printf("  I R1 %f R2 %f\r\n", cfg->I_R1[i], cfg->I_R2[i]);
  }
#endif

  printf("\r\n");
  printf("PID 0: (%d)\r\n", cfg->PID_flags.PID0_active);
  printf("  T %f\r\n", cfg->PID[0].PID_T);
  printf("  P %f\r\n", cfg->PID[0].PID_P);
  printf("  I %f\r\n", cfg->PID[0].PID_I);
  printf("  D %f\r\n", cfg->PID[0].PID_D);

  printf("PID 1: (%d)\r\n", cfg->PID_flags.PID1_active);
  printf("  T %f\r\n", cfg->PID[1].PID_T);
  printf("  P %f\r\n", cfg->PID[1].PID_P);
  printf("  I %f\r\n", cfg->PID[1].PID_I);
  printf("  D %f\r\n", cfg->PID[1].PID_D);

}
