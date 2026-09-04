#include <stdio.h>
#include <stdint.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_err.h"

#define LATCH_PIN  GPIO_NUM_20
#define CLOCK_PIN  GPIO_NUM_22
#define DATA_PIN   GPIO_NUM_21
#define OE_PIN     GPIO_NUM_7


// Equivalent to Arduino shiftOut(..., MSBFIRST, ...)
static void shift_out_byte(uint8_t data)
{
    for (int i = 7; i >= 0; i--)
    {
        gpio_set_level(DATA_PIN, (data >> i) & 0x01);

        gpio_set_level(CLOCK_PIN, 1);
        gpio_set_level(CLOCK_PIN, 0);
    }
}


// Exactly the same two shiftOut() calls as your original code
static void send_data(uint16_t Data)
{
    gpio_set_level(LATCH_PIN, 0);

    shift_out_byte((Data >> 8) & 0xFF);
    shift_out_byte(Data & 0xFF);

    gpio_set_level(LATCH_PIN, 1);
}


void app_main(void)
{
    gpio_config_t config = {
        .pin_bit_mask =
            (1ULL << LATCH_PIN) |
            (1ULL << CLOCK_PIN) |
            (1ULL << DATA_PIN) |
            (1ULL << OE_PIN),

        .mode = GPIO_MODE_OUTPUT,
        .pull_up_en = GPIO_PULLUP_DISABLE,
        .pull_down_en = GPIO_PULLDOWN_DISABLE,
        .intr_type = GPIO_INTR_DISABLE
    };

    ESP_ERROR_CHECK(gpio_config(&config));

    gpio_set_level(LATCH_PIN, 0);
    gpio_set_level(CLOCK_PIN, 0);
    gpio_set_level(DATA_PIN, 0);

    // Same OE pin as your original program.
    // Your original didn't use OE, so leave it LOW.
    gpio_set_level(OE_PIN, 0);


    while (1)
    {
        uint16_t Data;


    
        Data = 0b1111111111111111;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111111111111100;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111111111111000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111111111110000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111111111100000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111111111000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111111110000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111111100000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111111000000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111110000000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111100000000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1111000000000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1110000000000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1100000000000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b1000000000000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));


        Data = 0b0000000000000000;
        send_data(Data);
        vTaskDelay(pdMS_TO_TICKS(100));
    }
}