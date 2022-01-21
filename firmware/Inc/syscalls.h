#ifndef __SYSCALLS_H__
#define __SYSCALLS_H__

#include <stdio.h>
#include <stdarg.h>
#include <string.h>

#ifdef __cplusplus
extern "C" {
#endif
	int _write(int file, char *data, int len);

#ifdef __cplusplus
}
#endif

#endif /* __SYSCALLS_H__ */