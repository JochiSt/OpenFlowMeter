
#include "eeprom_cfg.h"
#include "i2c_utils.h"    // access to I2C EEPROM

#include <stdio.h>
#include <stdint.h>

/**
 * @brief read config from EEPROM
 * @param i2cHandle I2C handler
 * @param cfg config, which will be modified
 * @param default_cfg default config, which will be used, in case the EEPROM
 *  config is invalid / not available
 */
void read_EEPROM_cfg(I2C_HandleTypeDef* i2cHandle, config_t *cfg, const config_t *default_cfg){
  // access the configuration via uint8_t pointer
  uint8_t *ptr = (uint8_t*)cfg;
  uint8_t *dptr = (uint8_t*)default_cfg;

  uint8_t addr; // address inside the EEPROM
  uint8_t eeprom_content;
  for(addr=0; addr<sizeof(config_t); addr++){
    eeprom_content = read8_EEPROM(i2cHandle, 0x50, addr);
    if( eeprom_content == 0xFF){
      ptr[addr] = dptr[addr];
    }else{
      ptr[addr] = eeprom_content;
    }
  }
}

/**
 * @brief write config ro EEPROM
 * @param i2cHandle I2C handler
 * @param cfg config, which will be written into EEPROM
 */
void write_EEPROM_cfg(I2C_HandleTypeDef* i2cHandle, config_t *cfg){
  // access the configuration via uint8_t pointer
  uint8_t *ptr = (uint8_t*)cfg;

  uint8_t ret = 0;
  uint8_t addr; // address inside the EEPROM
  for(addr=0; addr<sizeof(config_t); addr++){
    ret = write8_EEPROM(i2cHandle, 0x50, addr, ptr[addr]);
    if(ret != 0){
      printf("ERROR while writing config\r\n");
    }
  }
}


