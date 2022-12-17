/* USER CODE BEGIN Header */
/**
  ******************************************************************************
  * @file           : main.c
  * @brief          : Main program body
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
/* USER CODE END Header */
/* Includes ------------------------------------------------------------------*/
#include "main.h"
#include "adc.h"
#include "can.h"
#include "dma.h"
#include "i2c.h"
#include "spi.h"
#include "tim.h"
#include "usart.h"
#include "gpio.h"

/* Private includes ----------------------------------------------------------*/
/* USER CODE BEGIN Includes */
#include "syscalls.h"
#include "utils.h"
#include "i2c_scanner.h"
#include "i2c_utils.h"
#include "config.h"
#include <stdbool.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
// send out the can message about the ADC
// gives the number of triggered interrupts in 125ms steps
#define CAN_ADC_RATE    (500/125)
#define CAN_I2C_RATE    (2000/125)
#define PRINT_UART_RATE (1000/125)

/* CAN Message IDs */
#define CAN_ADC_MSG_ID_CH0  0x123
#define CAN_ADC_MSG_ID_CH1  0x124
#define CAN_STATUS_ID       0x120
#define CAN_I2C_MSG_TMP100  0x121
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */


/* USER CODE END PV */

/* Private function prototypes -----------------------------------------------*/
void SystemClock_Config(void);
/* USER CODE BEGIN PFP */

/* USER CODE END PFP */

/* Private user code ---------------------------------------------------------*/
/* USER CODE BEGIN 0 */

/* USER CODE END 0 */

/**
  * @brief  The application entry point.
  * @retval int
  */
int main(void)
{
  /* USER CODE BEGIN 1 */

  /* USER CODE END 1 */

  /* MCU Configuration--------------------------------------------------------*/

  /* Reset of all peripherals, Initializes the Flash interface and the Systick. */
  HAL_Init();

  /* USER CODE BEGIN Init */

  /* USER CODE END Init */

  /* Configure the system clock */
  SystemClock_Config();

  /* USER CODE BEGIN SysInit */

  /* USER CODE END SysInit */

  /* Initialize all configured peripherals */
  MX_GPIO_Init();
  MX_DMA_Init();
  MX_ADC1_Init();
  MX_CAN_Init();
  MX_I2C1_Init();
  MX_I2C2_Init();
  MX_USART1_UART_Init();
  MX_SPI2_Init();
  MX_TIM3_Init();
  MX_TIM2_Init();
  /* USER CODE BEGIN 2 */
  /****************************************************************************/
  printf("\r\n\r\n");
  printf("Compiled at "__DATE__" - "__TIME__"\r\n");
  printf("Compiled with GCC Version "__VERSION__"\r\n");
  /****************************************************************************/
  // all OFF
  LED_ERROR(SET);    // red      -> failure
  LED_CANRX(SET);    // yellow   -> RX
  LED_CANTX(SET);    // yellow   -> TX
  LED_STATUS(SET);   // green    -> TIM2

  // all LEDs ON
  LED_ERROR(RESET);
  HAL_Delay(500);
  LED_CANRX(RESET);
  HAL_Delay(500);
  LED_CANTX(RESET);
  HAL_Delay(500);
  LED_STATUS(RESET);

  HAL_Delay(1000);

  // do an I2C scan of both I2C ports
  i2c_scan(&hi2c1);   // PORT 1
  i2c_scan(&hi2c2);   // PORT 2

  // all LEDs off
  LED_ERROR(SET);
  HAL_Delay(500);
  LED_CANRX(SET);
  HAL_Delay(500);
  LED_CANTX(SET);
  HAL_Delay(500);
  LED_STATUS(SET);
  /****************************************************************************/
  // read all configuration values from I2C EEPROM, or use default ones
  generateDefaultCFG();
  cfg = default_cfg;

  /****************************************************************************/
  // START CAN Bus (required for transmission of messages)
  printf("starting CAN Bus...\r\n");
  HAL_CAN_Start(&hcan);

  // prepare CAN filter for receiving messages
  CAN_prepare_filter(0x123, 0x124, 0);
  CAN_prepare_filter(0x125, 0x126, 1);

  // activate notifications
  if(HAL_CAN_ActivateNotification(&hcan, CAN_IT_RX_FIFO0_MSG_PENDING) != HAL_OK){
	  Error_Handler();
  }
  if(HAL_CAN_ActivateNotification(&hcan, CAN_IT_RX_FIFO1_MSG_PENDING) != HAL_OK){
	  Error_Handler();
  }
  /****************************************************************************/
  printf("starting TIM2...\r\n");
  HAL_TIM_Base_Start_IT(&htim2);

  printf("starting TIM3 PWM...\r\n");
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1); // start channel 1
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2); // start channel 2

  // initialise PWM outputs with 0
  TIM3->CCR1 = 0; // set channel 1 max. 1024
  TIM3->CCR2 = 0; // set channel 2 max. 1024
  /****************************************************************************/
  // Calibrate The ADC On Power-Up For Better Accuracy
  printf("calibrating ADC...\r\n");
  HAL_ADCEx_Calibration_Start(&hadc1);

  /****************************************************************************/
  // Test of TMP100 / TMP101
  i2c_init_TMP100(&hi2c1, 0x48);
  i2c_read_TMP100(&hi2c1, 0x48);

  // start ADC DMA
  printf("starting ADC DMA...\r\n");
  // start first ADC conversion
  HAL_ADC_Start_DMA(&hadc1, adcBuf, ADC_BUFLEN); //Link DMA to ADC1
  /****************************************************************************/
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */

  /// store the old timer2 value
  uint8_t timer2_elapsed_old = 0;

  // variables for transmitting CAN messages
  uint8_t cnt_can_adc = 0;      ///< counter for the CAN ADC message rate
  uint8_t cnt_can_i2c = 0;      ///< counter for the CAN I2C message rate

  uint8_t cnt_print_uart = 0;   ///< counter for UART output

  uint8_t data[8] = {0};        ///< bytes, which are send via the CAN bus


  /****************************************************************************/
  printf("successfully started everything\r\n");
  // Main loop
  while (1)
  {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
    /**************************************************************************/
    // CAN message handling is done in CAN_parse_message in can.c
    if (can_message_received){
      CAN_parse_message(RxHeader, RxData);
      can_message_received = 0;
    }

    /***************************************************************************
     * check whether a new ADC result has been taken, wait a short time for
     * everything to settle and trigger a new conversion
     **************************************************************************/
    if (adc_result_received){
      adc_result_received = 0;
      HAL_Delay(2);
      HAL_ADC_Start_DMA(&hadc1, adcBuf, ADC_BUFLEN);
    }

    /***************************************************************************
     * check timer 2 for doing periodic tasks
     * one timer2_elapsed is equal to 125ms
     **************************************************************************/
    if( timer2_elapsed >= timer2_elapsed_old){
        timer2_elapsed_old = timer2_elapsed + 1;	// important to add +1, in
                                                  // order to catch overflow

        // increase the CAN counter every time this counter is evaluated
        cnt_can_adc++;
        cnt_can_i2c++;
        cnt_print_uart++;

        /***********************************************************************
         * PID handling
         * for the PID, it is important, that it is triggered with a constant
         * frequency.
         */

    }

    /*************************************************************************
     * Print some variables via UART
     ************************************************************************/
    if( cnt_print_uart >= PRINT_UART_RATE){
      cnt_print_uart = 0;

      printf("collected ADC results %d\r\n", adc_result_cnt);
      // reset ADC result counter
      adc_result_cnt = 0;

      /**********************************************************************/
      // printout collected data
      // first 4 samples are from current sources
      for(uint8_t i = 0; i<4; i++){
        printf("%d\t", avr_adcBuf_GAIN_0[i]);
      }
      printf("\r\n");
      for(uint8_t i = 0; i<4; i++){
        printf("%d\t", avr_adcBuf_GAIN_1[i]);
      }
      printf("\r\n");

      printf("T= %ld\tU= %ld\r\n", adcBuf[4], adcBuf[5]);
    }

    /***************************************************************************
     * Send out periodic CAN messages for ADC
     **************************************************************************/
    // ADC CAN message
    if( cnt_can_adc >= CAN_ADC_RATE) {
        // reset CAN timer counter
        cnt_can_adc = 0;

        /**********************************************************************/
        // convert 16bit ADC result into 2x 8bit for CAN message
        // one CAN message can transport up to 8 bytes

        /**********************************************************************/
        // CHANNEL 0
        // position 0 - 3 GAIN_0
        for(uint8_t i = 0; i<2; i++) {
            data[2*i    ] = upper(avr_adcBuf_GAIN_0[i]);
            data[2*i + 1] = lower(avr_adcBuf_GAIN_0[i]);
        }
        // position 4 - 7 GAIN_1
        for(uint8_t i = 0; i<2; i++) {
            data[2*i     + 4] = upper(avr_adcBuf_GAIN_1[i]);
            data[2*i + 1 + 4] = lower(avr_adcBuf_GAIN_1[i]);
        }
        // sendout frame with data
        CAN_send_data_frame(CAN_ADC_MSG_ID_CH0, 8, data);

        /**********************************************************************/
        // CHANNEL 1
        for(uint8_t i = 0; i<2; i++) {
            data[2*i    ] = upper(avr_adcBuf_GAIN_0[i+2]);
            data[2*i + 1] = lower(avr_adcBuf_GAIN_0[i+2]);
        }
        // position 4 - 7 GAIN_1
        for(uint8_t i = 0; i<2; i++) {
            data[2*i     + 4] = upper(avr_adcBuf_GAIN_1[i+2]);
            data[2*i + 1 + 4] = lower(avr_adcBuf_GAIN_1[i+2]);
        }
        // sendout frame with data
        CAN_send_data_frame(CAN_ADC_MSG_ID_CH1, 8, data);

        /**********************************************************************/
        // send internal data
        for(uint8_t i = 0; i<2; i++) {
            data[2*i    ] = upper(avr_adcBuf_GAIN_0[i + 2]);
            data[2*i + 1] = lower(avr_adcBuf_GAIN_0[i + 2]);
        }
        // sendout frame with data
        CAN_send_data_frame(CAN_STATUS_ID, 4, data);
    }

    /***************************************************************************
     * Send out periodic CAN messages for I2C bus
     **************************************************************************/
    // I2C sensors
    if( cnt_can_i2c >= CAN_I2C_RATE){
        cnt_can_i2c = 0;
        uint16_t tmp100 = i2c_read_TMP100(&hi2c1, 0x48);
        data[0] = upper(tmp100);
        data[1] = lower(tmp100);
        CAN_send_data_frame(CAN_I2C_MSG_TMP100, 2, data);
    }
  }
  /* USER CODE END 3 */
}

/**
  * @brief System Clock Configuration
  * @retval None
  */
void SystemClock_Config(void)
{
  RCC_OscInitTypeDef RCC_OscInitStruct = {0};
  RCC_ClkInitTypeDef RCC_ClkInitStruct = {0};
  RCC_PeriphCLKInitTypeDef PeriphClkInit = {0};

  /** Initializes the RCC Oscillators according to the specified parameters
  * in the RCC_OscInitTypeDef structure.
  */
  RCC_OscInitStruct.OscillatorType = RCC_OSCILLATORTYPE_HSE;
  RCC_OscInitStruct.HSEState = RCC_HSE_ON;
  RCC_OscInitStruct.HSEPredivValue = RCC_HSE_PREDIV_DIV2;
  RCC_OscInitStruct.HSIState = RCC_HSI_ON;
  RCC_OscInitStruct.PLL.PLLState = RCC_PLL_ON;
  RCC_OscInitStruct.PLL.PLLSource = RCC_PLLSOURCE_HSE;
  RCC_OscInitStruct.PLL.PLLMUL = RCC_PLL_MUL9;
  if (HAL_RCC_OscConfig(&RCC_OscInitStruct) != HAL_OK)
  {
    Error_Handler();
  }
  /** Initializes the CPU, AHB and APB buses clocks
  */
  RCC_ClkInitStruct.ClockType = RCC_CLOCKTYPE_HCLK|RCC_CLOCKTYPE_SYSCLK
                              |RCC_CLOCKTYPE_PCLK1|RCC_CLOCKTYPE_PCLK2;
  RCC_ClkInitStruct.SYSCLKSource = RCC_SYSCLKSOURCE_PLLCLK;
  RCC_ClkInitStruct.AHBCLKDivider = RCC_SYSCLK_DIV1;
  RCC_ClkInitStruct.APB1CLKDivider = RCC_HCLK_DIV2;
  RCC_ClkInitStruct.APB2CLKDivider = RCC_HCLK_DIV1;

  if (HAL_RCC_ClockConfig(&RCC_ClkInitStruct, FLASH_LATENCY_2) != HAL_OK)
  {
    Error_Handler();
  }
  PeriphClkInit.PeriphClockSelection = RCC_PERIPHCLK_ADC;
  PeriphClkInit.AdcClockSelection = RCC_ADCPCLK2_DIV8;
  if (HAL_RCCEx_PeriphCLKConfig(&PeriphClkInit) != HAL_OK)
  {
    Error_Handler();
  }
}

/* USER CODE BEGIN 4 */

/* USER CODE END 4 */

/**
  * @brief  This function is executed in case of error occurrence.
  * @retval None
  */
void Error_Handler(void)
{
  /* USER CODE BEGIN Error_Handler_Debug */
  /* User can add his own implementation to report the HAL error return state */
  __disable_irq();
  // switch ON red LED
  HAL_GPIO_WritePin(LED1_GPIO_Port, LED1_Pin, GPIO_PIN_RESET);
  while (1)
  {
  }
  /* USER CODE END Error_Handler_Debug */
}

#ifdef  USE_FULL_ASSERT
/**
  * @brief  Reports the name of the source file and the source line number
  *         where the assert_param error has occurred.
  * @param  file: pointer to the source file name
  * @param  line: assert_param error line source number
  * @retval None
  */
void assert_failed(uint8_t *file, uint32_t line)
{
  /* USER CODE BEGIN 6 */
  /* User can add his own implementation to report the file name and line number,
     ex: printf("Wrong parameters value: file %s on line %d\r\n", file, line) */
  printf("Wrong parameters value: file %s on line %d\r\n", file, line);
  /* USER CODE END 6 */
}
#endif /* USE_FULL_ASSERT */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
