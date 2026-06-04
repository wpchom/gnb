#ifndef __MDS_LVGL_H__
#define __MDS_LVGL_H__

#include "mds/sys.h"

#define LV_OS_MDS 254

extern const MDS_LOG_Module_t G_MDS_LOG_MODULE_lvgl;

#define LV_MDS_LOG_PRINT(_lvl, _fmt, ...)                                                          \
    do {                                                                                           \
        if (_lvl <= (LV_LOG_LEVEL_NUM - LV_LOG_LEVEL)) {                                           \
            static __attribute__((section(__LOG_FORMAT_SECTION_STR(_lvl))))                        \
            const char __logfmt[] = _fmt "\n";                                                     \
            MDS_LOG_ModulePrintf(&G_MDS_LOG_MODULE_lvgl, _lvl,                                     \
                                 __LOG_ARGUMENT_SIZE(__VA_ARGS__) / sizeof(int32_t), __logfmt,     \
                                 ##__VA_ARGS__);                                                   \
        }                                                                                          \
    } while (0)

typedef struct {
    MDS_Thread_t *thread;
} lv_thread_t;

typedef struct {
    MDS_Mutex_t *mutex;
} lv_mutex_t;

typedef struct {
    MDS_Semaphore_t *sem;
} lv_thread_sync_t;

#endif /* __MDS_LVGL_H__ */
