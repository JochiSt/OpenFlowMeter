#ifndef __I2C_SCANNER_H__
#define __I2C_SCANNER_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "stm32f1xx_hal.h"

void i2c_scan(I2C_HandleTypeDef* i2cHandle);

#ifdef __cplusplus
}
#endif

#endif /* __I2C_SCANNER_H__ */
