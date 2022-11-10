/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __I2C_SCANNER_H__
#define __I2C_SCANNER_H__

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/

/* USER CODE BEGIN Includes */
#include "stm32f1xx_hal.h"

/* USER CODE END Includes */


/* USER CODE BEGIN Private defines */

/* USER CODE END Private defines */

void i2c_scan(I2C_HandleTypeDef* i2cHandle);

/* USER CODE BEGIN Prototypes */

/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __I2C_SCANNER_H__ */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
