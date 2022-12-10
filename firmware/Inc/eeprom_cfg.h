/* Define to prevent recursive inclusion -------------------------------------*/
#ifndef __EEPROM_CFG_H__
#define __EEPROM_CFG_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "i2c_utils.h"

struct eeprom_cfg {
    /** @defgroup OFM_cfg configuration of the Open Flow Meter
     *  @{
     */
    uint8_t board_ID;           ///< Board ID
    ////////////////////////////////////////////////////////////////////////////
    /** @defgroup intervals
     *  @ingroup OFM_cfg
     *  The intervals, the OFM reports different things. The larger the interval
     *  the longer the time between two updates.
     *  @{
     */
    uint8_t interval_OFM;       ///< interval, the OFM read its data and the PID
                                ///< loop is triggered
    uint8_t interval_OFM_report;///< interval, the OFM reports
    uint8_t interval_TMP100;    ///< interval, the TMP100 should be read
    uint8_t interval_BME680;    ///< internal, the BME680 should be read
    /** @}*/
    ////////////////////////////////////////////////////////////////////////////
    /** @defgroup PID parameter
     *  @ingroup OFM_cfg
     *  parameters of the internal PID controller
     *  @{
     */
    bool PID0_active;
    float PID0_T;
    uint8_t PID0_P;
    uint8_t PID0_I;
    uint8_t PID0_D;

    bool PID1_active;
    float PID1_T;
    uint8_t PID1_P;
    uint8_t PID1_I;
    uint8_t PID1_D;
    /** @}*/


    /** @}*/
};

#ifdef __cplusplus
}
#endif

#endif /* __EEPROM_CFG_H__ */

/************************ (C) COPYRIGHT STMicroelectronics *****END OF FILE****/
