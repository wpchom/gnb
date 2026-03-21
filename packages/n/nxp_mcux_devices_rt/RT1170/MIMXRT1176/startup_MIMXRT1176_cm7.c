/**
 * @copyright   Copyright (c) 2024 Pchom & licensed under Mulan PSL v2
 * @file        startup_MIMXRT1176_cm7.c
 * @brief       MIMXRT1176 cm7 startup source
 * @date        2026-03-12
 */

/* Include ----------------------------------------------------------------- */
#include "MIMXRT1176_cm7.h"

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
#ifndef DRV_CHIP_WITHOUT_IRQ
__attribute__((weak, alias("Default_Handler"))) void DMA0_DMA16_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA1_DMA17_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA2_DMA18_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA3_DMA19_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA4_DMA20_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA5_DMA21_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA6_DMA22_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA7_DMA23_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA8_DMA24_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA9_DMA25_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA10_DMA26_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA11_DMA27_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA12_DMA28_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA13_DMA29_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA14_DMA30_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA15_DMA31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DMA_ERROR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CTI_TRIGGER_OUT0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CTI_TRIGGER_OUT1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CORE_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART7_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART8_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART9_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART10_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART11_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPUART12_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPI2C1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPI2C2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPI2C3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPI2C4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPI2C5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPI2C6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPSPI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPSPI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPSPI3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPSPI4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPSPI5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPSPI6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN1_ERROR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN2_ERROR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAN3_ERROR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FLEXRAM_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void KPP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved68_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPR_IRQ_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void eLCDIF_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LCDIFv2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CSI_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PXP_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MIPI_CSI_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MIPI_DSI_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPU2D_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO6_Combined_0_15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO6_Combined_16_31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DAC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void KEY_MANAGER_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void WDOG2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SNVS_HP_NON_TZ_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SNVS_HP_TZ_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SNVS_PULSE_EVENT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAAM_IRQ0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAAM_IRQ1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAAM_IRQ2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAAM_IRQ3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAAM_RECORVE_ERRPR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CAAM_RTIC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CDOG_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI3_RX_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI3_TX_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI4_RX_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SAI4_TX_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SPDIF_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TMPSNS_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TMPSNS_LOW_HIGH_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TMPSNS_PANIC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void LPSR_LP8_BROWNOUT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved103_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBPHY1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USBPHY2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RDC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO13_Combined_0_31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved110_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DCIC1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void DCIC2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ASRC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FLEXRAM_ECC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void CM7_GPIO2_3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO1_Combined_0_15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO1_Combined_16_31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO2_Combined_0_15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO2_Combined_16_31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO3_Combined_0_15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO3_Combined_16_31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO4_Combined_0_15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO4_Combined_16_31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO5_Combined_0_15_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPIO5_Combined_16_31_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FLEXIO1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FLEXIO2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void WDOG1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void RTWDOG3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EWM_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OCOTP_READ_FUSE_ERROR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void OCOTP_READ_DONE_ERROR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MUA_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPT1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPT2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPT3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPT4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPT5_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void GPT6_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM1_0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM1_1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM1_2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM1_3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM1_FAULT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FLEXSPI1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void FLEXSPI2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SEMC_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USDHC1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USDHC2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USB_OTG2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void USB_OTG1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET_1588_Timer_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET_1G_MAC0_Tx_Rx_1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET_1G_MAC0_Tx_Rx_2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET_1G_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET_1G_1588_Timer_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void XBAR1_IRQ_0_1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void XBAR1_IRQ_2_3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC_ETC_IRQ0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC_ETC_IRQ1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC_ETC_IRQ2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC_ETC_IRQ3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ADC_ETC_ERROR_IRQ_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved166_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved167_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved168_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved169_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved170_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PIT1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PIT2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ACMP1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ACMP2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ACMP3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ACMP4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved177_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved178_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved179_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved180_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENC1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENC2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENC3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENC4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved185_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved186_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TMR1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TMR2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TMR3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void TMR4_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SEMA4_CP0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void SEMA4_CP1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM2_0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM2_1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM2_2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM2_3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM2_FAULT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM3_0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM3_1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM3_2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM3_3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM3_FAULT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM4_0_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM4_1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM4_2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM4_3_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PWM4_FAULT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved208_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved209_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved210_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved211_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved212_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved213_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved214_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void Reserved215_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PDM_HWVAD_EVENT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PDM_HWVAD_ERROR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PDM_EVENT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void PDM_ERROR_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EMVSIM1_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void EMVSIM2_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MECC1_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MECC1_FATAL_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MECC2_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void MECC2_FATAL_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void XECC_FLEXSPI1_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void XECC_FLEXSPI1_FATAL_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void XECC_FLEXSPI2_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void XECC_FLEXSPI2_FATAL_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void XECC_SEMC_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void XECC_SEMC_FATAL_INT_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET_QOS_IRQHandler(void);
__attribute__((weak, alias("Default_Handler"))) void ENET_QOS_PMT_IRQHandler(void);
#endif

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
#ifndef DRV_CHIP_WITHOUT_IRQ
    DMA0_DMA16_IRQHandler,
    DMA1_DMA17_IRQHandler,
    DMA2_DMA18_IRQHandler,
    DMA3_DMA19_IRQHandler,
    DMA4_DMA20_IRQHandler,
    DMA5_DMA21_IRQHandler,
    DMA6_DMA22_IRQHandler,
    DMA7_DMA23_IRQHandler,
    DMA8_DMA24_IRQHandler,
    DMA9_DMA25_IRQHandler,
    DMA10_DMA26_IRQHandler,
    DMA11_DMA27_IRQHandler,
    DMA12_DMA28_IRQHandler,
    DMA13_DMA29_IRQHandler,
    DMA14_DMA30_IRQHandler,
    DMA15_DMA31_IRQHandler,
    DMA_ERROR_IRQHandler,
    CTI_TRIGGER_OUT0_IRQHandler,
    CTI_TRIGGER_OUT1_IRQHandler,
    CORE_IRQHandler,
    LPUART1_IRQHandler,
    LPUART2_IRQHandler,
    LPUART3_IRQHandler,
    LPUART4_IRQHandler,
    LPUART5_IRQHandler,
    LPUART6_IRQHandler,
    LPUART7_IRQHandler,
    LPUART8_IRQHandler,
    LPUART9_IRQHandler,
    LPUART10_IRQHandler,
    LPUART11_IRQHandler,
    LPUART12_IRQHandler,
    LPI2C1_IRQHandler,
    LPI2C2_IRQHandler,
    LPI2C3_IRQHandler,
    LPI2C4_IRQHandler,
    LPI2C5_IRQHandler,
    LPI2C6_IRQHandler,
    LPSPI1_IRQHandler,
    LPSPI2_IRQHandler,
    LPSPI3_IRQHandler,
    LPSPI4_IRQHandler,
    LPSPI5_IRQHandler,
    LPSPI6_IRQHandler,
    CAN1_IRQHandler,
    CAN1_ERROR_IRQHandler,
    CAN2_IRQHandler,
    CAN2_ERROR_IRQHandler,
    CAN3_IRQHandler,
    CAN3_ERROR_IRQHandler,
    FLEXRAM_IRQHandler,
    KPP_IRQHandler,
    Reserved68_IRQHandler,
    GPR_IRQ_IRQHandler,
    eLCDIF_IRQHandler,
    LCDIFv2_IRQHandler,
    CSI_IRQHandler,
    PXP_IRQHandler,
    MIPI_CSI_IRQHandler,
    MIPI_DSI_IRQHandler,
    GPU2D_IRQHandler,
    GPIO6_Combined_0_15_IRQHandler,
    GPIO6_Combined_16_31_IRQHandler,
    DAC_IRQHandler,
    KEY_MANAGER_IRQHandler,
    WDOG2_IRQHandler,
    SNVS_HP_NON_TZ_IRQHandler,
    SNVS_HP_TZ_IRQHandler,
    SNVS_PULSE_EVENT_IRQHandler,
    CAAM_IRQ0_IRQHandler,
    CAAM_IRQ1_IRQHandler,
    CAAM_IRQ2_IRQHandler,
    CAAM_IRQ3_IRQHandler,
    CAAM_RECORVE_ERRPR_IRQHandler,
    CAAM_RTIC_IRQHandler,
    CDOG_IRQHandler,
    SAI1_IRQHandler,
    SAI2_IRQHandler,
    SAI3_RX_IRQHandler,
    SAI3_TX_IRQHandler,
    SAI4_RX_IRQHandler,
    SAI4_TX_IRQHandler,
    SPDIF_IRQHandler,
    TMPSNS_INT_IRQHandler,
    TMPSNS_LOW_HIGH_IRQHandler,
    TMPSNS_PANIC_IRQHandler,
    LPSR_LP8_BROWNOUT_IRQHandler,
    Reserved103_IRQHandler,
    ADC1_IRQHandler,
    ADC2_IRQHandler,
    USBPHY1_IRQHandler,
    USBPHY2_IRQHandler,
    RDC_IRQHandler,
    GPIO13_Combined_0_31_IRQHandler,
    Reserved110_IRQHandler,
    DCIC1_IRQHandler,
    DCIC2_IRQHandler,
    ASRC_IRQHandler,
    FLEXRAM_ECC_IRQHandler,
    CM7_GPIO2_3_IRQHandler,
    GPIO1_Combined_0_15_IRQHandler,
    GPIO1_Combined_16_31_IRQHandler,
    GPIO2_Combined_0_15_IRQHandler,
    GPIO2_Combined_16_31_IRQHandler,
    GPIO3_Combined_0_15_IRQHandler,
    GPIO3_Combined_16_31_IRQHandler,
    GPIO4_Combined_0_15_IRQHandler,
    GPIO4_Combined_16_31_IRQHandler,
    GPIO5_Combined_0_15_IRQHandler,
    GPIO5_Combined_16_31_IRQHandler,
    FLEXIO1_IRQHandler,
    FLEXIO2_IRQHandler,
    WDOG1_IRQHandler,
    RTWDOG3_IRQHandler,
    EWM_IRQHandler,
    OCOTP_READ_FUSE_ERROR_IRQHandler,
    OCOTP_READ_DONE_ERROR_IRQHandler,
    GPC_IRQHandler,
    MUA_IRQHandler,
    GPT1_IRQHandler,
    GPT2_IRQHandler,
    GPT3_IRQHandler,
    GPT4_IRQHandler,
    GPT5_IRQHandler,
    GPT6_IRQHandler,
    PWM1_0_IRQHandler,
    PWM1_1_IRQHandler,
    PWM1_2_IRQHandler,
    PWM1_3_IRQHandler,
    PWM1_FAULT_IRQHandler,
    FLEXSPI1_IRQHandler,
    FLEXSPI2_IRQHandler,
    SEMC_IRQHandler,
    USDHC1_IRQHandler,
    USDHC2_IRQHandler,
    USB_OTG2_IRQHandler,
    USB_OTG1_IRQHandler,
    ENET_IRQHandler,
    ENET_1588_Timer_IRQHandler,
    ENET_1G_MAC0_Tx_Rx_1_IRQHandler,
    ENET_1G_MAC0_Tx_Rx_2_IRQHandler,
    ENET_1G_IRQHandler,
    ENET_1G_1588_Timer_IRQHandler,
    XBAR1_IRQ_0_1_IRQHandler,
    XBAR1_IRQ_2_3_IRQHandler,
    ADC_ETC_IRQ0_IRQHandler,
    ADC_ETC_IRQ1_IRQHandler,
    ADC_ETC_IRQ2_IRQHandler,
    ADC_ETC_IRQ3_IRQHandler,
    ADC_ETC_ERROR_IRQ_IRQHandler,
    Reserved166_IRQHandler,
    Reserved167_IRQHandler,
    Reserved168_IRQHandler,
    Reserved169_IRQHandler,
    Reserved170_IRQHandler,
    PIT1_IRQHandler,
    PIT2_IRQHandler,
    ACMP1_IRQHandler,
    ACMP2_IRQHandler,
    ACMP3_IRQHandler,
    ACMP4_IRQHandler,
    Reserved177_IRQHandler,
    Reserved178_IRQHandler,
    Reserved179_IRQHandler,
    Reserved180_IRQHandler,
    ENC1_IRQHandler,
    ENC2_IRQHandler,
    ENC3_IRQHandler,
    ENC4_IRQHandler,
    Reserved185_IRQHandler,
    Reserved186_IRQHandler,
    TMR1_IRQHandler,
    TMR2_IRQHandler,
    TMR3_IRQHandler,
    TMR4_IRQHandler,
    SEMA4_CP0_IRQHandler,
    SEMA4_CP1_IRQHandler,
    PWM2_0_IRQHandler,
    PWM2_1_IRQHandler,
    PWM2_2_IRQHandler,
    PWM2_3_IRQHandler,
    PWM2_FAULT_IRQHandler,
    PWM3_0_IRQHandler,
    PWM3_1_IRQHandler,
    PWM3_2_IRQHandler,
    PWM3_3_IRQHandler,
    PWM3_FAULT_IRQHandler,
    PWM4_0_IRQHandler,
    PWM4_1_IRQHandler,
    PWM4_2_IRQHandler,
    PWM4_3_IRQHandler,
    PWM4_FAULT_IRQHandler,
    Reserved208_IRQHandler,
    Reserved209_IRQHandler,
    Reserved210_IRQHandler,
    Reserved211_IRQHandler,
    Reserved212_IRQHandler,
    Reserved213_IRQHandler,
    Reserved214_IRQHandler,
    Reserved215_IRQHandler,
    PDM_HWVAD_EVENT_IRQHandler,
    PDM_HWVAD_ERROR_IRQHandler,
    PDM_EVENT_IRQHandler,
    PDM_ERROR_IRQHandler,
    EMVSIM1_IRQHandler,
    EMVSIM2_IRQHandler,
    MECC1_INT_IRQHandler,
    MECC1_FATAL_INT_IRQHandler,
    MECC2_INT_IRQHandler,
    MECC2_FATAL_INT_IRQHandler,
    XECC_FLEXSPI1_INT_IRQHandler,
    XECC_FLEXSPI1_FATAL_INT_IRQHandler,
    XECC_FLEXSPI2_INT_IRQHandler,
    XECC_FLEXSPI2_FATAL_INT_IRQHandler,
    XECC_SEMC_INT_IRQHandler,
    XECC_SEMC_FATAL_INT_IRQHandler,
    ENET_QOS_IRQHandler,
    ENET_QOS_PMT_IRQHandler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    Default_Handler,
    (void *)0xFFFFFFFF,
#endif
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

__attribute__((__noreturn__)) void DRV_CHIP_JumpIntoDFU(void)
{
    DRV_CHIP_JumpIntoVectorAddress(0x1FFFF000);
}

__attribute__((__noreturn__)) void DRV_CHIP_SystemReset(void)
{
    NVIC_SystemReset();
}

// gcc
__attribute__((weak, naked, __noreturn__)) void _start(void)
{
    __asm volatile("bl     main");
    __asm volatile("b      .");
}

__attribute__((naked, __noreturn__)) void _exit(int status)
{
    (void)(status);
    __asm volatile("b      .");
}
