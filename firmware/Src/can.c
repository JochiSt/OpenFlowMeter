/**
  ******************************************************************************
  * @file    can.c
  * @brief   This file provides code for the configuration
  *          of the CAN instances.
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

/* Includes ------------------------------------------------------------------*/
#include "can.h"

/* USER CODE BEGIN 0 */
#include "syscalls.h"
#include "utils.h"

/// store the current used filter bank
uint8_t can_filter_bank = 0;
/// is there a new message, which we have received?
uint8_t can_message_received = 0;

/* USER CODE END 0 */

CAN_HandleTypeDef hcan;

/* CAN init function */
void MX_CAN_Init(void)
{

  hcan.Instance = CAN1;
  hcan.Init.Prescaler = 6;
  hcan.Init.Mode = CAN_MODE_NORMAL;
  hcan.Init.SyncJumpWidth = CAN_SJW_1TQ;
  hcan.Init.TimeSeg1 = CAN_BS1_7TQ;
  hcan.Init.TimeSeg2 = CAN_BS2_1TQ;
  hcan.Init.TimeTriggeredMode = DISABLE;
  hcan.Init.AutoBusOff = DISABLE;
  hcan.Init.AutoWakeUp = DISABLE;
  hcan.Init.AutoRetransmission = DISABLE;
  hcan.Init.ReceiveFifoLocked = DISABLE;
  hcan.Init.TransmitFifoPriority = ENABLE;
  if (HAL_CAN_Init(&hcan) != HAL_OK)
  {
    Error_Handler();
  }

}

void HAL_CAN_MspInit(CAN_HandleTypeDef* canHandle)
{

  GPIO_InitTypeDef GPIO_InitStruct = {0};
  if(canHandle->Instance==CAN1)
  {
  /* USER CODE BEGIN CAN1_MspInit 0 */

  /* USER CODE END CAN1_MspInit 0 */
    /* CAN1 clock enable */
    __HAL_RCC_CAN1_CLK_ENABLE();

    __HAL_RCC_GPIOB_CLK_ENABLE();
    /**CAN GPIO Configuration
    PB8     ------> CAN_RX
    PB9     ------> CAN_TX
    */
    GPIO_InitStruct.Pin = GPIO_PIN_8;
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT;
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    GPIO_InitStruct.Pin = GPIO_PIN_9;
    GPIO_InitStruct.Mode = GPIO_MODE_AF_PP;
    GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_HIGH;
    HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    __HAL_AFIO_REMAP_CAN1_2();

    /* CAN1 interrupt Init */
    HAL_NVIC_SetPriority(USB_LP_CAN1_RX0_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(USB_LP_CAN1_RX0_IRQn);
    HAL_NVIC_SetPriority(CAN1_RX1_IRQn, 0, 0);
    HAL_NVIC_EnableIRQ(CAN1_RX1_IRQn);
  /* USER CODE BEGIN CAN1_MspInit 1 */

  /* USER CODE END CAN1_MspInit 1 */
  }
}

void HAL_CAN_MspDeInit(CAN_HandleTypeDef* canHandle)
{

  if(canHandle->Instance==CAN1)
  {
  /* USER CODE BEGIN CAN1_MspDeInit 0 */

  /* USER CODE END CAN1_MspDeInit 0 */
    /* Peripheral clock disable */
    __HAL_RCC_CAN1_CLK_DISABLE();

    /**CAN GPIO Configuration
    PB8     ------> CAN_RX
    PB9     ------> CAN_TX
    */
    HAL_GPIO_DeInit(GPIOB, GPIO_PIN_8|GPIO_PIN_9);

    /* CAN1 interrupt Deinit */
    HAL_NVIC_DisableIRQ(USB_LP_CAN1_RX0_IRQn);
    HAL_NVIC_DisableIRQ(CAN1_RX1_IRQn);
  /* USER CODE BEGIN CAN1_MspDeInit 1 */

  /* USER CODE END CAN1_MspDeInit 1 */
  }
}

/* USER CODE BEGIN 1 */
/**
 * prepare CAN filter
 * https://schulz-m.github.io/2017/03/23/stm32-can-id-filter/
 *
*/
void CAN_prepare_filter(uint16_t canID0, uint16_t canID1, uint8_t can_fifo){
  if(can_filter_bank < 14){
    CAN_FilterTypeDef canfilterconfig;
    canfilterconfig.FilterActivation      = CAN_FILTER_ENABLE;  // enable filter
    canfilterconfig.FilterBank            = can_filter_bank++;  // increment filter bank by one
    
    // choose FIFO for filter (each FiFo holds 3 messages)
    if(can_fifo == 0){
      // use FIFO0
      canfilterconfig.FilterFIFOAssignment  = CAN_FILTER_FIFO0;
    }else if(can_fifo == 1){
      // use FIFO1
      canfilterconfig.FilterFIFOAssignment  = CAN_FILTER_FIFO1;
    }else{
      // automatic assignment of FIFO
      if ( can_filter_bank % 2 == 0){
        canfilterconfig.FilterFIFOAssignment  = CAN_FILTER_FIFO1;
      }else{
        canfilterconfig.FilterFIFOAssignment  = CAN_FILTER_FIFO0;
      }
    }
        
    canfilterconfig.FilterIdHigh          = canID0<<5;
    canfilterconfig.FilterMaskIdHigh      = 0x7FF<<5;           // get just this ID    
    
    canfilterconfig.FilterIdLow           = canID1<<5;           
    canfilterconfig.FilterMaskIdLow       = 0x7FF<<5;           // get just this ID
    
    canfilterconfig.FilterMode            = CAN_FILTERMODE_IDMASK;  // or IDLIST for double amount of IDs (but no mask)
    canfilterconfig.FilterScale           = CAN_FILTERSCALE_16BIT;  // for usage with 2x standard ID
    
    canfilterconfig.SlaveStartFilterBank  = 14;   // how many filters do we want to set for CAN1
                                                  // irrelevant for single CAN types
                                                  // STM32F103 -> single CAN 14 filter (0-13)

    HAL_CAN_ConfigFilter(&hcan, &canfilterconfig);// set filter in CAN module
  }else{
    printf("No free CAN filter bank!\r\n");
  }
}

CAN_RxHeaderTypeDef   RxHeader;
uint8_t               RxData[8];
/**
 * CAN RX interrupt callback
 */
void HAL_CAN_RxFifo0MsgPendingCallback(CAN_HandleTypeDef *hcan){
  if (HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO0, &RxHeader, RxData) != HAL_OK){
    Error_Handler();
  }
  LED_CANRX_TOGGLE;
  //CAN_parse_message(RxHeader, RxData);
  can_message_received++;
}

void HAL_CAN_RxFifo1MsgPendingCallback(CAN_HandleTypeDef *hcan){
  if (HAL_CAN_GetRxMessage(hcan, CAN_RX_FIFO1, &RxHeader, RxData) != HAL_OK){
    Error_Handler();
  }
  LED_CANRX_TOGGLE;
  //CAN_parse_message(RxHeader, RxData);
  can_message_received++;
}

void CAN_parse_message(CAN_RxHeaderTypeDef RxHeader, uint8_t *RxData){
  printf("received message with ID: %x\r\n", (uint16_t) RxHeader.StdId);
  if ((RxHeader.StdId == 0x123)) {
      // set PWM values
      uint16_t pwm1 = RxData[0] <<8 | RxData[1];
      uint16_t pwm2 = RxData[2] <<8 | RxData[3];
      
      printf("PWM1 %x PWM2 %x\r\n", pwm1, pwm2);
      
      TIM3->CCR1 = pwm1; // set channel 1 max. 1024
      TIM3->CCR2 = pwm2; // set channel 2 max. 1024  
  }else{
    printf("message not parsed\r\n");
  }
}

/**
 * send data frame via CAN bus
 * @param can_id ID of frame
 * @param size length of data
 * @param data array
 */
void CAN_send_data_frame(uint16_t can_id, uint8_t size, uint8_t *data){
  uint32_t              TxMailbox;
  
  CAN_TxHeaderTypeDef   TxHeader;
  TxHeader.IDE = CAN_ID_STD;    // use standard ID (not extended)
  TxHeader.StdId = can_id;      // message ID
  TxHeader.RTR = CAN_RTR_DATA;  // sending data frame
  TxHeader.DLC = size;          // length of data bytes
    
  // check, whether we have a free mailbox
  if (HAL_CAN_GetTxMailboxesFreeLevel(&hcan) > 0){
    if (HAL_CAN_AddTxMessage(&hcan, &TxHeader, data, &TxMailbox) != HAL_OK){
      Error_Handler();
    }else{
      LED_CANTX_TOGGLE;
    }
  }else{
    // there is no free mailbox
    // reason might be, that there is no second participant on the CAN Bus
    // who acknowledges our messages.
    printf("No free CAN Mailbox\r\n");
    HAL_CAN_AbortTxRequest(&hcan, 4 | 2 | 1);   // clear all Mailboxes
    LED_ERROR_TOGGLE;
  }
}
/* USER CODE END 1 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
