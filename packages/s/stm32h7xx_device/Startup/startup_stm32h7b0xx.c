/**
 * @copyright   Copyright (c) 2024 Pchom & licensed under Mulan PSL v2
 * @file        startup_stm32h7b0xx.c
 * @brief       stm32h7b0xx startup source
 * @date        2024-05-30
 */
/* Include ----------------------------------------------------------------- */
#include "stm32h7b0xx.h"

/* Reference --------------------------------------------------------------- */
void __INITIAL_SP(void);
void __STACK_LIMIT(void);
void Reset_Handler(void);

/* Handler ----------------------------------------------------------------- */
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

/* Exception --------------------------------------------------------------- */
__attribute__((weak, alias("Default_Handler"))) void NMI_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void HardFault_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void MemManage_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void BusFault_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void UsageFault_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void SVC_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void DebugMon_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void PendSV_Handler(void);
__attribute__((weak, alias("Default_Handler"))) void SysTick_Handler(void);

/* Interrupt --------------------------------------------------------------- */
__attribute__((weak, alias("Default_Handler"))) void WWDG_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PVD_PVM_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RTC_TAMP_STAMP_CSS_LSE_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RTC_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FLASH_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RCC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Stream0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Stream1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Stream2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Stream3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Stream4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Stream5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Stream6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FDCAN1_IT0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FDCAN2_IT0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FDCAN1_IT1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FDCAN2_IT1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI9_5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM1_BRK_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM1_UP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM1_TRG_COM_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM1_CC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C1_EV_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C1_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C2_EV_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C2_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EXTI15_10_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RTC_Alarm_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM8_BRK_TIM12_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM8_UP_TIM13_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM8_TRG_COM_TIM14_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM8_CC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_Stream7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FMC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SDMMC1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM6_DAC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_Stream0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_Stream1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_Stream2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_Stream3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_Stream4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FDCAN_CAL_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM1_FLT4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM1_FLT5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM1_FLT6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM1_FLT7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_Stream5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_Stream6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_Stream7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C3_EV_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C3_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OTG_HS_EP1_OUT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OTG_HS_EP1_IN_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OTG_HS_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OTG_HS_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DCMI_PSSI_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CRYP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void HASH_RNG_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FPU_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART8_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPI6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LTDC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LTDC_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2D_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OCTOSPI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPTIM1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CEC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C4_EV_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void I2C4_ER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPDIF_RX_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMAMUX1_OVR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM1_FLT0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM1_FLT1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM1_FLT2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DFSDM1_FLT3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SWPMI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM16_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TIM17_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MDIOS_WKUP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MDIOS_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void JPEG_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MDMA_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SDMMC2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void HSEM1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DAC2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMAMUX2_OVR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA2_Channel0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA2_Channel1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA2_Channel2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA2_Channel3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA2_Channel4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA2_Channel5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA2_Channel6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA2_Channel7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void COMP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPTIM2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPTIM3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void UART9_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USART10_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CRS_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ECC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DTS_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void WAKEUP_PIN_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OCTOSPI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OTFDEC1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OTFDEC2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GFXMMU_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void BDMA1_IRQHandler(void);

/* Vector ------------------------------------------------------------------ */
static void (*__VECTOR_TABLE[])(void) __VECTOR_TABLE_ATTRIBUTE = {
    // Exception
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
    // Interrupt
    WWDG_IRQHandler,
    PVD_PVM_IRQHandler,
    RTC_TAMP_STAMP_CSS_LSE_IRQHandler,
    RTC_WKUP_IRQHandler,
    FLASH_IRQHandler,
    RCC_IRQHandler,
    EXTI0_IRQHandler,
    EXTI1_IRQHandler,
    EXTI2_IRQHandler,
    EXTI3_IRQHandler,
    EXTI4_IRQHandler,
    DMA1_Stream0_IRQHandler,
    DMA1_Stream1_IRQHandler,
    DMA1_Stream2_IRQHandler,
    DMA1_Stream3_IRQHandler,
    DMA1_Stream4_IRQHandler,
    DMA1_Stream5_IRQHandler,
    DMA1_Stream6_IRQHandler,
    ADC_IRQHandler,
    FDCAN1_IT0_IRQHandler,
    FDCAN2_IT0_IRQHandler,
    FDCAN1_IT1_IRQHandler,
    FDCAN2_IT1_IRQHandler,
    EXTI9_5_IRQHandler,
    TIM1_BRK_IRQHandler,
    TIM1_UP_IRQHandler,
    TIM1_TRG_COM_IRQHandler,
    TIM1_CC_IRQHandler,
    TIM2_IRQHandler,
    TIM3_IRQHandler,
    TIM4_IRQHandler,
    I2C1_EV_IRQHandler,
    I2C1_ER_IRQHandler,
    I2C2_EV_IRQHandler,
    I2C2_ER_IRQHandler,
    SPI1_IRQHandler,
    SPI2_IRQHandler,
    USART1_IRQHandler,
    USART2_IRQHandler,
    USART3_IRQHandler,
    EXTI15_10_IRQHandler,
    RTC_Alarm_IRQHandler,
    DFSDM2_IRQHandler,
    TIM8_BRK_TIM12_IRQHandler,
    TIM8_UP_TIM13_IRQHandler,
    TIM8_TRG_COM_TIM14_IRQHandler,
    TIM8_CC_IRQHandler,
    DMA1_Stream7_IRQHandler,
    FMC_IRQHandler,
    SDMMC1_IRQHandler,
    TIM5_IRQHandler,
    SPI3_IRQHandler,
    UART4_IRQHandler,
    UART5_IRQHandler,
    TIM6_DAC_IRQHandler,
    TIM7_IRQHandler,
    DMA2_Stream0_IRQHandler,
    DMA2_Stream1_IRQHandler,
    DMA2_Stream2_IRQHandler,
    DMA2_Stream3_IRQHandler,
    DMA2_Stream4_IRQHandler,
    0,
    0,
    FDCAN_CAL_IRQHandler,
    DFSDM1_FLT4_IRQHandler,
    DFSDM1_FLT5_IRQHandler,
    DFSDM1_FLT6_IRQHandler,
    DFSDM1_FLT7_IRQHandler,
    DMA2_Stream5_IRQHandler,
    DMA2_Stream6_IRQHandler,
    DMA2_Stream7_IRQHandler,
    USART6_IRQHandler,
    I2C3_EV_IRQHandler,
    I2C3_ER_IRQHandler,
    OTG_HS_EP1_OUT_IRQHandler,
    OTG_HS_EP1_IN_IRQHandler,
    OTG_HS_WKUP_IRQHandler,
    OTG_HS_IRQHandler,
    DCMI_PSSI_IRQHandler,
    CRYP_IRQHandler,
    HASH_RNG_IRQHandler,
    FPU_IRQHandler,
    UART7_IRQHandler,
    UART8_IRQHandler,
    SPI4_IRQHandler,
    SPI5_IRQHandler,
    SPI6_IRQHandler,
    SAI1_IRQHandler,
    LTDC_IRQHandler,
    LTDC_ER_IRQHandler,
    DMA2D_IRQHandler,
    SAI2_IRQHandler,
    OCTOSPI1_IRQHandler,
    LPTIM1_IRQHandler,
    CEC_IRQHandler,
    I2C4_EV_IRQHandler,
    I2C4_ER_IRQHandler,
    SPDIF_RX_IRQHandler,
    0,
    0,
    0,
    0,
    DMAMUX1_OVR_IRQHandler,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    DFSDM1_FLT0_IRQHandler,
    DFSDM1_FLT1_IRQHandler,
    DFSDM1_FLT2_IRQHandler,
    DFSDM1_FLT3_IRQHandler,
    0,
    SWPMI1_IRQHandler,
    TIM15_IRQHandler,
    TIM16_IRQHandler,
    TIM17_IRQHandler,
    MDIOS_WKUP_IRQHandler,
    MDIOS_IRQHandler,
    JPEG_IRQHandler,
    MDMA_IRQHandler,
    0,
    SDMMC2_IRQHandler,
    HSEM1_IRQHandler,
    0,
    DAC2_IRQHandler,
    DMAMUX2_OVR_IRQHandler,
    BDMA2_Channel0_IRQHandler,
    BDMA2_Channel1_IRQHandler,
    BDMA2_Channel2_IRQHandler,
    BDMA2_Channel3_IRQHandler,
    BDMA2_Channel4_IRQHandler,
    BDMA2_Channel5_IRQHandler,
    BDMA2_Channel6_IRQHandler,
    BDMA2_Channel7_IRQHandler,
    COMP_IRQHandler,
    LPTIM2_IRQHandler,
    LPTIM3_IRQHandler,
    UART9_IRQHandler,
    USART10_IRQHandler,
    LPUART1_IRQHandler,
    0,
    CRS_IRQHandler,
    ECC_IRQHandler,
    0,
    DTS_IRQHandler,
    0,
    WAKEUP_PIN_IRQHandler,
    OCTOSPI2_IRQHandler,
    OTFDEC1_IRQHandler,
    OTFDEC2_IRQHandler,
    GFXMMU_IRQHandler,
    BDMA1_IRQHandler
};

/* Function ---------------------------------------------------------------- */
__attribute__((naked, noreturn)) void Reset_Handler(void)
{
    __disable_irq();

    __set_MSP((uint32_t)(&__INITIAL_SP));

    SystemInit();

    SCB->VTOR = (uint32_t)__VECTOR_TABLE;

    __DSB();
    __ISB();

    __enable_irq();

    __PROGRAM_START();
}
