/**
 * @copyright   Copyright (c) 2024 Pchom & licensed under Mulan PSL v2
 * @file        startup_gd32h7xx.c
 * @brief       gd32h7xx startup source
 * @date        2025-12-24
 */

/* Include ----------------------------------------------------------------- */
#include "gd32h7xx.h"

/* Reference --------------------------------------------------------------- */
void __INITIAL_SP(void);
void __STACK_LIMIT(void);
void Reset_Handler(void);

/* Interrupt --------------------------------------------------------------- */
__attribute__((weak)) void Interrupt_Handler(uintptr_t ipsr)
{
    (void)(ipsr);

    for (;;) {
        __WFI();
    }
}

void Default_Handler(void)
{
    uintptr_t ipsr = __get_IPSR() & IPSR_ISR_Msk;

    Interrupt_Handler(ipsr);
}

__attribute__((weak, alias("Default_Handler"))) void NMI_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void HardFault_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void MemManage_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void BusFault_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void UsageFault_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void SVC_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void DebugMon_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void PendSV_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void SysTick_Handler(void);

__attribute__((weak, alias("Default_Handler"))) void WWDGT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void VAVD_LVD_VOVD_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TAMPER_STAMP_LXTAL_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RTC_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FMC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RCU_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA0_Channel0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA0_Channel1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA0_Channel2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA0_Channel3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA0_Channel4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA0_Channel5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA0_Channel6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC0_1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI5_9_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER0_BRK_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER0_UP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER0_TRG_CMT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER0_Channel_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C0_EV_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C0_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C1_EV_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C1_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI10_15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RTC_Alarm_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER7_BRK_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER7_UP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER7_TRG_CMT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER7_Channel_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA0_Channel7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXMC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SDIO0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER5_DAC_UDR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Channel0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Channel1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Channel2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Channel3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Channel4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET0_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Channel5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Channel6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Channel7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C2_EV_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C2_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBHS0_EP1_OUT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBHS0_EP1_IN_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBHS0_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBHS0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DCI_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAU_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void HAU_TRNG_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FPU_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TLI_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TLI_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void IPA_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OSPI0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C3_EV_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C3_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RSPDIF_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMAMUX_OVR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void HPDF_INT0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void HPDF_INT1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void HPDF_INT2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void HPDF_INT3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER14_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER16_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MDIO_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MDMA_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SDIO1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void HWSEM_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CMP0_1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CTC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RAMECCMU_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OSPI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RTDEC0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RTDEC1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FAC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TMU_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER22_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER23_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER30_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER40_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER41_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER42_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER43_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER44_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER50_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER51_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBHS1_EP1_OUT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBHS1_EP1_IN_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBHS1_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBHS1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET1_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN0_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN0_Message_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN0_Busoff_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN0_Error_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN0_FastError_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN0_TEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN0_REC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_Message_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_Busoff_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_Error_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_FastError_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_TEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_REC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_Message_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_Busoff_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_Error_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_FastError_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_TEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_REC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EFUSE_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C0_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C1_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C2_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C3_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPDTS_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPDTS_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER0_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER7_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER1_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER2_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER3_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER4_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER22_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER23_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER30_DEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIMER31_DEC_IRQHandler(void);

static void (*__VECTOR_TABLE[])(void) __VECTOR_TABLE_ATTRIBUTE = {
    (void *)(&__INITIAL_SP),
    Reset_Handler,
    NMI_Handler,
    HardFault_Handler,
    MemManage_Handler,
    BusFault_Handler,
    UsageFault_Handler,
    0,
    0,
    0,
    0,
    SVC_Handler,
    DebugMon_Handler,
    0,
    PendSV_Handler,
    SysTick_Handler,

    WWDGT_IRQHandler,
    VAVD_LVD_VOVD_IRQHandler,
    TAMPER_STAMP_LXTAL_IRQHandler,
    RTC_WKUP_IRQHandler,
    FMC_IRQHandler,
    RCU_IRQHandler,
    EXTI0_IRQHandler,
    EXTI1_IRQHandler,
    EXTI2_IRQHandler,
    EXTI3_IRQHandler,
    EXTI4_IRQHandler,
    DMA0_Channel0_IRQHandler,
    DMA0_Channel1_IRQHandler,
    DMA0_Channel2_IRQHandler,
    DMA0_Channel3_IRQHandler,
    DMA0_Channel4_IRQHandler,
    DMA0_Channel5_IRQHandler,
    DMA0_Channel6_IRQHandler,
    ADC0_1_IRQHandler,
    0,
    0,
    0,
    0,
    EXTI5_9_IRQHandler,
    TIMER0_BRK_IRQHandler,
    TIMER0_UP_IRQHandler,
    TIMER0_TRG_CMT_IRQHandler,
    TIMER0_Channel_IRQHandler,
    TIMER1_IRQHandler,
    TIMER2_IRQHandler,
    TIMER3_IRQHandler,
    I2C0_EV_IRQHandler,
    I2C0_ER_IRQHandler,
    I2C1_EV_IRQHandler,
    I2C1_ER_IRQHandler,
    SPI0_IRQHandler,
    SPI1_IRQHandler,
    USART0_IRQHandler,
    USART1_IRQHandler,
    USART2_IRQHandler,
    EXTI10_15_IRQHandler,
    RTC_Alarm_IRQHandler,
    0,
    TIMER7_BRK_IRQHandler,
    TIMER7_UP_IRQHandler,
    TIMER7_TRG_CMT_IRQHandler,
    TIMER7_Channel_IRQHandler,
    DMA0_Channel7_IRQHandler,
    EXMC_IRQHandler,
    SDIO0_IRQHandler,
    TIMER4_IRQHandler,
    SPI2_IRQHandler,
    UART3_IRQHandler,
    UART4_IRQHandler,
    TIMER5_DAC_UDR_IRQHandler,
    TIMER6_IRQHandler,
    DMA1_Channel0_IRQHandler,
    DMA1_Channel1_IRQHandler,
    DMA1_Channel2_IRQHandler,
    DMA1_Channel3_IRQHandler,
    DMA1_Channel4_IRQHandler,
    ENET0_IRQHandler,
    ENET0_WKUP_IRQHandler,
    0,
    0,
    0,
    0,
    0,
    DMA1_Channel5_IRQHandler,
    DMA1_Channel6_IRQHandler,
    DMA1_Channel7_IRQHandler,
    USART5_IRQHandler,
    I2C2_EV_IRQHandler,
    I2C2_ER_IRQHandler,
    USBHS0_EP1_OUT_IRQHandler,
    USBHS0_EP1_IN_IRQHandler,
    USBHS0_WKUP_IRQHandler,
    USBHS0_IRQHandler,
    DCI_IRQHandler,
    CAU_IRQHandler,
    HAU_TRNG_IRQHandler,
    FPU_IRQHandler,
    UART6_IRQHandler,
    UART7_IRQHandler,
    SPI3_IRQHandler,
    SPI4_IRQHandler,
    SPI5_IRQHandler,
    SAI0_IRQHandler,
    TLI_IRQHandler,
    TLI_ER_IRQHandler,
    IPA_IRQHandler,
    SAI1_IRQHandler,
    OSPI0_IRQHandler,
    0,
    0,
    I2C3_EV_IRQHandler,
    I2C3_ER_IRQHandler,
    RSPDIF_IRQHandler,
    0,
    0,
    0,
    0,
    DMAMUX_OVR_IRQHandler,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    HPDF_INT0_IRQHandler,
    HPDF_INT1_IRQHandler,
    HPDF_INT2_IRQHandler,
    HPDF_INT3_IRQHandler,
    SAI2_IRQHandler,
    0,
    TIMER14_IRQHandler,
    TIMER15_IRQHandler,
    TIMER16_IRQHandler,
    0,
    MDIO_IRQHandler,
    0,
    MDMA_IRQHandler,
    0,
    SDIO1_IRQHandler,
    HWSEM_IRQHandler,
    0,
    ADC2_IRQHandler,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    CMP0_1_IRQHandler,
    0,
    0,
    0,
    0,
    0,
    0,
    CTC_IRQHandler,
    RAMECCMU_IRQHandler,
    0,
    0,
    0,
    0,
    OSPI1_IRQHandler,
    RTDEC0_IRQHandler,
    RTDEC1_IRQHandler,
    FAC_IRQHandler,
    TMU_IRQHandler,
    0,
    0,
    0,
    0,
    0,
    0,
    TIMER22_IRQHandler,
    TIMER23_IRQHandler,
    TIMER30_IRQHandler,
    TIMER31_IRQHandler,
    TIMER40_IRQHandler,
    TIMER41_IRQHandler,
    TIMER42_IRQHandler,
    TIMER43_IRQHandler,
    TIMER44_IRQHandler,
    TIMER50_IRQHandler,
    TIMER51_IRQHandler,
    USBHS1_EP1_OUT_IRQHandler,
    USBHS1_EP1_IN_IRQHandler,
    USBHS1_WKUP_IRQHandler,
    USBHS1_IRQHandler,
    ENET1_IRQHandler,
    ENET1_WKUP_IRQHandler,
    0,
    CAN0_WKUP_IRQHandler,
    CAN0_Message_IRQHandler,
    CAN0_Busoff_IRQHandler,
    CAN0_Error_IRQHandler,
    CAN0_FastError_IRQHandler,
    CAN0_TEC_IRQHandler,
    CAN0_REC_IRQHandler,
    CAN1_WKUP_IRQHandler,
    CAN1_Message_IRQHandler,
    CAN1_Busoff_IRQHandler,
    CAN1_Error_IRQHandler,
    CAN1_FastError_IRQHandler,
    CAN1_TEC_IRQHandler,
    CAN1_REC_IRQHandler,
    CAN2_WKUP_IRQHandler,
    CAN2_Message_IRQHandler,
    CAN2_Busoff_IRQHandler,
    CAN2_Error_IRQHandler,
    CAN2_FastError_IRQHandler,
    CAN2_TEC_IRQHandler,
    CAN2_REC_IRQHandler,
    EFUSE_IRQHandler,
    I2C0_WKUP_IRQHandler,
    I2C1_WKUP_IRQHandler,
    I2C2_WKUP_IRQHandler,
    I2C3_WKUP_IRQHandler,
    LPDTS_IRQHandler,
    LPDTS_WKUP_IRQHandler,
    TIMER0_DEC_IRQHandler,
    TIMER7_DEC_IRQHandler,
    TIMER1_DEC_IRQHandler,
    TIMER2_DEC_IRQHandler,
    TIMER3_DEC_IRQHandler,
    TIMER4_DEC_IRQHandler,
    TIMER22_DEC_IRQHandler,
    TIMER23_DEC_IRQHandler,
    TIMER30_DEC_IRQHandler,
    TIMER31_DEC_IRQHandler,
};

/* Function ---------------------------------------------------------------- */
__attribute__((weak)) void VectorInit(uintptr_t vectorAddress)
{
    SysTick->CTRL = 0U;
    SysTick->LOAD = 0U;
    SysTick->VAL = 0U;

    for (uint32_t idx = 0; idx < (sizeof(NVIC->ICER) / sizeof(NVIC->ICER[0])); idx++) {
        NVIC->ICER[idx] = 0xFFFFFFFF;
    }

    SCB->VTOR = vectorAddress;
}

__attribute__((naked, noreturn)) void Reset_Handler(void)
{
    __disable_irq();

    __set_MSP((uint32_t)(&__INITIAL_SP));

    SystemInit();

    VectorInit((uintptr_t)__VECTOR_TABLE);

    __enable_irq();

    __PROGRAM_START();
}

__attribute__((noreturn)) void DRV_CHIP_JumpIntoVectorAddress(uintptr_t vectorAddress)
{
    typedef void (*vector_t)(void);
    vector_t *vectorTable = (vector_t *)(vectorAddress);

    __disable_irq();

    __set_MSP((uint32_t)(vectorTable[0]));

    VectorInit(vectorAddress);

    __enable_irq();

    vectorTable[1]();

    for (;;) {
    }
}

__attribute__((noreturn)) void DRV_CHIP_JumpIntoDFU(void)
{
    DRV_CHIP_JumpIntoVectorAddress(0x1FF00000);
}

__attribute__((noreturn)) void DRV_CHIP_SystemReset(void)
{
    NVIC_SystemReset();
}

// gcc
__attribute__((weak, noreturn)) void _exit(int status)
{
    (void)(status);
    for (;;) {
        __WFI();
    }
}
