#ifndef __EEPROM_CFG_H__
#define __EEPROM_CFG_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "stm32f1xx_hal.h"
#include "config.h"

void read_EEPROM_cfg(I2C_HandleTypeDef* i2cHandle, config_t *cfg, const config_t *default_cfg);
void write_EEPROM_cfg(I2C_HandleTypeDef* i2cHandle, config_t *cfg);

#ifdef __cplusplus
}
#endif

#endif /* __EEPROM_CFG_H__ */
