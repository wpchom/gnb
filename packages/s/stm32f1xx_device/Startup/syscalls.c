/**
 * @copyright   Copyright (c) 2024 Pchom & licensed under Mulan PSL v2
 * @file        syscall.c
 * @brief       stm32f1xx syscalls stubs
 * @date        2024-05-30
 */

/* Include ----------------------------------------------------------------- */
#include "stm32f1xx.h"

/* syscall ----------------------------------------------------------------- */
__attribute__((weak, noreturn)) void _exit(int status)
{
    (void)(status);

    for (;;) {
        __WFI();
    }
}

__attribute__((weak)) int _getpid(void)
{
    return 1;
}

__attribute__((weak)) int _kill(int pid, int sig)
{
    (void)(pid);
    (void)(sig);

    return -1;
}

__attribute__((weak)) int _open(char *path, int flags, ...)
{
    (void)(path);
    (void)(flags);

    /* Pretend like we always fail */
    return -1;
}

__attribute__((weak)) int _close(int file)
{
    (void)(file);

    return -1;
}

__attribute__((weak)) int _write(int file, char *ptr, int len)
{
    (void)(file);

    for (int DataIdx = 0; DataIdx < len; DataIdx++) {
        ITM_SendChar(*ptr++);
    }

    return len;
}

__attribute__((weak)) int _read(int file, char *ptr, int len)
{
    (void)(file);

    for (int DataIdx = 0; DataIdx < len; DataIdx++) {
        *ptr++ = ITM_ReceiveChar();
    }

    return len;
}

__attribute__((weak)) int _lseek(int file, int ptr, int dir)
{
    (void)(file);
    (void)(ptr);
    (void)(dir);

    return 0;
}