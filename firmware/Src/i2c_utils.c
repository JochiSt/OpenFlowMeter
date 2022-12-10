#include <stdio.h>
#include "i2c_utils.h"

/**
 *
 */
uint8_t write16_EEPROM(I2C_HandleTypeDef* i2cHandle, uint8_t i2c_addr, uint8_t addr, uint16_t value){
  // store a 16 bit number in the EEPROM

  return 0x00;
}

/**
 *
 */
uint8_t read16_EEPROM(I2C_HandleTypeDef* i2cHandle, uint8_t i2c_addr, uint8_t addr){
  // read a 16 bit number from the EEPROM

  return 0x00;
}


/**
 * init the temperature sensor
 */
void i2c_init_TMP100(I2C_HandleTypeDef* i2cHandle, uint8_t addr){
  printf("Init TMP100\r\n");
  // set the resolution of the TMP100

}
/**
 * read the I2C temperature sensor
 * @param i2cHandle
 * @param TMP100_addr
 * @return raw temperature
 */
uint16_t i2c_read_TMP100(I2C_HandleTypeDef* i2cHandle, uint8_t TMP100_addr){
  printf("Reading TMP100\r\n");

  uint8_t buf[12];  // buffer for sending and receiving I2C data
  int16_t val = 0xFFFF;
  HAL_StatusTypeDef result;
  // Tell TMP100 that we want to read from the temperature register
  buf[0] = 0x00;

  result = HAL_I2C_Master_Transmit(i2cHandle, TMP100_addr, buf, 1, HAL_MAX_DELAY);
  if ( result == HAL_OK ) {
    // Read 2 bytes from the temperature register
    result = HAL_I2C_Master_Receive(i2cHandle, TMP100_addr, buf, 2, HAL_MAX_DELAY);
    if ( result != HAL_OK ) {
      printf("Error TMP100 RX\r\n");
    } else {

      //Combine the bytes
      val = ((int16_t)buf[0] << 4) | (buf[1] >> 4);

      // Convert to 2's complement, since temperature can be negative
      if ( val > 0x7FF ) {
        val |= 0xF000;
      }

      // Convert to float temperature value (Celsius)
      float temp_c = val * 0.0625;

      // Convert temperature to decimal format
      temp_c *= 100;
      printf("%u.%u C\r\n", ((unsigned int)temp_c / 100),
                                ((unsigned int)temp_c % 100));
    }
  }else{
    printf("Error TMP100 TX\r\n");
  }
  return val;
}
