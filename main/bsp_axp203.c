#include "bsp_axp203.h"

esp_err_t bsp_axp_checkConnect()
{
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();

    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (AXP_ADDRESS << 1) | WRITE_BIT, ACK_CHECK_EN);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(AXP_IIC_DEV, cmd, 1);
    i2c_cmd_link_delete(cmd);

    return ret;
}

esp_err_t bsp_axp_iic_readReg(uint8_t address, uint8_t *dst)
{
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();

    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (AXP_ADDRESS << 1) | WRITE_BIT, ACK_CHECK_EN);
    i2c_master_write_byte(cmd, address, ACK_CHECK_EN);
    // i2c_master_stop(cmd);
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (AXP_ADDRESS << 1) | READ_BIT, ACK_CHECK_EN);
    i2c_master_read_byte(cmd, dst, NACK_VAL);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(AXP_IIC_DEV, cmd, portMAX_DELAY);
    i2c_cmd_link_delete(cmd);

    return ret;
}
esp_err_t bsp_axp_iic_writeReg(uint8_t address, uint8_t src)
{
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (AXP_ADDRESS << 1) | WRITE_BIT, ACK_CHECK_EN);
    i2c_master_write_byte(cmd, address, ACK_CHECK_EN);
    i2c_master_write_byte(cmd, src, ACK_CHECK_EN);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(AXP_IIC_DEV, cmd, portMAX_DELAY);
    i2c_cmd_link_delete(cmd);
    return ret;
}

esp_err_t bsp_axp_iic_readRegs(uint8_t address, uint16_t len, uint8_t *dst)
{
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();

    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (AXP_ADDRESS << 1) | WRITE_BIT, ACK_CHECK_EN);
    i2c_master_write_byte(cmd, address, ACK_CHECK_EN);
    // i2c_master_stop(cmd);
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (AXP_ADDRESS << 1) | READ_BIT, ACK_CHECK_EN);
    // i2c_master_read_byte(cmd, dst, NACK_VAL);
    i2c_master_read(cmd, dst, len, I2C_MASTER_LAST_NACK);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(AXP_IIC_DEV, cmd, portMAX_DELAY);
    i2c_cmd_link_delete(cmd);

    return ret;
}
esp_err_t bsp_axp_iic_writeRegs(uint8_t address, uint8_t len, uint8_t *src)
{
    i2c_cmd_handle_t cmd = i2c_cmd_link_create();
    i2c_master_start(cmd);
    i2c_master_write_byte(cmd, (AXP_ADDRESS << 1) | I2C_MASTER_WRITE, ACK_CHECK_EN);
    i2c_master_write_byte(cmd, address, ACK_CHECK_EN);
    // i2c_master_write_byte(cmd, src, ACK_CHECK_EN);
    i2c_master_write(cmd, src, len, ACK_CHECK_EN);
    i2c_master_stop(cmd);

    esp_err_t ret = i2c_master_cmd_begin(AXP_IIC_DEV, cmd, portMAX_DELAY);

    i2c_cmd_link_delete(cmd);
    return ret;
}


//