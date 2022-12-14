/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __I2C_UTILS_H__
#define __I2C_UTILS_H__

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/

/* USER CODE BEGIN Includes */
#include "stm32f1xx_hal.h"

/* USER CODE END Includes */


/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */


/* USER CODE BEGIN Prototypes */
void i2c_init_TMP100(I2C_HandleTypeDef* i2cHandle, uint8_t TMP100_addr);
uint16_t i2c_read_TMP100(I2C_HandleTypeDef* i2cHandle, uint8_t TMP100_addr);

/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __I2C_UTILS_H__ */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/