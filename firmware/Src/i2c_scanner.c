
#include <stdio.h>
#include "i2c_scanner.h"

/**
 * I2C Scanner on the specified handle
 * \param i2cHandle Handle of the I2C Bus, which should be scanned.
 */
void i2c_scan(I2C_HandleTypeDef* i2cHandle){
  // function for simple I2C scanner
  
  if(i2cHandle->Instance==I2C1){
    printf("I2C bus #1\r\n");    
  }else if(i2cHandle->Instance==I2C2){
    printf("I2C bus #2\r\n");
  }
  
  printf("Scanning I2C bus:\r\n");
  HAL_StatusTypeDef result;
  uint8_t i;
  for (i=1; i<128; i++){
    /*
 	 * the HAL wants a left aligned i2c address
 	 * (uint16_t)(i<<1) is the i2c address left aligned
 	 * retries 2
 	 * timeout 2
 	 */
 	result = HAL_I2C_IsDeviceReady(i2cHandle, (uint16_t)(i<<1), 2, 2);
 	if (result != HAL_OK) // HAL_ERROR or HAL_BUSY or HAL_TIMEOUT
 	{
      printf("."); // No ACK received at that address
    }
 	if (result == HAL_OK)
 	{
      printf("0x%X", i); // Received an ACK at that address
    }
  }
  printf("\r\n");
}