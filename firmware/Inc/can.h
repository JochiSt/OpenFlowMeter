/**
  ******************************************************************************
  * @file    can.h
  * @brief   This file contains all the function prototypes for
  *          the can.c file
  ******************************************************************************
  * @attention
  *
  * <h2><center>&copy; Copyright (c) 2022 STMicroelectronics.
  * All rights reserved.</center></h2>
  *
  * This software component is licensed by ST under BSD 3-Clause license,
  * the "License"; You may not use this file except in compliance with the
  * License. You may obtain a copy of the License at:
  *                        opensource.org/licenses/BSD-3-Clause
  *
  ******************************************************************************
  */
/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __CAN_H__
#define __CAN_H__

#ifdef __cplusplus
extern "C" {
#endif

/* Includes ------------------------------------------------------------------*/
#include "main.h"

/* USER CODE BEGIN Includes */
#include <stdint.h>
#include <stdbool.h>
/* USER CODE END Includes */

extern CAN_HandleTypeDef hcan;

/* USER CODE BEGIN Private defines */
/* CAN Message IDs */
// The format is 0xX?Y, where ? is replaced by the board ID
#define CAN_CONFIG_ID       0x100
#define CAN_UC_STATUS       0x101
#define CAN_DAC_ID          0x102

#define CAN_ADC_MSG_ID_CH0  0x103
#define CAN_ADC_MSG_ID_CH1  0x104

#define CAN_I2C_MSG_TMP100  0x108
#define CAN_I2C_MSG_BME680  0x109


extern uint8_t can_message_received;
extern CAN_RxHeaderTypeDef   RxHeader;
extern uint8_t               RxData[8];
extern uint8_t data[8];

/* USER CODE END Private defines */

void MX_CAN_Init(void);

/* USER CODE BEGIN Prototypes */
void CAN_send_data_frame(uint16_t can_id, uint8_t size, uint8_t *data);
void CAN_prepare_filter_id(uint16_t canID0, uint16_t canID1, uint8_t can_fifo);
void CAN_prepare_filter_mask(uint16_t maskID0, uint16_t canID0, uint16_t maskID1, uint16_t canID1, uint8_t can_fifo);
void CAN_parse_message(CAN_RxHeaderTypeDef RxHeader, uint8_t *RxData);

void CAN_send_DAC_readback();
void CAN_send_Configuration();

/* USER CODE END Prototypes */

#ifdef __cplusplus
}
#endif

#endif /* __CAN_H__ */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
