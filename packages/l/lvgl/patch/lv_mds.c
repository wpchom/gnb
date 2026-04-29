#include "osal/lv_os_private.h"
#include "misc/lv_log.h"

MDS_LOG_MODULE_DEFINE(lvgl);

#define THREAD_TIMESLICE MDS_TIMEOUT_MS(20U)

/**
 * Create a new thread
 * @param thread        a variable in which the thread will be stored
 * @param name          the name of the thread
 * @param prio          priority of the thread
 * @param callback      function of the thread
 * @param stack_size    stack size in bytes
 * @param user_data     arbitrary data, will be available in the callback
 * @return              LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_thread_init(lv_thread_t *thread, const char *const name, lv_thread_prio_t prio,
                           void (*callback)(void *), size_t stack_size, void *user_data)
{
    MDS_ThreadEntry_t entry = (MDS_ThreadEntry_t)(uintptr_t)callback;

    thread->thread =
        MDS_ThreadCreate(name, entry, MDS_ARG_WITH(user_data), stack_size,
                         MDS_THREAD_PRIORITY(LV_THREAD_PRIO_HIGHEST - prio), THREAD_TIMESLICE);
    if (thread->thread == NULL) {
        MDS_LOG_E("thead create fail");
        return (LV_RESULT_INVALID);
    }

    MDS_Err_t err = MDS_ThreadStartup(thread->thread);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        MDS_ThreadDestroy(thread->thread);
        thread->thread = NULL;
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Delete a thread
 * @param thread        the thread to delete
 * @return              LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_thread_delete(lv_thread_t *thread)
{
    MDS_Err_t err = MDS_ThreadDestroy(thread->thread);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    thread->thread = NULL;

    return (LV_RESULT_OK);
}

/**
 * Create a mutex
 * @param mutex         a variable in which the thread will be stored
 * @return              LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_mutex_init(lv_mutex_t *mutex)
{
    mutex->mutex = MDS_MutexCreate("lvmtx");
    if (mutex->mutex == NULL) {
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Lock a mutex
 * @param mutex         the mutex to lock
 * @return              LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_mutex_lock(lv_mutex_t *mutex)
{
    MDS_Err_t err = MDS_MutexAcquire(mutex->mutex, MDS_TIMEOUT_FOREVER);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Lock a mutex from interrupt
 * @param mutex         the mutex to lock
 * @return              LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_mutex_lock_isr(lv_mutex_t *mutex)
{
    MDS_Err_t err = MDS_MutexAcquire(mutex->mutex, MDS_TIMEOUT_NOWAIT);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Unlock a mutex
 * @param mutex         the mutex to unlock
 * @return              LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_mutex_unlock(lv_mutex_t *mutex)
{
    MDS_Err_t err = MDS_MutexRelease(mutex->mutex);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Delete a mutex
 * @param mutex         the mutex to delete
 * @return              LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_mutex_delete(lv_mutex_t *mutex)
{
    MDS_Err_t err = MDS_MutexDestroy(mutex->mutex);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    mutex->mutex = NULL;

    return (LV_RESULT_OK);
}

/**
 * Create a thread synchronization object
 * @param sync          a variable in which the sync will be stored
 * @return              LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_thread_sync_init(lv_thread_sync_t *sync)
{
    sync->sem = MDS_SemaphoreCreate("lvsem", 0, 1);
    if (sync->sem == NULL) {
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Wait for a "signal" on a sync object
 * @param sync      a sync object
 * @return          LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_thread_sync_wait(lv_thread_sync_t *sync)
{
    MDS_Err_t err = MDS_SemaphoreAcquire(sync->sem, MDS_TIMEOUT_FOREVER);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Send a wake-up signal to a sync object
 * @param sync      a sync object
 * @return          LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_thread_sync_signal(lv_thread_sync_t *sync)
{
    MDS_Err_t err = MDS_SemaphoreRelease(sync->sem);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Send a wake-up signal to a sync object from interrupt
 * @param sync      a sync object
 * @return          LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_thread_sync_signal_isr(lv_thread_sync_t *sync)
{
    MDS_Err_t err = MDS_SemaphoreRelease(sync->sem);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    return (LV_RESULT_OK);
}

/**
 * Delete a sync object
 * @param sync      a sync object to delete
 * @return          LV_RESULT_OK: success; LV_RESULT_INVALID: failure
 */
lv_result_t lv_thread_sync_delete(lv_thread_sync_t *sync)
{
    MDS_Err_t err = MDS_SemaphoreDestroy(sync->sem);
    if (!MDS_ErrIsSame(err, MDS_EOK)) {
        //
        return (LV_RESULT_INVALID);
    }

    sync->sem = NULL;

    return (LV_RESULT_OK);
}
