#ifndef __CONFIG_H__
#define __CONFIG_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>
#include "pcb_version.h"
#include "pid.h"

#define ISATURATION_LSB   3970
#define USATURATION_LSB   3970

extern const float LSB2U;
extern const float LSB2I;

typedef struct {
    float Ugain;
    float Igain;
    float Ubias;  // in V
    float Ibias;  // in mA
} gain_config_t ;

typedef struct {
    /** @defgroup OFM_cfg configuration of the Open Flow Meter
     *  @{
     */
    uint8_t board_ID;             ///< Board ID
    ////////////////////////////////////////////////////////////////////////////
    /** @defgroup intervals
     *  @ingroup OFM_cfg
     *  The intervals, the OFM reports different things. The larger the interval
     *  the longer the time between two updates.
     *
     *  Intervals are counted in TIM2 cycles (125ms).
     *  If the interval is 0xFF, this function is deactivated
     *
     *  @{
     */
    uint8_t interval_CAN_ADC;       ///< interval, the data is reported to CAN
    uint8_t interval_PRINT_UART;    ///< interval, the data is printed on UART
    uint8_t interval_I2C_TMP100;    ///< interval, the TMP100 should be read

    uint8_t interval_I2C_BME680;    ///< internal, the BME680 should be read

    /** @}*/

    ////////////////////////////////////////////////////////////////////////////
    /** @defgroup SMOO parameters
     *  @ingroup OFM_cfg
     *  parameters of the ADC smootings (moving average)
     *  VAL = (val * (SMOO_MAX - SMOO) + Previous_value * SMOO) / SMOO_MAX
     *  @{
     */
    uint8_t SMOO;     ///< smoothing value
    uint8_t SMOO_MAX; ///< maximal smoothing
    /** @}*/

    ////////////////////////////////////////////////////////////////////////////
    /** @defgroup PID parameter
     *  @ingroup OFM_cfg
     *  parameters of the internal PID controller
     *  @{
     */
    union{
        struct { // LSB first
            uint8_t PID0_active : 1;  ///< is PID channel 0 active
            uint8_t PID1_active : 1;  ///< is PID channel 1 active
            uint8_t spare : 6;
        };
        uint8_t raw;
    } PID_flags;

    PID_config_t PID[2]; ///< configuration of PID channels

    /** @}*/

    ////////////////////////////////////////////////////////////////////////////
    /** @defgroup gain configuration
     *  @ingroup OFM_cfg
     *  switchable gain of the voltage and current channel
     *  only the high gain is stored here, the lower gain is always 1
     *  @{
     */
    gain_config_t GAIN[2];

    /** @}*/

    /** @}*/
} config_t;

extern config_t default_cfg;
extern config_t cfg;

void generateDefaultCFG(config_t *cfg);
void printCfg(config_t *cfg);

#ifdef __cplusplus
}
#endif

#endif /* __CONFIG_H__ */
