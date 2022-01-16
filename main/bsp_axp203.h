#ifndef __BSP_AXP203_H__
#define __BSP_AXP203_H__

#include "driver/gpio.h"
#include "driver/i2c.h"
#include "esp_err.h"
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include "esp_log.h"
#include "esp_system.h"

#define AXP_DRV_VBUS -1
#define AXP_IRQ -1
#define AXP_IIC_DEV 1

#define AXP_ADDRESS 0x34

#define AXP_CHECK_CONN

#define I2C_MASTER_TX_BUF_DISABLE 0 /*!< I2C master doesn't need buffer */
#define I2C_MASTER_RX_BUF_DISABLE 0 /*!< I2C master doesn't need buffer */
#define WRITE_BIT I2C_MASTER_WRITE  /*!< I2C master write */
#define READ_BIT I2C_MASTER_READ    /*!< I2C master read */
#define ACK_CHECK_EN 0x1            /*!< I2C master will check ack from slave*/
#define ACK_CHECK_DIS 0x0           /*!< I2C master will not check ack from slave */
#define ACK_VAL I2C_MASTER_ACK      /*!< I2C ack value */
#define NACK_VAL I2C_MASTER_NACK    /*!< I2C nack value */

esp_err_t bsp_axp_checkConnect();

esp_err_t bsp_axp_iic_readReg(uint8_t address, uint8_t *dst);
esp_err_t bsp_axp_iic_writeReg(uint8_t address, uint8_t src);
esp_err_t bsp_axp_iic_readRegs(uint8_t address, uint16_t len, uint8_t *dst);
esp_err_t bsp_axp_iic_writeRegs(uint8_t address, uint8_t len, uint8_t *src);

//
typedef union
{
    struct
    {
        // lsb
        // reg 00h [0..7]
        uint8_t bootSource : 1;              // 1:boot source is ACIN/VBUS
        uint8_t ACIN_VBUSShort : 1;          // 1:ACIN and VBUS short on PCB
        uint8_t batteryCurrentDirection : 1; // 1:charging,0:discharging
        uint8_t VBUSUseable : 1;
        uint8_t VBUSPresence : 1;
        uint8_t ACINUseable : 1;
        uint8_t ACINPresence : 1;
        // reg 01h [0..7]
        uint8_t : 2;
        uint8_t chargingCurrentLow:1;//1:current lower than expected current
        uint8_t batteryActivate:1;//1:already entered activate mode
        uint8_t :1;
        uint8_t batteryExist:1;//1:battery exist
        uint8_t chargeIndication:1;//1:charging
        uint8_t overTemperature:1;//1:OT
        // reg 02h [0..7]
        uint8_t SessionEndStatus : 1;  // Session End Status(1 means valid)
        uint8_t VBUSSessionStatus : 1; // VBUS Session A/B valid (1 means valid)
        uint8_t VBUSValid : 1;         // VBUS Valid or not (1 means valid)
        uint8_t : 5;
        // msb
    } str;
    uint32_t reg;//0x 00 3 2 1
} axp_status_t;

typedef struct
{
    uint8_t dcdc2Enable;
    uint8_t dcdc2Vout;
    uint8_t dcdc3Enable;
    uint8_t dcdc3Vout;
} axp_dcdc_config_t;

typedef struct
{
    uint8_t ldo2Enable;
    uint8_t ldo2Vout;
    uint8_t ldo3Enable;
    uint8_t ldo3Vout;
    uint8_t ldo4Enable;
    uint8_t ldo4Vout;
} axp_ldo_config_t;

typedef struct 
{
    uint8_t chargingEnable;
    uint8_t chargingCVVoltage;
    uint8_t chargingEndCurrent;
    uint8_t chargingCCCurrent;
    uint8_t preChargingTimeOut;
    uint8_t chargingCCTimeOut;
    uint8_t BackupBatteryChargeEnable;
    uint8_t BackupBatteryChargeVoltage;
    uint8_t BackupBatteryChargeCurrent;
}axp_charge_config_t;


#endif