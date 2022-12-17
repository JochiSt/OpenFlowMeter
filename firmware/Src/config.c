
#include <stdio.h>

#include "eeprom_cfg.h"
#include "config.h"

config_t default_cfg;
config_t cfg;

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
  cfg->PID0.PID_T = 40;
  cfg->PID0.PID_P = 0;
  cfg->PID0.PID_I = 0;
  cfg->PID0.PID_D = 0;

  cfg->PID1.PID_T = 40;
  cfg->PID1.PID_P = 0;
  cfg->PID1.PID_I = 0;
  cfg->PID1.PID_D = 0;

  cfg->PID_flags.PID0_active = 0;
  cfg->PID_flags.PID1_active = 0;

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

  /*
  // set the PID
  cfg->PID0.PID_T
  cfg->PID0.PID_P
  cfg->PID0.PID_I
  cfg->PID0.PID_D

  cfg->PID1.PID_T
  cfg->PID1.PID_P
  cfg->PID1.PID_I
  cfg->PID1.PID_D

  cfg->PID_flags.PID0_active
  cfg->PID_flags.PID1_active
  */
}
