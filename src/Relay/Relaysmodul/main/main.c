#include <stdio.h>
#include <stdint.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "driver/gpio.h"
#include "esp_err.h"

#define LATCH_PIN  GPIO_NUM_20
#define CLOCK_PIN  GPIO_NUM_22
#define DATA_PIN   GPIO_NUM_21
#define OE_PIN     GPIO_NUM_7


// ============================================================
// Send one byte MSB first
// Equivalent to Arduino shiftOut(..., MSBFIRST, ...)
// ============================================================

static void shift_out_byte(uint8_t data)
{
    for (int i = 7; i >= 0; i--)
    {
        gpio_set_level(DATA_PIN, (data >> i) & 0x01);

        gpio_set_level(CLOCK_PIN, 1);
        gpio_set_level(CLOCK_PIN, 0);
    }
}


// ============================================================
// Send 16 bits to the two 74HC595s
//
// This is exactly the same order as your original program:
//
// shiftOut(dataPin, clockPin, MSBFIRST, (Data >> 8));
// shiftOut(dataPin, clockPin, MSBFIRST, Data);
// ============================================================

static void send_data(uint16_t Data)
{
    gpio_set_level(LATCH_PIN, 0);

    shift_out_byte((Data >> 8) & 0xFF);
    shift_out_byte(Data & 0xFF);

    gpio_set_level(LATCH_PIN, 1);
}


// ============================================================
// Initialize GPIOs and 74HC595
// ============================================================

static void relay_init(void)
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


    // --------------------------------------------------------
    // Disable 74HC595 outputs during initialization
    // OE is active LOW
    //
    // HIGH = outputs disabled
    // LOW  = outputs enabled
    // --------------------------------------------------------

    gpio_set_level(OE_PIN, 1);


    // Put control signals into known states

    gpio_set_level(DATA_PIN, 0);
    gpio_set_level(CLOCK_PIN, 0);
    gpio_set_level(LATCH_PIN, 0);


    // --------------------------------------------------------
    // Clear all 74HC595 outputs while outputs are disabled
    // --------------------------------------------------------

    send_data(0x0000);


    // --------------------------------------------------------
    // Enable outputs
    // --------------------------------------------------------

    gpio_set_level(OE_PIN, 0);
}


// ============================================================
// Main
// ============================================================

void app_main(void)
{
    char line[64];

    relay_init();


    printf("\n");
    printf("========================================\n");
    printf(" ESP32-P4 74HC595 Controller\n");
    printf("========================================\n");
    printf("\n");

    printf("Pins:\n");
    printf(" DATA  = GPIO 21\n");
    printf(" CLOCK = GPIO 22\n");
    printf(" LATCH = GPIO 20\n");
    printf(" OE    = GPIO 7\n");
    printf("\n");

    printf("Enter a 16-bit binary value using this format:\n");
    printf("0b0000000000000000\n");



    while (1)
    {
        // ----------------------------------------------------
        // Read a line from serial monitor / UART0
        // ----------------------------------------------------

        if (fgets(line, sizeof(line), stdin) != NULL)
        {
            // Remove CR/LF
            line[strcspn(line, "\r\n")] = '\0';


            // ------------------------------------------------
            // Check length
            //
            // 0b + 16 binary digits = 18 characters
            // ------------------------------------------------

            if (strlen(line) != 18)
            {
                printf("ERR: Expected 0b followed by exactly 16 bits\n");
                continue;
            }


            // ------------------------------------------------
            // Check "0b" prefix
            // ------------------------------------------------

            if (line[0] != '0' || line[1] != 'b')
            {
                printf("ERR: Format must be 0bXXXXXXXXXXXXXXXX\n");
                continue;
            }


            // ------------------------------------------------
            // Convert binary string to uint16_t
            // ------------------------------------------------

            uint16_t Data = 0;
            int valid = 1;

            for (int i = 2; i < 18; i++)
            {
                if (line[i] == '0')
                {
                    Data = (Data << 1);
                }
                else if (line[i] == '1')
                {
                    Data = (Data << 1) | 1;
                }
                else
                {
                    valid = 0;
                    break;
                }
            }


            // ------------------------------------------------
            // Invalid character
            // ------------------------------------------------

            if (!valid)
            {
                printf("ERR: Only 0 and 1 are allowed\n");
                continue;
            }


            // ------------------------------------------------
            // Send the exact 16-bit pattern
            // ------------------------------------------------

            send_data(Data);


            // ------------------------------------------------
            // Confirmation
            // ------------------------------------------------

            printf("Data received: %s\n", line);
        }


        // Small delay so the task doesn't continuously consume CPU
        vTaskDelay(pdMS_TO_TICKS(10));
    }
}