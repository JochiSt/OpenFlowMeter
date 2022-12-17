
#include "eeprom_cfg.h"
#include "config.h"

config_t default_cfg;
config_t cfg;

void generateDefaultCFG(){

  // set the board ID
  default_cfg.board_ID = 1;

  // set the rates
  default_cfg.interval_OFM_report = 4;
  default_cfg.interval_OFM_PID = 2;

  default_cfg.interval_TMP100 = 8;
  default_cfg.interval_BME680 = 255;

  // set the smoothing
  default_cfg.SMOO = 15;
  default_cfg.SMOO_MAX = 16;

  // set the PID
  default_cfg.PID0.PID_T = 40;
  default_cfg.PID0.PID_P = 0;
  default_cfg.PID0.PID_I = 0;
  default_cfg.PID0.PID_D = 0;

  default_cfg.PID1.PID_T = 40;
  default_cfg.PID1.PID_P = 0;
  default_cfg.PID1.PID_I = 0;
  default_cfg.PID1.PID_D = 0;

  default_cfg.PID_flags.PID0_active = 0;
  default_cfg.PID_flags.PID1_active = 0;

}



