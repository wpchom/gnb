/*!
    \file    gd32h7xx_redirect.c
    \brief   redirect optional for gd32h7xx

    \version 2023-12-31, V1.2.0, firmware for GD32H7xx
*/

#include "gd32h7xx.h"

void nvic_vector_table_set(uint32_t nvic_vict_tab, uint32_t offset)
{
    (void)(nvic_vict_tab);
    (void)(offset);
}
