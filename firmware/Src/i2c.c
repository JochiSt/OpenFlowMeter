/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file    i2c.c
  * @brief   This file provides code for the configuration
  *          of the I2C instances.
  ******************************************************************************
  * @attention
  *
  * Copyright (c) 2023 STMicroelectronics.
  * All rights reserved.
  *
  * This software is licensed under terms that can be found in the LICENSE file
  * in the root directory of this software component.
  * If no LICENSE file comes with this software, it is provided AS-IS.
  *
  ******************************************************************************
  */
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "i2c.h"


/* USER CODE BEGIN 0 */
#include <stdio.h>

enum I2CDeviceState {
  /// initial state
  STATE_INITIAL = 0,
  /// receiving the first byte of word addr
  STATE_RECEIVING_ADDRESS,
  /// after the 2nd byte of word addr
  STATE_HAVE_ADDRESS
};
/* USER CODE END 0 */

I2C_HandleTypeDef hi2c1;
I2C_HandleTypeDef hi2c2;

/* I2C1 init function */
void MX_I2C1_Init(void)
{

  /* USER CODE BEGIN I2C1_Init 0 */

  /* USER CODE END I2C1_Init 0 */

  /* USER CODE BEGIN I2C1_Init 1 */

  /* USER CODE END I2C1_Init 1 */
  hi2c1.Instance = I2C1;
  hi2c1.Init.ClockSpeed = 100000;
  hi2c1.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c1.Init.OwnAddress1 = 0;
  hi2c1.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c1.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c1.Init.OwnAddress2 = 0;
  hi2c1.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c1.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c1) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C1_Init 2 */

  /* USER CODE END I2C1_Init 2 */

}
/* I2C2 init function */
void MX_I2C2_Init(void)
{

  /* USER CODE BEGIN I2C2_Init 0 */

  /* USER CODE END I2C2_Init 0 */

  /* USER CODE BEGIN I2C2_Init 1 */

  /* USER CODE END I2C2_Init 1 */
  hi2c2.Instance = I2C2;
  hi2c2.Init.ClockSpeed = 100000;
  hi2c2.Init.DutyCycle = I2C_DUTYCYCLE_2;
  hi2c2.Init.OwnAddress1 = 64;
  hi2c2.Init.AddressingMode = I2C_ADDRESSINGMODE_7BIT;
  hi2c2.Init.DualAddressMode = I2C_DUALADDRESS_DISABLE;
  hi2c2.Init.OwnAddress2 = 0;
  hi2c2.Init.GeneralCallMode = I2C_GENERALCALL_DISABLE;
  hi2c2.Init.NoStretchMode = I2C_NOSTRETCH_DISABLE;
  if (HAL_I2C_Init(&hi2c2) != HAL_OK)
  {
    Error_Handler();
  }
  /* USER CODE BEGIN I2C2_Init 2 */

  /* USER CODE END I2C2_Init 2 */

}

void HAL_I2C_MspInit(I2C_HandleTypeDef* i2cHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(i2cHandle->Instance==I2C1)
  {
  /* USER CODE BEGIN I2C1_MspInit 0 */

  /* USER CODE END I2C1_MspInit 0 */

    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**I2C1 GPIO Configuration
    PB6     ------> I2C1_SCL
    PB7     ------> I2C1_SDA
    */
    GPIO_InitStruct.Pin = GPIO_PIN_6|GPIO_PIN_7;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    /* I2C1 clock enable */
    __HAL_RCC_I2C1_CLK_ENABLE();
  /* USER CODE BEGIN I2C1_MspInit 1 */

  /* USER CODE END I2C1_MspInit 1 */
  }
  else if(i2cHandle->Instance==I2C2)
  {
  /* USER CODE BEGIN I2C2_MspInit 0 */

  /* USER CODE END I2C2_MspInit 0 */

    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**I2C2 GPIO Configuration
    PB10     ------> I2C2_SCL
    PB11     ------> I2C2_SDA
    */
    GPIO_InitStruct.Pin = GPIO_PIN_10|GPIO_PIN_11;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_OD;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    /* I2C2 clock enable */
    __HAL_RCC_I2C2_CLK_ENABLE();

    /* I2C2 interrupt Init */
    HAL_NVIC_SetPriority(I2C2_EV_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(I2C2_EV_IRQn);
  /* USER CODE BEGIN I2C2_MspInit 1 */

  /* USER CODE END I2C2_MspInit 1 */
  }
}

void HAL_I2C_MspDeInit(I2C_HandleTypeDef* i2cHandle)
{

  if(i2cHandle->Instance==I2C1)
  {
  /* USER CODE BEGIN I2C1_MspDeInit 0 */

  /* USER CODE END I2C1_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_I2C1_CLK_DISABLE();

    /**I2C1 GPIO Configuration
    PB6     ------> I2C1_SCL
    PB7     ------> I2C1_SDA
    */
    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_6);

    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_7);

  /* USER CODE BEGIN I2C1_MspDeInit 1 */

  /* USER CODE END I2C1_MspDeInit 1 */
  }
  else if(i2cHandle->Instance==I2C2)
  {
  /* USER CODE BEGIN I2C2_MspDeInit 0 */

  /* USER CODE END I2C2_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_I2C2_CLK_DISABLE();

    /**I2C2 GPIO Configuration
    PB10     ------> I2C2_SCL
    PB11     ------> I2C2_SDA
    */
    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_10);

    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_11);

    /* I2C2 interrupt Deinit */
    HAL_NVIC_DisableIRQ(I2C2_EV_IRQn);
  /* USER CODE BEGIN I2C2_MspDeInit 1 */

  /* USER CODE END I2C2_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */
// interrupt driven I2C RX and TX according to
// https://www.mikrocontroller.net/topic/459202#6441255
// and
// https://github.com/smx-smx/stm32-eeprom/blob/master/src/main.c
/*
1. HAL_I2C_EnableListen_IT
2. Der Master sendet die Nachricht
3. HAL_I2C_AddrCallback kommt: Dort HAL_I2C_Slave_Receive_IT aufrufen
4. HAL_I2C_SlaveRxCpltCallback
5. HAL_I2C_ListenCpltCallback
*/

/** eeprom data **/
#define EEPROM_SIZE (1024)
#define EEPROM_OFFSET(x) ((x) & (sizeof(ram) - 1))

static uint8_t ram[EEPROM_SIZE];
static uint16_t word_addr = 0;
static enum I2CDeviceState state = STATE_INITIAL;
static uint8_t word_addr_byte = 0;

// gets called on address match
void HAL_I2C_AddrCallback(I2C_HandleTypeDef *hi2c, uint8_t TransferDirection, uint16_t AddrMatchCode){

  UNUSED(AddrMatchCode);

  switch (TransferDirection) {
    case I2C_DIRECTION_TRANSMIT:
      // master is sending, start first receive
      // if the master is writing, it always writes the address first
      if( HAL_I2C_Slave_Seq_Receive_IT(hi2c, &word_addr_byte, 1, I2C_NEXT_FRAME) != HAL_OK){
        printf("I2C error: slave receive\r\n");
      }
      break;

    case I2C_DIRECTION_RECEIVE:
      // master is receiving, start first transmit
      word_addr = EEPROM_OFFSET(word_addr);
      if( HAL_I2C_Slave_Seq_Transmit_IT(hi2c, &ram[word_addr], 1, I2C_NEXT_FRAME) != HAL_OK){
        printf("I2C error: slave transmit\r\n");
      }
      break;
  }
}

// gets called when RX / TX done
void HAL_I2C_SlaveTxCpltCallback(I2C_HandleTypeDef *hi2c){
  // we just sent something to the master

  // offer the next eeprom byte (the master will NACK if it doesn't want it)
  word_addr = EEPROM_OFFSET(word_addr + 1);
  HAL_I2C_Slave_Seq_Transmit_IT(hi2c, &ram[word_addr], 1, I2C_NEXT_FRAME);
}


void HAL_I2C_SlaveRxCpltCallback(I2C_HandleTypeDef *hi2c){
  // we just received something from the master
  if(state == STATE_INITIAL){ // received byte0 of addr
    // [DE] AD
    // overwrite previous word_addr
    word_addr = word_addr_byte << 8;
    state = STATE_RECEIVING_ADDRESS;

    // start to receive next addr byte
    HAL_I2C_Slave_Seq_Receive_IT(hi2c, &word_addr_byte, 1, I2C_NEXT_FRAME);
  } else {
    if(state == STATE_RECEIVING_ADDRESS){ // received byte1 of addr
      // DE [AD]
      word_addr |= word_addr_byte;
      state = STATE_HAVE_ADDRESS;
    }
    // handle next (or first) data RX
    HAL_I2C_Slave_Seq_Receive_IT(hi2c, &ram[word_addr], 1, I2C_NEXT_FRAME);
    word_addr = EEPROM_OFFSET(word_addr + 1);
  }
}
//
void HAL_I2C_ListenCpltCallback(I2C_HandleTypeDef *hi2c){
  state = STATE_INITIAL;
  // (re-) enable the listen mode
  HAL_I2C_EnableListen_IT(hi2c);
}


/* USER CODE END 1 */
