#ifndef __MDS_LVGL_H__
#define __MDS_LVGL_H__

#include "mds_sys.h"

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
