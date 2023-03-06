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
#include "eeprom_cfg.h"

#include "pid.h"

#include <stdbool.h>
/* USER CODE END Includes */

/* Private typedef -----------------------------------------------------------*/
/* USER CODE BEGIN PTD */

/* USER CODE END PTD */

/* Private define ------------------------------------------------------------*/
/* USER CODE BEGIN PD */
// select, what should be printed via UART
//#define PRINT_UART_PID          // print PID performance
//#define PRINT_UART_ADC        // print the ADC data
//#define PRINT_UART_CALC_TEMP  // print the calculated temperatures

/**
 * PCB v1 compatibility mode
 */
//#define PCB_V1

/**
 * PCB v2 compatibility mode
 * enables:
 *  - dual gain ADC readout
 *  - I2C sensor readout
 */
//#define PCB_V2
#ifdef PCB_V2
#undef PCB_V1
#define I2C_SENSOR_READOUT
#endif

/**
 * PCB v3 compatibility mode
 * enables:
 *  - dual gain ADC readout
 *  - offset for ADC / differential amplifier
 *  - I2C sensor readout
 */
//#define PCB_V3
#ifdef PCB_V3
#undef PCB_V1
#undef PCB_V2
#define I2C_SENSOR_READOUT
#endif

//#define WRITE_DEFAULT_CFG_EEPROM_STARTUP
/* USER CODE END PD */

/* Private macro -------------------------------------------------------------*/
/* USER CODE BEGIN PM */
/* USER CODE END PM */

/* Private variables ---------------------------------------------------------*/

/* USER CODE BEGIN PV */
/* at the moment, just for one gain */
/// current
float current0, current1;
/// voltage
float voltage0, voltage1;
/// temperature
float temperature0, temperature1;

// avoid flickering saturation non saturation
#define SAT_CNT_PRESET  10
uint8_t current0_sat_cnt, current1_sat_cnt;
uint8_t voltage0_sat_cnt, voltage1_sat_cnt;

/// output from PID, which is connected to the PWM output, if the PID is active
uint16_t PIDout0, PIDout1;

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
  MX_TIM1_Init();
  MX_TIM4_Init();
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
  generateDefaultCFG(&cfg);
  generateDefaultCFG(&default_cfg);

  printf("\r\n\r\nDEFAULT config:\r\n");
  printCfg(&default_cfg);

#ifdef WRITE_DEFAULT_CFG_EEPROM_STARTUP
  write_EEPROM_cfg(&hi2c1, &default_cfg);
#endif

  read_EEPROM_cfg(&hi2c1, &cfg, &default_cfg);

  printf("\r\n\r\nEEPROM config:\r\n");
  printCfg(&cfg);

  // link configuration to PID controllers
  pid0.PIDcfg = &cfg.PID0;
  pid1.PIDcfg = &cfg.PID1;
  pid0.input  = &temperature0;
  pid1.input  = &temperature1;
  pid0.output = &PIDout0;
  pid1.output = &PIDout1;

  printf("\r\n\r\n");
  /****************************************************************************/
  // START CAN Bus (required for transmission of messages)
  printf("starting CAN Bus...\r\n");
  HAL_CAN_Start(&hcan);

  // prepare CAN filter for receiving messages
  // FIFO 0
  CAN_prepare_filter_id(
      CAN_CONFIG_ID | (cfg.board_ID << 4),
      CAN_DAC_ID    | (cfg.board_ID << 4),
      0);
  // FIFO 1
  //CAN_prepare_filter_id(0x125, 0x126, 1);   // not needed?

  // activate notifications
  if(HAL_CAN_ActivateNotification(&hcan, CAN_IT_RX_FIFO0_MSG_PENDING)!= HAL_OK){
	  Error_Handler();
  }
  if(HAL_CAN_ActivateNotification(&hcan, CAN_IT_RX_FIFO1_MSG_PENDING)!= HAL_OK){
	  Error_Handler();
  }
  /****************************************************************************/
  printf("starting periodic timer TIM1...\r\n");
  HAL_TIM_Base_Start_IT(&htim1);

#ifdef PCB_V3
  // PWM for driving the bias of the amplifier
  printf("starting TIM2 PWM...\r\n");
  HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_1); // start channel 1
  HAL_TIM_PWM_Start(&htim2, TIM_CHANNEL_2); // start channel 2

  // Initialize PWM outputs with 0
  TIM2->CCR1 = 0; // set channel 1
  TIM2->CCR2 = 0; // set channel 2
#endif

  // PWM for driving the current sources
  printf("starting TIM3 PWM...\r\n");
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_1); // start channel 1
  HAL_TIM_PWM_Start(&htim3, TIM_CHANNEL_2); // start channel 2

  // Initialize PWM outputs with 0
  TIM3->CCR1 = 0; // set channel 1
  TIM3->CCR2 = 0; // set channel 2

  /****************************************************************************/
  // Calibrate The ADC On Power-Up For Better Accuracy
  printf("calibrating ADC...\r\n");
  HAL_ADCEx_Calibration_Start(&hadc1);

  /****************************************************************************/
#ifdef I2C_SENSOR_READOUT
  // Test of TMP100 / TMP101
  i2c_init_TMP100(&hi2c1, 0x48);
  i2c_read_TMP100(&hi2c1, 0x48);
#endif

  // start ADC DMA
  printf("starting ADC DMA...\r\n");
  // start first ADC conversion
  HAL_ADC_Start_DMA(&hadc1, adcBuf, ADC_BUFLEN); //Link DMA to ADC1
  /****************************************************************************/
  /* USER CODE END 2 */

  /* Infinite loop */
  /* USER CODE BEGIN WHILE */

  /// store the old timer2 value
  uint8_t timer_elapsed_old = 0;

  // variables for transmitting CAN messages
  uint8_t cnt_can_adc = 0;        ///< counter for the CAN ADC message rate

#ifdef I2C_SENSOR_READOUT
  uint8_t cnt_can_i2c_tmp100 = 0; ///< counter for the CAN I2C TMP100 rate
  uint8_t cnt_can_i2c_bme680 = 0; ///< counter for the CAN I2C BME680 rate
#endif

  uint8_t cnt_print_uart = 0;     ///< counter for UART output

  uint8_t ADCgainUsed = 0;        ///< which ADC gain is used for calculation

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
    if( timer_elapsed >= timer_elapsed_old){
        timer_elapsed_old = timer_elapsed + 1;	// important to add +1, in
                                                  // order to catch overflow

        // increase the interval counters every time this counter is evaluated
        cnt_can_adc++;
        cnt_print_uart++;

#ifdef I2C_SENSOR_READOUT
        cnt_can_i2c_tmp100++;
        cnt_can_i2c_bme680++;
#endif

        /***********************************************************************
         * PID handling
         * for the PID, it is important, that it is triggered with a constant
         * frequency.
         */
        // calculate current and voltage of each channel
        // use the highest possible gain

        ADCgainUsed = 0;
        /** CHANNEL 0 *********************************************************/
        current0 = (avr_adcBuf_GAIN_0[0] * LSB2I) + cfg.GAIN0.Ibias/1000.;
#ifdef PCB_V2
        if( avr_adcBuf_GAIN_1[0] < ISATURATION_LSB ){
          // high gain setting
          if(!current0_sat_cnt){
            current0 = avr_adcBuf_GAIN_1[0] * LSB2I / cfg.GAIN0.Igain;
            ADCgainUsed |= (1 << 0);
          }else{
            current0_sat_cnt--;
          }
        }else{
          current0_sat_cnt = SAT_CNT_PRESET;
        }
#endif

        voltage0 = (avr_adcBuf_GAIN_0[1] * LSB2U) + cfg.GAIN0.Ubias;
#ifdef PCB_V2
        if( avr_adcBuf_GAIN_1[1] < USATURATION_LSB ){
          // high gain setting
          if(!voltage0_sat_cnt){
            voltage0 = avr_adcBuf_GAIN_1[1] * LSB2U / cfg.GAIN0.Ugain;
            ADCgainUsed |= (1 << 1);
          }else{
            voltage0_sat_cnt--;
          }
        }else{
          voltage0_sat_cnt = SAT_CNT_PRESET;
        }
#endif
        /** CHANNEL 1 *********************************************************/
        current1 = (avr_adcBuf_GAIN_0[2] * LSB2I) + cfg.GAIN1.Ibias/1000.;
#ifdef PCB_V2
        if( avr_adcBuf_GAIN_1[2] < ISATURATION_LSB ){
          // high gain setting
          if(!current1_sat_cnt){
            current1 = avr_adcBuf_GAIN_1[2] * LSB2I / cfg.GAIN1.Igain;
            ADCgainUsed |= (1 << 2);
          }else{
            current1_sat_cnt--;
          }
        }else{
          current1_sat_cnt = SAT_CNT_PRESET;
        }
#endif

        voltage1 = (avr_adcBuf_GAIN_0[3] * LSB2U) + cfg.GAIN1.Ubias;
#ifdef PCB_V2
        if( avr_adcBuf_GAIN_1[3] < USATURATION_LSB ){
          // high gain setting
          if(!voltage1_sat_cnt){
            voltage1 = avr_adcBuf_GAIN_1[3] * LSB2U / cfg.GAIN1.Ugain;
            ADCgainUsed |= (1 << 3);
          }else{
            voltage1_sat_cnt--;
          }
        }else{
          voltage1_sat_cnt = SAT_CNT_PRESET;
        }
#endif
        /** calculate temperatures ********************************************/
        temperature0 = convertPT100_R2T( voltage0 / current0 );
        temperature1 = convertPT100_R2T( voltage1 / current1 );

        /** run the PID controllers *******************************************/
        runPID(&pid0);
        runPID(&pid1);

        /** update the output, if the PID is active ***************************/
        if(pid0.active){
          TIM3->CCR2 = PIDout0;
        }else{
          TIM3->CCR2 = PWM0;
        }
        if(pid1.active){
          TIM3->CCR1 = PIDout1;
        }else{
          TIM3->CCR1 = PWM1;
        }

        // link the PID active to the configuration active
        pid0.active = cfg.PID_flags.PID0_active;
        pid1.active = cfg.PID_flags.PID1_active;
    }

    /*************************************************************************
     * Print some variables via UART
     ************************************************************************/
    if( cnt_print_uart >= cfg.interval_PRINT_UART
        && cfg.interval_PRINT_UART < 255
        ){
      cnt_print_uart = 0;

#ifdef PRINT_UART_ADC
      printf("collected ADC results %d\r\n", adc_result_cnt);
      // reset ADC result counter
      adc_result_cnt = 0;

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

#endif
#ifdef PRINT_UART_PID
      printf("PID0 %d\r\n",  pid0.active);
      printf(" - I   %f\r\n",  current0);
      printf(" - U   %f\r\n",  voltage0);
      printf(" - PWM %ld\r\n", TIM3->CCR2);
      printf(" - Tm  %f\r\n",  temperature0);
      printf(" - Ts  %f\r\n",  pid0.PIDcfg->PID_T );
      printf(" - P   %f\r\n",  pid0.PIDcfg->PID_P );
      printf(" - I   %f\r\n",  pid0.PIDcfg->PID_I );
      printf(" - D   %f\r\n",  pid0.PIDcfg->PID_D );

      printf("PID1 %d\r\n", pid1.active);
      printf(" - I   %f\r\n",  current1);
      printf(" - U   %f\r\n",  voltage1);
      printf(" - PWM %ld\r\n", TIM3->CCR1);
      printf(" - Tm  %f\r\n",  temperature1);
      printf(" - Ts  %f\r\n",  pid1.PIDcfg->PID_T );
      printf(" - P   %f\r\n",  pid1.PIDcfg->PID_P );
      printf(" - I   %f\r\n",  pid1.PIDcfg->PID_I );
      printf(" - D   %f\r\n",  pid1.PIDcfg->PID_D );
#endif
#ifdef PRINT_UART_CALC_TEMP
      printf("Temperatures:\r\n");
      printf("ADC gain selection %x \r\n", ADCgainUsed);
      printf("CH0: %f\r\n", temperature0);
      printf(" - I   %f\r\n",  current0);
      printf(" - U   %f\r\n",  voltage0);
      printf("CH1: %f\r\n", temperature1);
      printf(" - I   %f\r\n",  current1);
      printf(" - U   %f\r\n",  voltage1);
#endif
    }

    /***************************************************************************
     * Send out periodic CAN messages for ADC
     **************************************************************************/
    // ADC CAN message
    if( cnt_can_adc >= cfg.interval_CAN_ADC && cfg.interval_CAN_ADC < 255) {
        // reset CAN timer counter
        cnt_can_adc = 0;

        // TODO remove debug CAN message transmission
        //CAN_send_DAC_readback();
        CAN_send_uint16s(CAN_DAC_ID         | (cfg.board_ID << 4),
                             3, TIM3->CCR2, TIM3->CCR1, (uint16_t)ADCgainUsed );
        CAN_send_floats( CAN_TEMPERATURE_ID | (cfg.board_ID << 4) ,
                                                  &temperature0, &temperature1);
        CAN_send_floats( CAN_VOLTAGE_ID     | (cfg.board_ID << 4) ,
                                                  &voltage0, &voltage1);
        CAN_send_floats( CAN_CURRENT_ID     | (cfg.board_ID << 4) ,
                                                  &current0, &current1);

        /**********************************************************************/
        // convert 16bit ADC result into 2x 8bit for CAN message
        // one CAN message can transport up to 8 bytes

        /**********************************************************************/
        // CHANNEL 0
        CAN_send_uint16s(CAN_ADC_MSG_ID_CH0 | (cfg.board_ID << 4), 4,
            avr_adcBuf_GAIN_0[0], avr_adcBuf_GAIN_0[1],
            avr_adcBuf_GAIN_1[0], avr_adcBuf_GAIN_1[1]
            );

        /**********************************************************************/
        // CHANNEL 1
        CAN_send_uint16s(CAN_ADC_MSG_ID_CH1 | (cfg.board_ID << 4), 4,
            avr_adcBuf_GAIN_0[2], avr_adcBuf_GAIN_0[3],
            avr_adcBuf_GAIN_1[2], avr_adcBuf_GAIN_1[3]
            );
        /**********************************************************************/
        // send internal data
        CAN_send_uint16s(CAN_UC_STATUS | (cfg.board_ID << 4), 2,
            avr_adcBuf_GAIN_0[4], avr_adcBuf_GAIN_0[5]
            );
    }

    /***************************************************************************
     * Send out periodic CAN messages for I2C bus
     **************************************************************************/
#ifdef I2C_SENSOR_READOUT
    // I2C sensors
    if( cnt_can_i2c_tmp100 >= cfg.interval_I2C_TMP100
        && cfg.interval_I2C_TMP100 < 255){
      cnt_can_i2c_tmp100 = 0;
      uint16_t tmp100 = i2c_read_TMP100(&hi2c1, 0x48);
      CAN_send_uint16s(CAN_I2C_MSG_TMP100 | (cfg.board_ID << 4), 1, tmp100 );
    }
    if( cnt_can_i2c_bme680 >= cfg.interval_I2C_BME680
        && cfg.interval_I2C_BME680 < 255){
      //TODO to be implemented
    }
#endif
  } // while(1)
  /* USER CODE END 3 */
} // void main()

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
