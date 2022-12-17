#ifndef __CONFIG_H__
#define __CONFIG_H__

#ifdef __cplusplus
extern "C" {
#endif

#include "eeprom_cfg.h"

extern eeprom_cfg default_cfg;
extern eeprom_cfg cfg;

void generateDefaultCFG();

#ifdef __cplusplus
}
#endif

#endif /* __CONFIG_H__ */
