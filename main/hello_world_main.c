/* Hello World Example

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include "sdkconfig.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "esp_system.h"
#include "esp_spi_flash.h"
#include "driver/gpio.h"
#include "esp_log.h"
#include "driver/i2c.h"
#include "esp_err.h"
#include <stdint.h>
#include <string.h>
#include "bsp_axp203.h"

#define EGL_IIC_DEV 1

#define I2C_MASTER_TX_BUF_DISABLE 0 /*!< I2C master doesn't need buffer */
#define I2C_MASTER_RX_BUF_DISABLE 0 /*!< I2C master doesn't need buffer */
#define WRITE_BIT I2C_MASTER_WRITE  /*!< I2C master write */
#define READ_BIT I2C_MASTER_READ    /*!< I2C master read */
#define ACK_CHECK_EN 0x1            /*!< I2C master will check ack from slave*/
#define ACK_CHECK_DIS 0x0           /*!< I2C master will not check ack from slave */
#define ACK_VAL I2C_MASTER_ACK      /*!< I2C ack value */
#define NACK_VAL I2C_MASTER_NACK    /*!< I2C nack value */

SemaphoreHandle_t xsemiicfree;

esp_err_t egl_iic_init(uint8_t sda, uint8_t scl, uint32_t freq)
{
    // i2c_config_t conf;
    // conf.mode = I2C_MODE_MASTER;
    // conf.sda_io_num = sda;
    // conf.sda_pullup_en = GPIO_PULLUP_ENABLE;
    // conf.scl_io_num = scl;
    // conf.scl_pullup_en = GPIO_PULLUP_ENABLE;
    // conf.master.clk_speed = freq;

    i2c_config_t conf = {
        .mode = I2C_MODE_MASTER,
        .sda_io_num = sda,
        .scl_io_num = scl,
        .sda_pullup_en = GPIO_PULLUP_ENABLE,
        .scl_pullup_en = GPIO_PULLUP_ENABLE,
        .master.clk_speed = freq,
        .clk_flags = 0,
    };
    i2c_param_config(EGL_IIC_DEV, &conf);
    return i2c_driver_install(EGL_IIC_DEV, conf.mode, I2C_MASTER_RX_BUF_DISABLE, I2C_MASTER_TX_BUF_DISABLE, 0);
}

void vtaskreadser(void *args)
{
    int waddr,wdata;

    char inbuf[100];
    char tmp[4];
    int inbuf_cnt = 0;
    for (;;)
    {
        int ret = getchar();
        if (ret > 0)
        {
            // ESP_LOGI("main","%c",ret);
            inbuf[inbuf_cnt] = (ret & 0xff);
            inbuf_cnt++;
            if (inbuf_cnt > 7)
            {
                // ESP_LOGI("main","ac");
                // ESP_LOGI("main","%.7s",inbuf);
                inbuf_cnt = 0;
                if (inbuf[0] == 'Q' && inbuf[7] == 'Z')
                {
                    strncpy(tmp, inbuf + 1, 3);
                    tmp[4] = 0;
                    waddr = atoi(tmp);
                    strncpy(tmp, inbuf + 4, 3);
                    tmp[4] = 0;
                    wdata = atoi(tmp);
                    //ESP_LOGI("main","waddr : %02x    wdata : %02x",waddr,wdata);
                    if (bsp_axp_checkConnect() == ESP_OK)
                    {

                        uint8_t wa = waddr;
                        uint8_t wd = wdata;
                        // ESP_LOGI("main", "waddr : %02x    wdata : %02x", wa, wd);
                        if (xSemaphoreTake(xsemiicfree, portMAX_DELAY) == pdPASS)
                        {
                            ESP_ERROR_CHECK(bsp_axp_iic_writeReg(wa, wd));
                            xSemaphoreGive(xsemiicfree);
                        }
                        
                    }
                }
            }
        }
        vTaskDelay(1);
    }
}

void app_main(void)
{
    //printf("Hello world!\n");
    xsemiicfree = xSemaphoreCreateMutex();
    xSemaphoreGive(xsemiicfree);
    gpio_reset_pin(GPIO_NUM_13);
    gpio_set_direction(GPIO_NUM_13,GPIO_MODE_OUTPUT);
    

    ESP_ERROR_CHECK(egl_iic_init(26, 27, 400 * 1000)); // sda,scl,freq

    xTaskCreatePinnedToCore(vtaskreadser,"rs",4096,NULL,2,NULL,1);

    uint8_t axpRegs[256];
    while (1)
    {
        //ESP_ERROR_CHECK(bsp_axp_iic_writeReg(0x32, axpRegs[0x32] | 0x80));
        if (xSemaphoreTake(xsemiicfree, portMAX_DELAY) == pdPASS)
        {
            if (bsp_axp_checkConnect() != ESP_OK)
            {
                // ESP_LOGW("axp","axp iic disconnect");
                for (size_t i = 0; i < 0xff; i++)
                {
                    printf("XX");
                }
            }
            else
            {
                bsp_axp_iic_readRegs(0x00, 0x100, axpRegs);
                for (size_t i = 0; i < 0xff; i++)
                {
                    printf("%02x", axpRegs[i]);
                }
            }
            xSemaphoreGive(xsemiicfree);
        }

        printf("\n");
        vTaskDelay(50);
        

        //bsp_axp_iic_readRegs(0x00,255,axpRegs);

        // printf("xx\t");
        // for (size_t i = 0; i < 16; i++)
        // {
        //     printf(" %1x\t",i);
        // }
        // printf("\r\n");

        // for (size_t i = 0; i < 16; i++)
        // {
        //     printf("%02x\t",(i<<4));
        //     for (size_t j = 0; j < 16; j++)
        //     {
        //         printf("%02x\t", axpRegs[(i * 16) + j]);
        //     }
        //     printf("\r\n");
        // }

        // egl_iic_writeReg(0x34, 0x32, axpRegs[0x32] | 0x80);//poff
        

        // vTaskDelay(1000); // 10s
        // printf("\r\n");
        // printf("\r\n");
        // printf("\r\n");
        // printf("\r\n");
        // printf("\r\n");
        // printf("\r\n");
        
    }
}
/*
00      01      02      03      04      05      06      07      08      09      0a      0b      0c      0d      0e      0f
21      30      00      41      00      00      00      00      00      00      00      00      00      00      00      00
01      00      17      00      00      00      00      00      00      00      00      00      00      00      00      00
00      00      00      16      00      00      00      68      cf      18      00      00      00      00      00      00
61      03      42      c2      45      22      9d      08      a5      1f      68      5f      fc      16      00      00
d8      ff      03      01      00      00      00      00      24      80      00      03      00      00      00      00
b0      05      00      00      00      00      00      00      00      00      00      00      00      00      67      07
8a      01      00      00      00      00      00      00      00      00      00      00      00      00      00      00
00      00      00      00      00      00      00      00      b0      05      00      00      00      00      8a      01
e0      fd      83      80      32      00      ff      00      00      00      00      00      00      00      00      21
07      a5      07      07      00      02      00      00      00      00      00      00      00      00      00      00
00      00      00      00      00      00      00      00      b0      05      00      00      00      00      8a      01
00      00      00      00      00      00      00      00      00      7f      00      ba      00      00      00      00
01      01      02      04      07      0d      10      1a      24      2e      35      3d      49      54      5c      63
00      00      00      00      00      00      00      00      00      00      00      00      00      00      00      00
00      00      00      00      00      00      00      00      00      00      00      00      00      00      00      00
41      00      80      03      00      00      00      00      00      00      00      00      00      00      00      00
*/



/*
xx       0       1       2       3       4       5       6       7       8       9       a       b       c       d       e       f
00      c1      10      00      41      00      00      00      00      00      00      00      00      00      00      00      00
10      01      00      17      00      00      00      00      00      00      00      00      00      00      00      00      00
20      00      00      00      16      00      00      00      68      cf      18      00      00      00      00      00      00
30      61      03      42      c2      45      22      9d      08      a5      1f      68      5f      fc      16      00      00
40      d8      ff      03      01      00      00      00      00      44      40      00      00      00      00      00      00
50      00      00      00      00      00      00      00      00      00      00      00      00      00      00      68      05
60      df      04      3e      08      00      00      00      00      00      00      00      00      00      00      00      00
70      00      00      00      00      00      00      00      00      00      00      00      00      00      00      df      04
80      e0      fd      83      80      32      00      ff      00      00      00      00      00      00      00      00      21
90      07      a5      07      07      00      02      00      00      00      00      00      00      00      00      00      00
a0      00      00      00      00      00      00      00      00      00      00      00      00      00      00      df      04
b0      00      00      00      00      00      00      00      00      00      7f      00      ba      00      00      00      00
c0      01      01      02      04      07      0d      10      1a      24      2e      35      3d      49      54      5c      63
d0      00      00      00      00      00      00      00      00      00      00      00      00      00      00      00      00
e0      00      00      00      00      00      00      00      00      00      00      00      00      00      00      00      00
f0      41      00      80      03      00      00      00      00      00      00      00      00      00      00      00      00
*/