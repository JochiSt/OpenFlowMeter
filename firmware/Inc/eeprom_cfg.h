#ifndef __EEPROM_CFG_H__
#define __EEPROM_CFG_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "config.h"

void read_EEPROM_cfg(config_t *cfg, const config_t *default_cfg);

#ifdef __cplusplus
}
#endif

#endif /* __EEPROM_CFG_H__ */
