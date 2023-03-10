
#include "utils.h"

uint8_t upper(uint16_t val){
	return (val >> 8) & 0xFF;
};
uint8_t lower(uint16_t val){
	return (val & 0xFF);
};

/**
 * convert the resistance of a PT100 into its temperature
 * @param resistance PT100 resistance
 * @return temperature derived from the given resistance
 */
float convertPT100_R2T(float resistance){
    const float A = 3.9083e-3;
    //const float B = -5.775e-7;
    const float R0 = 100;
    return (resistance - R0)/(R0 * A);
}

/**
 * calculate the voltage before the biases amplifier
 * @param Ubias bias voltage
 * @param Uadc measured voltage of the ADC (amplifier output)
 * @param R1 gain setting resistor (upper)
 * @param R2 gain setting resistor (lower)
 */
float getVoltageBeforeAmplifier(float Uadc, float Ubias, float R1, float R2){
  return (R1 * Ubias + R2 * Uadc)/(R1 + R2);
}
