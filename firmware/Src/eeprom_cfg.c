
#include "eeprom_cfg.h"
#include "i2c_utils.h"    // access to I2C EEPROM
#include "config.h"       // values for default configuration

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
    union{
        struct {
            uint8_t PID0_active : 1;
            uint8_t PID1_active : 1;
            uint8_t spare : 6;
        };
        uint8_t raw;
    } PID_flags;

    uint8_t PID0_T; // temperature setpoint
    uint8_t PID0_P;
    uint8_t PID0_I;
    uint8_t PID0_D;

    uint8_t PID1_T;
    uint8_t PID1_P;
    uint8_t PID1_I;
    uint8_t PID1_D;
    /** @}*/


    /** @}*/
} config;

void read_EEPROM_cfg(){

}


