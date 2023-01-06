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
#include "eeprom_cfg.h"
#include "i2c.h"          // needed for the pointer to the I2C bus
#include "config.h"

/// store the current used filter bank
uint8_t can_filter_bank = 0;
/// is there a new message, which we have received?
uint8_t can_message_received = 0;

CAN_RxHeaderTypeDef   RxHeader;
uint8_t               RxData[8];
uint8_t data[8] = {0};        ///< bytes, which are send via the CAN bus

uint16_t PWM0, PWM1;
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
void CAN_prepare_filter_id(uint16_t canID0, uint16_t canID1, uint8_t can_fifo){
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

void CAN_prepare_filter_mask(uint16_t maskID0, uint16_t canID0, uint16_t maskID1, uint16_t canID1, uint8_t can_fifo){
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
    canfilterconfig.FilterMaskIdHigh      = maskID0<<5;

    canfilterconfig.FilterIdLow           = canID1<<5;
    canfilterconfig.FilterMaskIdLow       = maskID1<<5;

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
  /****************************************************************************/
  // 0x1?0 HANDLE CONFIGURATION
  if ( RxHeader.StdId == (uint32_t)(CAN_CONFIG_ID | (cfg.board_ID << 4))) {
    //RxHeader.DLC <- data length
    if (RxHeader.DLC == 2){
      // RxData[0] <- byte ID
      // RXData[1] <- value
      uint8_t *ptr = (uint8_t*)&cfg;
      if(RxData[0] <= sizeof(config_t) ){
        ptr[RxData[0]] = RxData[1];
      }else{
        // pointer is out of allowed range
      }
    }else if(RxHeader.DLC == 8){
      // write config to EEPROM
      // to ensure, that we really want to write to EEPROM, double check the
      // data (it's a special word)
      if(    RxData[0] == 0x12
          && RxData[1] == 0x34
          && RxData[2] == 0x56
          && RxData[3] == 0x78
          && RxData[4] == 0x90
          && RxData[5] == 0x01
          && RxData[6] == 0xFF
          && RxData[7] == 0xFE
          ){
        write_EEPROM_cfg(&hi2c1, &cfg);
      }else if(  RxData[0] == 0x12
              && RxData[1] == 0x34
              && RxData[2] == 0x56
              && RxData[3] == 0x78
              && RxData[4] == 0x90
              && RxData[5] == 0x01
              && RxData[6] == 0xFF
              && RxData[7] == 0xFF
          ){
        write_EEPROM_cfg(&hi2c1, &default_cfg);
      }else if(  RxData[0] == 0x12
              && RxData[1] == 0x34
              && RxData[2] == 0x56
              && RxData[3] == 0x78
              && RxData[4] == 0x90
              && RxData[5] == 0x01
              && RxData[6] == 0xFF
              && RxData[7] == 0xFD
          ){
        CAN_send_Configuration();
     }else if(  RxData[0] == 0x12
          && RxData[1] == 0x34
          && RxData[2] == 0x56
          && RxData[3] == 0x78
          && RxData[4] == 0x90
          && RxData[5] == 0x01
      ){
       uint8_t *ptr = (uint8_t*)&cfg;

       uint8_t addr = RxData[6]; // address inside the EEPROM
       if( addr<sizeof(config_t) ){
         ptr[addr] = RxData[7];
       }
     }
    }
  /****************************************************************************/
  // 0x1?1 DAC settings
  }else if ( RxHeader.StdId == (uint32_t)(CAN_DAC_ID | (cfg.board_ID << 4))) {
    // set PWM values
    PWM0 = RxData[0] <<8 | RxData[1];
    PWM1 = RxData[2] <<8 | RxData[3];

    printf("PWM1 %x PWM2 %x\r\n", PWM0, PWM1);

    CAN_send_DAC_readback();
  /****************************************************************************/
  }else{
    printf("received message with ID: %x\r\n", (uint16_t) RxHeader.StdId);
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
    
  // check, whether we have a free mailbox or wait until we have one
  uint16_t timeout_ms = 100;
  while( HAL_CAN_GetTxMailboxesFreeLevel(&hcan) == 0 ) {
    if ( !timeout_ms ){ /*TODO ignore timeout in ISR */
      break;
    }else {
      timeout_ms--;
      HAL_Delay(1);
    }
  }
  if(timeout_ms == 0){
    // there is no free mailbox
    // reason might be, that there is no second participant on the CAN Bus
    // who acknowledges our messages.
    printf("No free CAN Mailbox\r\n");
    HAL_CAN_AbortTxRequest(&hcan, 4 | 2 | 1);   // clear all Mailboxes
    LED_ERROR_TOGGLE;
    return;
  }else{
    // there is a free mailbox
    if (HAL_CAN_AddTxMessage(&hcan, &TxHeader, data, &TxMailbox) != HAL_OK){
      Error_Handler();
    }else{
      LED_CANTX_TOGGLE;
    }
  }
}

void CAN_send_DAC_readback(void){
  data[0] = upper(TIM3->CCR2);
  data[1] = lower(TIM3->CCR2);
  data[2] = upper(TIM3->CCR1);
  data[3] = lower(TIM3->CCR1);

  CAN_send_data_frame( CAN_DAC_ID | (cfg.board_ID << 4), 4, data);
}

void CAN_send_floats(uint16_t can_id, float *float0, float *float1){
  uint8_t *ptr_t0 = (uint8_t*)float0;
  uint8_t *ptr_t1 = (uint8_t*)float1;
  for( uint8_t i=0; i<4; i++){
    data[i] = ptr_t0[i];
  }
  for( uint8_t i=0; i<4; i++){
    data[i+4] = ptr_t1[i];
  }
  CAN_send_data_frame( can_id, 8, data);
}


void CAN_send_Configuration(void){
  uint8_t *ptr = (uint8_t*)&cfg;
  uint8_t addr; // address inside the EEPROM
  for(addr=0; addr<sizeof(config_t); addr++){
    data[0] = addr;
    data[1] = ptr[addr];
    CAN_send_data_frame( CAN_CONFIG_ID | (cfg.board_ID << 4), 2, data);
    HAL_Delay(10);
  }
}

/* USER CODE END 1 */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
