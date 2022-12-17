
#include "eeprom_cfg.h"
#include "i2c_utils.h"    // access to I2C EEPROM

/**
 * @brief read config from EEPROM
 * @param cfg config, which will be modified
 * @param default_cfg default config, which will be used, in case the EEPROM
 *  config is invalid / not available
 */
void read_EEPROM_cfg(config_t *cfg, const config_t *default_cfg){
  *cfg = *default_cfg;
}


