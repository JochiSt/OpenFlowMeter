#include <stdio.h>
#include "i2c_utils.h"
#include "utils.h"

//#define TMP100_DEBUG

/**
 *
 */
uint8_t write8_EEPROM(I2C_HandleTypeDef* i2cHandle, uint8_t EEPROM_addr, uint8_t addr, uint8_t value){
  // store a 8bit number in the EEPROM
  uint8_t buf[2] = {0x00};
  buf[0] = addr;  // first byte to write the the memory address
  buf[1] = value; // second byte is the actual data / content
  HAL_StatusTypeDef result;
  result = HAL_I2C_Master_Transmit(i2cHandle, EEPROM_addr<<1, buf, 2, HAL_MAX_DELAY);
  if ( result != HAL_OK ) {
    printf("unable to set address of EEPROM\r\n");
    return 1;
  }
  // give the EEPROM some time to write the data into the memory
  HAL_Delay(10);
  return 0;
}

/**
 *
 */
uint8_t read8_EEPROM(I2C_HandleTypeDef* i2cHandle, uint8_t EEPROM_addr, uint8_t addr){
  // read a 8bit number from the EEPROM
  uint8_t buf[1] = {0x00};
  buf[0] = addr;
  HAL_StatusTypeDef result;
  result = HAL_I2C_Master_Transmit(i2cHandle, EEPROM_addr<<1, buf, 1, HAL_MAX_DELAY);
  if ( result != HAL_OK ) {
    printf("unable to set address of EEPROM\r\n");
    return 0xFF;
  }
  result = HAL_I2C_Master_Receive(i2cHandle, EEPROM_addr<<1, buf, 1, HAL_MAX_DELAY);
  if ( result != HAL_OK ) {
    printf("Error TMP100 RX\r\n");
    return 0xFF;
  }
  return buf[0];
}


/**
 * init the temperature sensor
 */
void i2c_init_TMP100(I2C_HandleTypeDef* i2cHandle, uint8_t TMP100_addr){
#ifdef TMP100_DEBUG
  printf("Init TMP100\r\n");
#endif
  // set the resolution of the TMP100

  uint8_t buf[2] = {
        0x01,   // point to configuration register
        0x00    // configuration register content
        };
  // see Table 8 of TMP100 / TMP101 datasheet
  // ignore other settings than resolution
  // features like alert, thermostat and fault handling are not needed to be
  // configured. We just want to have the best resolution (R1 = R0 = 1 - 12bit)
  // R1 = D6, R0 = D5
  buf[1] = (1<<6) | (1<<5);
  HAL_StatusTypeDef result;
  result = HAL_I2C_Master_Transmit(i2cHandle, TMP100_addr<<1, buf, 2, HAL_MAX_DELAY);
  if ( result != HAL_OK ) {
    printf("unable to set resolution of TMP100\r\n");
  }
}
/**
 * read the I2C temperature sensor
 * @param i2cHandle
 * @param TMP100_addr
 * @return raw temperature
 */
uint16_t i2c_read_TMP100(I2C_HandleTypeDef* i2cHandle, uint8_t TMP100_addr){
#ifdef TMP100_DEBUG
  printf("Reading TMP100\r\n");
#endif

  uint8_t buf[2];  // buffer for sending and receiving I2C data
  int16_t val = 0xFFFF;
  HAL_StatusTypeDef result;

  // Tell TMP100 that we want to read from the temperature register
  buf[0] = 0x00;
  result = HAL_I2C_Master_Transmit(i2cHandle, TMP100_addr<<1, buf, 1, HAL_MAX_DELAY);
  if ( result == HAL_OK ) {
    // Read 2 bytes from the temperature register
    result = HAL_I2C_Master_Receive(i2cHandle, TMP100_addr<<1, buf, 2, HAL_MAX_DELAY);
    if ( result != HAL_OK ) {
      printf("Error TMP100 RX\r\n");
    } else {
      //Combine the bytes
      val = ((int16_t)buf[0] << 4) | (buf[1] >> 4);
      // Convert to 2's complement, since temperature can be negative
      if ( val > 0x7FF ) {
        val |= 0xF000;
      }

#ifdef TMP100_DEBUG
      // Convert to float temperature value (Celsius)
      float temp_c = val * 0.0625;
      // Convert temperature to decimal format
      temp_c *= 100;
      printf("%u.%u C\r\n", ((unsigned int)temp_c / 100),
                                ((unsigned int)temp_c % 100));
#endif
    }
  }else{
    printf("Error TMP100 TX\r\n");
  }
  return val;
}
