#ifndef __UTILS_H__
#define __UTILS_H__

// red 		-> failure
#define LED_ERROR(Op)  HAL_GPIO_WritePin(LED1_GPIO_Port, LED1_Pin, GPIO_PIN_##Op)
// yellow   -> RX
#define LED_CANRX(Op)  HAL_GPIO_WritePin(LED2_GPIO_Port, LED2_Pin, GPIO_PIN_##Op)
// yellow   -> TX
#define LED_CANTX(Op)  HAL_GPIO_WritePin(LED3_GPIO_Port, LED3_Pin, GPIO_PIN_##Op)
// green    -> TIM2
#define LED_STATUS(Op) HAL_GPIO_WritePin(LED4_GPIO_Port, LED4_Pin, GPIO_PIN_##Op)

// GAIN_I & GAIN_U
#define GAIN_I(Op) HAL_GPIO_WritePin(SEL_GAIN_I_GPIO_Port, SEL_GAIN_I_Pin, GPIO_PIN_##Op)
#define GAIN_U(Op) HAL_GPIO_WritePin(SEL_GAIN_U_GPIO_Port, SEL_GAIN_U_Pin, GPIO_PIN_##Op)

#define LED_ERROR_TOGGLE	HAL_GPIO_TogglePin(LED1_GPIO_Port, LED1_Pin);
#define LED_CANRX_TOGGLE	HAL_GPIO_TogglePin(LED2_GPIO_Port, LED2_Pin);
#define LED_CANTX_TOGGLE	HAL_GPIO_TogglePin(LED3_GPIO_Port, LED3_Pin);
#define LED_STATUS_TOGGLE	HAL_GPIO_TogglePin(LED4_GPIO_Port, LED4_Pin);

inline uint8_t upper(uint16_t val){
	return (val >> 8) & 0xFF;
};
inline uint8_t lower(uint16_t val){
	return (val & 0xFF);
};

#endif //__UTILS_H__