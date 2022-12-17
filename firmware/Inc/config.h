#ifndef __CONFIG_H__
#define __CONFIG_H__

#ifdef __cplusplus
extern "C" {
#endif

#include <stdint.h>

typedef struct {
    uint8_t PID_T;  ///< temperature setpoint
    uint8_t PID_P;  ///< proportional part
    uint8_t PID_I;  ///< integral part
    uint8_t PID_D;  ///< differential part
} PID_config_t;

typedef struct  {
    /** @defgroup OFM_cfg configuration of the Open Flow Meter
     *  @{
     */
    uint8_t board_ID;           ///< Board ID
    ////////////////////////////////////////////////////////////////////////////
    /** @defgroup intervals
     *  @ingroup OFM_cfg
     *  The intervals, the OFM reports different things. The larger the interval
     *  the longer the time between two updates.
     *
     *  Intervals are counted in TIM2 cycles.
     *  If the interval is 0xFF, this function is deactivated
     *  @{
     */
    uint8_t interval_OFM_PID;   ///< interval, the PID loop is triggered
    uint8_t interval_OFM_report;///< interval, the OFM reports via CANbus

    uint8_t interval_TMP100;    ///< interval, the TMP100 should be read
    uint8_t interval_BME680;    ///< internal, the BME680 should be read

    /** @}*/
    ////////////////////////////////////////////////////////////////////////////
    /** @defgroup PID parameter
     *  @ingroup OFM_cfg
     *  parameters of the internal PID controller
     *  @{
     */
    union{
        struct {
            uint8_t PID0_active : 1;  ///< is PID channel 0 active
            uint8_t PID1_active : 1;  ///< is PID channel 1 active
            uint8_t spare : 6;
        };
        uint8_t raw;
    } PID_flags;

    PID_config_t PID0; ///< configuration of PID channel 0
    PID_config_t PID1; ///< configuration of PID channel 1

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

    /** @}*/
} config_t;

extern config_t default_cfg;
extern config_t cfg;

void generateDefaultCFG();

#ifdef __cplusplus
}
#endif

#endif /* __CONFIG_H__ */
