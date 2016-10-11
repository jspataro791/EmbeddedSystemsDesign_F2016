
#ifndef DEBUG_H    /* Guard against multiple inclusion */
#define DEBUG_H

#include "system_definitions.h"

#ifdef __cplusplus
extern "C" {
#endif

    // LED DEBUG PORT AND PIN
#define DBG_LED_PORT PORT_CHANNEL_A
#define DBG_LED_PIN PORTS_BIT_POS_3

    // GPIO PORT AND PIN
#define ERR_GPIO_PORT PORT_CHANNEL_E


    // GPIO ERROR DEFINES
#define ERR_GOOD                      0xFF
#define ERR_GENERIC_BAD          0x00
#define ERR_BAD_MQ_RECV         0x01
#define ERR_BAD_MQ_SEND         0x02
#define ERR_BAD_MQ_CREATE       0x03
#define ERR_BAD_TIMER_INIT          0x04
#define ERR_BAD_TASK_STATE      0x05

    // GPIO STATUS DEFINES

#define STAT_SYS_INIT                         0x06
#define STAT_SYS_TASK_CREATE        0x07
#define STAT_TASK_RX                        0x08
#define STAT_TASK_RX_GOOD            0x09
#define STAT_TASK_RX_INIT                 0x0A
#define STAT_TASK_TX                         0x0B
#define STAT_TASK_TX_GOOD               0x0C
#define STAT_TASK_TX_INIT                  0x0D
#define STAT_TASK_HEARTBEAT           0x0E
#define STAT_TASK_HEARTBEAT_INIT    0x0F
#define STAT_TASK_HEARTBEAT_SEND 0x10
#define STAT_TASK_LOOPBACK             0x11
#define STAT_TASK_LOOPBACK_INIT     0x12
#define STAT_SERIAL_ACK                     0x13
#define STAT_SERIAL_NACK                   0x14
#define STAT_INT_RX_UART0                  0x15


    // initialize GPIO error port
    void initGPIODebug();

    // send error to GPIO
    void sendGPIOError(uint8_t errCode);

    // send status to GPIO
    void sendGPIOStatus(uint8_t stat);

    // toggle LED

#ifdef __cplusplus
}
#endif

#endif /* _EXAMPLE_FILE_NAME_H */

/* *****************************************************************************
 End of File
 */
