#pragma once

/**
 * PCB v1 compatibility mode
 */
#define PCB_V1
/******************************************************************************/
/**
 * PCB v2 compatibility mode
 * enables:
 *  - dual gain ADC readout
 *  - I2C sensor readout
 */
//#define PCB_V2
#if defined(PCB_V2)
#undef PCB_V1
#endif
/******************************************************************************/
/**
 * PCB v3 compatibility mode
 * enables:
 *  - dual gain ADC readout
 *  - offset for ADC / differential amplifier
 *  - I2C sensor readout
 */
//#define PCB_V3
#if defined(PCB_V3)
#undef PCB_V1
#undef PCB_V2
#endif
