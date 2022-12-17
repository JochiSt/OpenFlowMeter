#ifndef __I2C_UTILS_H__
#define __I2C_UTILS_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "stm32f1xx_hal.h"

void i2c_init_TMP100(I2C_HandleTypeDef* i2cHandle, uint8_t TMP100_addr);
uint16_t i2c_read_TMP100(I2C_HandleTypeDef* i2cHandle, uint8_t TMP100_addr);

#ifdef __cplusplus
}
#endif

#endif /* __I2C_UTILS_H__ */
